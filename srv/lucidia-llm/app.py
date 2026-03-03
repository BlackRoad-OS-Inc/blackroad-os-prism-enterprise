"""Lucidia LLM service — proxies to a local Ollama instance.

Runs on port 8000 and forwards requests to Ollama.  No external provider
API keys are required.  Set OLLAMA_URL to override the Ollama base URL.
Set OLLAMA_MODEL (or LUCIDIA_MODEL) to choose the model.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Lucidia LLM Stub", version="0.2.0")

OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", os.getenv("LUCIDIA_MODEL", "llama3"))


class ChatRequest(BaseModel):
    prompt: str
    system: Optional[str] = None
    stream: Optional[bool] = False
    model: Optional[str] = None


class ChatResponse(BaseModel):
    text: str


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "backend": "ollama", "url": OLLAMA_URL}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> Dict[str, Any]:
    model = req.model or OLLAMA_MODEL
    messages = []
    if req.system:
        messages.append({"role": "system", "content": req.system})
    messages.append({"role": "user", "content": req.prompt})
    payload: Dict[str, Any] = {"model": model, "messages": messages, "stream": False}
    try:
        r = httpx.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=120.0)
        r.raise_for_status()
        data = r.json()
        text: str = (data.get("message") or {}).get("content", "")
        return {"text": text}
    except httpx.ConnectError as exc:
        raise HTTPException(status_code=502, detail=f"Ollama unreachable at {OLLAMA_URL}") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text) from exc
