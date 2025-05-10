import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from databases import Database
from sqlalchemy import MetaData, Table, Column, String, create_engine

BASE_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = BASE_DIR / "data"
os.makedirs(DATA_DIR, exist_ok=True)

DB_FILE = DATA_DIR / "db.sqlite"
DATABASE_URL = f"sqlite:///{DB_FILE}"

metadata = MetaData()
kv = Table("kv", metadata,
    Column("key", String, primary_key=True),
    Column("value", String, nullable=False),
)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)
db = Database(DATABASE_URL)

app = FastAPI(title="KVerse: A KV Store")

@app.on_event("startup")
async def connect_db():
    await db.connect()

@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.put("/")
async def put_item(data: dict):
    key = data["data"]["key"]
    value = data["data"]["value"]
    await db.execute(kv.insert().values(key=key, value=value).prefix_with("OR REPLACE"))
    return {"status": "ok"}

@app.get("/")
async def get_item(key: str):
    row = await db.fetch_one(kv.select().where(kv.c.key == key))
    if not row:
        raise HTTPException(404, "Not found")
    return {"data": {"value": row["value"]}}

@app.delete("/")
async def delete_item(key: str):
    deleted = await db.execute(kv.delete().where(kv.c.key == key))
    return {"deleted": bool(deleted)}