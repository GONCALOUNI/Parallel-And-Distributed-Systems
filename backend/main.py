import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlalchemy import MetaData, Table, Column, String, create_engine
from pydantic import BaseModel

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "db.sqlite")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

metadata = MetaData()
kv = Table(
    "kv", metadata,
    Column("key",   String, primary_key=True),
    Column("value", String, nullable=False),
)

metadata.create_all(engine)
db = Database(SQLALCHEMY_DATABASE_URL)

class KVItem(BaseModel):
    key: str
    value: str

class StatusResponse(BaseModel):
    status: str

class GetResponse(BaseModel):
    data: dict

class DeleteResponse(BaseModel):
    key: str
    deleted: bool

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(
    title="KVerse KV Store API",
    version="1.0.0",
    description="API para gerir pares key–value (CRUD simples + health-check)",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/health", response_model=StatusResponse, tags=["health"])
async def health():
    """Verifica se o serviço está a funcionar."""
    return {"status": "ok"}

@app.put("/", response_model=StatusResponse, tags=["kv"])
async def put_item(item: KVItem):
    """Insere ou atualiza um par key–value."""
    query = kv.insert().values(key=item.key, value=item.value).prefix_with("OR REPLACE")
    await db.execute(query)
    return {"status": "ok"}

@app.get("/", response_model=GetResponse, tags=["kv"])
async def get_item(key: str):
    """Obtém o valor associado a uma key."""
    row = await db.fetch_one(kv.select().where(kv.c.key == key))
    if not row:
        raise HTTPException(status_code=404, detail="Chave não encontrada")
    return {"data": {"value": row["value"]}}

@app.delete("/", response_model=DeleteResponse, tags=["kv"])
async def delete_item(key: str):
    """Remove uma key do armazenamento."""
    result = await db.execute(kv.delete().where(kv.c.key == key))
    return {"key": key, "deleted": bool(result)}