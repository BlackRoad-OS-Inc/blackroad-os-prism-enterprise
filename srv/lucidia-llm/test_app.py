from importlib import util
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent
APP_MODULE_PATH = ROOT / "app.py"


def _load_app():
    spec = util.spec_from_file_location("lucidia_llm_app", APP_MODULE_PATH)
    if spec is None or spec.loader is None:  # pragma: no cover - safety check
        raise ImportError(f"Unable to load FastAPI app from {APP_MODULE_PATH}")

    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


app = _load_app()


def test_health():
    client = TestClient(app)
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'ok'


def test_chat_stub_mode():
    """Without LUCIDIA_BACKEND_URL the bridge echoes the prompt."""
    client = TestClient(app)
    resp = client.post('/chat', json={'prompt': 'hello'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'text' in data
    assert 'hello' in data['text']
