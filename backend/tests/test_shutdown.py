import asyncio
from fastapi.testclient import TestClient
import app.main as main_app
import app.routes.shutdown as shutdown_module


class DummyTask:
    def __init__(self):
        self._cb = None

    def add_done_callback(self, cb):
        self._cb = cb

    def result(self):
        return None


def test_shutdown_disabled(monkeypatch):
    # Ensure remote shutdown is disabled
    monkeypatch.setattr(shutdown_module, "ALLOW_REMOTE_SHUTDOWN", False)
    monkeypatch.setattr(shutdown_module, "SHUTDOWN_TOKEN", None)

    client = TestClient(main_app.app)
    resp = client.post("/shutdown")

    assert resp.status_code == 403
    assert "disabled" in resp.json().get("detail", "").lower()


def test_shutdown_with_token_validation(monkeypatch):
    # Enable shutdown and configure a token
    monkeypatch.setattr(shutdown_module, "ALLOW_REMOTE_SHUTDOWN", True)
    monkeypatch.setattr(shutdown_module, "SHUTDOWN_TOKEN", "s3cr3t")

    recorded = {"called": False, "coro": None}

    def fake_create_task(coro):
        # Record that create_task was invoked and what coroutine was passed
        recorded["called"] = True
        recorded["coro"] = coro
        return DummyTask()

    monkeypatch.setattr(asyncio, "create_task", fake_create_task)

    client = TestClient(main_app.app)

    # Missing header -> 401
    resp = client.post("/shutdown")
    assert resp.status_code == 401

    # Wrong header -> 401
    resp = client.post("/shutdown", headers={"X-Shutdown-Token": "wrong"})
    assert resp.status_code == 401

    # Correct header -> 200 and task scheduled
    resp = client.post("/shutdown", headers={"X-Shutdown-Token": "s3cr3t"})
    assert resp.status_code == 200
    assert recorded["called"] is True


def test_shutdown_enabled_without_token(monkeypatch):
    # Enable shutdown but do not require token
    monkeypatch.setattr(shutdown_module, "ALLOW_REMOTE_SHUTDOWN", True)
    monkeypatch.setattr(shutdown_module, "SHUTDOWN_TOKEN", None)

    recorded = {"called": False}

    def fake_create_task(coro):
        recorded["called"] = True
        return DummyTask()

    monkeypatch.setattr(asyncio, "create_task", fake_create_task)

    client = TestClient(main_app.app)
    resp = client.post("/shutdown")

    assert resp.status_code == 200
    assert recorded["called"] is True
