import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis
from databases import Database
from sqlalchemy import MetaData, Table, Column, String, create_engine
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_FILE = DATA_DIR / "db.sqlite"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
metadata = MetaData()
kv = Table(
    "kv", metadata,
    Column("key", String, primary_key=True),
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
    app.state.redis = aioredis.from_url(
        "redis://redis:6379/0", decode_responses=True
    )
    yield
    await db.disconnect()
    await app.state.redis.close()

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
    return {"status": "ok"}

@app.put("/", response_model=StatusResponse, tags=["kv"])
async def put_item(item: KVItem):
    await app.state.redis.set(item.key, item.value)
    query = kv.insert().values(key=item.key, value=item.value).prefix_with("OR REPLACE")
    await db.execute(query)
    return {"status": "ok"}

@app.get("/", response_model=GetResponse, tags=["kv"])
async def get_item(key: str):
    val = await app.state.redis.get(key)
    if val is not None:
        return {"data": {"value": val}}
    row = await db.fetch_one(kv.select().where(kv.c.key == key))
    if not row:
        raise HTTPException(status_code=404, detail="Chave não encontrada")
    await app.state.redis.set(key, row["value"])
    return {"data": {"value": row["value"]}}

@app.delete("/", response_model=DeleteResponse, tags=["kv"])
async def delete_item(key: str):
    deleted_redis = await app.state.redis.delete(key)
    result = await db.execute(kv.delete().where(kv.c.key == key))
    deleted_sql = bool(result)
    return {
        "key": key,
        "deleted": bool(deleted_redis or deleted_sql)
    }