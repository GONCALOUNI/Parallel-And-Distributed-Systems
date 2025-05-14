import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from databases import Database
from sqlalchemy import MetaData, Table, Column, String, create_engine

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

# ---------- FastAPI com lifespan ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

app = FastAPI(title="KVerse", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.put("/")
async def put_item(data: dict):
    key   = data["data"]["key"]
    value = data["data"]["value"]
    query = kv.insert().values(key=key, value=value).prefix_with("OR REPLACE")
    await db.execute(query)
    return {"status": "ok"}

@app.get("/")
async def get_item(key: str):
    row = await db.fetch_one(kv.select().where(kv.c.key == key))
    if not row:
        raise HTTPException(status_code=404, detail="Chave não encontrada")
    return {"data": {"value": row["value"]}}

@app.delete("/")
async def delete_item(key: str):
    deleted = await db.execute(kv.delete().where(kv.c.key == key))
    return {"deleted": bool(deleted)}