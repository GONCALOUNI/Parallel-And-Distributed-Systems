import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as aioredis
from databases import Database
from sqlalchemy import MetaData, Table, Column, String, create_engine
from sqlalchemy.dialects.postgresql import insert as pg_insert
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/appdb")

engine = create_engine(DATABASE_URL)
metadata = MetaData()
kv = Table(
    "kv", metadata,
    Column("key", String, primary_key=True),
    Column("value", String, nullable=False),
)
metadata.create_all(engine)
db = Database(DATABASE_URL)

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
    app.state.db = db
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
    allow_origins=[
        "http://localhost:5173", "http://localhost:5174", "http://localhost:5176"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/health", response_model=StatusResponse, tags=["health"])
async def health():
    try:
        await db.execute("SELECT 1")
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")

    try:
        pong = await app.state.redis.ping()
        if pong is False:
            raise Exception("no pong")
    except Exception:
        raise HTTPException(status_code=503, detail="Redis unavailable")

    return {"status": "ok"}

@app.get("/stats", tags=["stats"])
async def stats():
    count = await db.fetch_val("SELECT COUNT(*) FROM kv")
    return {"items": count}

@app.put("/kv", response_model=StatusResponse, tags=["kv"])
async def put_item(item: KVItem):
    await app.state.redis.set(item.key, item.value)

    stmt = pg_insert(kv).values(
        key=item.key,
        value=item.value
    ).on_conflict_do_update(
        index_elements=["key"],
        set_={"value": item.value}
    )

    await db.execute(stmt)
    return {"status": "ok"}

@app.get("/kv", response_model=GetResponse, tags=["kv"])
async def get_item(key: str):
    val = await app.state.redis.get(key)
    if val is not None:
        return {"data": {"value": val}}
    row = await db.fetch_one(kv.select().where(kv.c.key == key))
    if not row:
        raise HTTPException(status_code=404, detail="Chave não encontrada")
    await app.state.redis.set(key, row["value"])
    return {"data": {"value": row["value"]}}

@app.delete("/kv", response_model=DeleteResponse, tags=["kv"])
async def delete_item(key: str):
    deleted_redis = await app.state.redis.delete(key)
    result = await db.execute(kv.delete().where(kv.c.key == key))
    deleted_sql = bool(result)
    return {
        "key": key,
        "deleted": bool(deleted_redis or deleted_sql)
    }

@app.get("/", include_in_schema=False)
async def homepage():
    return HTMLResponse("""
      <!doctype html>
      <html>
        <head>
          <meta charset="utf-8">
          <title>KVerse</title>
          <style>
            body { font-family: sans-serif; text-align: center; margin: 2rem; }
            ul { list-style: none; padding: 0; }
            li { margin: .5rem 0; }
            a { text-decoration: none; color: #007BFF; }
            a:hover { text-decoration: underline; }
          </style>
        </head>
        <body>
          <h1>Gestor de backend KVerse</h1>
          <ul>
            <li><a href="/docs">Swagger UI</a></li>
            <li><a href="/redoc">ReDoc</a></li>
            <li><a href="/openapi.json">OpenAPI JSON</a></li>
            <li><a href="/health">Health Check</a></li>
          </ul>
        </body>
      </html>
    """)