import os

import requests

DEFAULT_OLLAMA_BASE = "http://127.0.0.1:11434"


class LocalModelError(Exception):
    """Raised when a local model server cannot be queried."""


def list_ollama_models(base_url=None, timeout=3):
    """Return models served by a local Ollama server.

    Returns a list of dicts: {"name": str, "size_gb": float}.
    """
    if not base_url:
        base_url = os.environ.get("OLLAMA_API_BASE") or DEFAULT_OLLAMA_BASE
    base_url = base_url.rstrip("/")
    url = f"{base_url}/api/tags"

    try:
        response = requests.get(url, timeout=timeout)
    except requests.RequestException:
        raise LocalModelError(
            f"Could not reach Ollama at {base_url}. Is `ollama serve` running?"
        )

    if response.status_code != 200:
        raise LocalModelError(
            f"Ollama at {base_url} returned HTTP {response.status_code} for /api/tags."
        )

    try:
        data = response.json()
        raw_models = data["models"]
        models = []
        for item in raw_models:
            models.append(
                {
                    "name": str(item["name"]),
                    "size_gb": round(float(item.get("size", 0)) / (1024**3), 1),
                }
            )
    except (ValueError, KeyError, TypeError):
        raise LocalModelError(f"Ollama at {base_url} returned an unexpected response.")

    return models
