import pytest
from fastapi.testclient import TestClient
from main import app, metadata, engine, db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)
    db._database_url = "sqlite:///:memory:"
    import asyncio
    asyncio.get_event_loop().run_until_complete(db.connect())
    yield
    asyncio.get_event_loop().run_until_complete(db.disconnect())

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}

def test_put_get_delete():
    # PUT
    r = client.put("/", json={"data": {"key": "foo", "value": "bar"}})
    assert r.status_code == 200
    # GET
    r = client.get("/?key=foo")
    assert r.json() == {"data": {"value": "bar"}}
    # DELETE
    r = client.delete("/?key=foo")
    assert r.json() == {"deleted": True}
    # GET (404)
    r = client.get("/?key=foo")
    assert r.status_code == 404
