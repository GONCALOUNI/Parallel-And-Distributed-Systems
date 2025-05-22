import pytest
import asyncio
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from main import app, metadata, engine, db

client = TestClient(app)

@pytest.fixture(autouse=True, scope="function")
def setup_db():
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)
    db._database_url = "sqlite:///:memory:"

    app.state.redis = AsyncMock()
    app.state.redis.get = AsyncMock(side_effect=lambda key: None if key == "foo" else "bar")
    app.state.redis.set = AsyncMock()
    app.state.redis.delete = AsyncMock(return_value=1)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(db.connect())

    yield

    loop.run_until_complete(db.disconnect())
    loop.close()

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_put_get_delete():
    
    # PUT
    r = client.put("/kv", json={"key": "foo", "value": "bar"})
    assert r.status_code == 200 and r.json() == {"status": "ok"}

    # GET
    r = client.get("/kv?key=foo")
    assert r.status_code == 200 and r.json() == {"data": {"value": "bar"}}

    # DELETE
    r = client.delete("/kv?key=foo")
    assert r.status_code == 200 and r.json() == {"key": "foo", "deleted": True}

    # GET (404)
    r = client.get("/kv?key=foo")
    assert r.status_code == 404