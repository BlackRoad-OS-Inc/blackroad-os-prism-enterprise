import json
from importlib.machinery import SourceFileLoader
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

module = SourceFileLoader("llm_stub", "srv/lucidia-llm/app.py").load_module()
app = module.app
client = TestClient(app)


def _ollama_response(content: str):
    """Return a mock httpx.Response that simulates an Ollama /api/chat reply."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"message": {"role": "assistant", "content": content}}
    mock_resp.raise_for_status = MagicMock()
    return mock_resp


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_chat_returns_ollama_response():
    with patch("httpx.post", return_value=_ollama_response("pong")) as mock_post:
        res = client.post("/chat", json={"prompt": "ping"})
    assert res.status_code == 200
    assert res.json()["text"] == "pong"
    mock_post.assert_called_once()
    body = mock_post.call_args.kwargs.get("json", {})
    assert any(m["role"] == "user" and m["content"] == "ping" for m in body["messages"])


def test_chat_includes_system_when_present():
    with patch("httpx.post", return_value=_ollama_response("all good")) as mock_post:
        res = client.post("/chat", json={"prompt": "status", "system": "SYS"})
    assert res.status_code == 200
    assert res.json()["text"] == "all good"
    body = mock_post.call_args.kwargs.get("json", {})
    assert any(m["role"] == "system" and m["content"] == "SYS" for m in body["messages"])
