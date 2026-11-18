import os
from urllib.parse import urlsplit

import requests

DEFAULT_OLLAMA_BASE = "http://127.0.0.1:11434"
DEFAULT_OMNIROUTE_BASE = "http://localhost:20128/v1"


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


def list_openai_compatible_models(base_url, api_key=None, timeout=3):
    """Return sorted model ids from an OpenAI-compatible server (GET <base_url>/models)."""
    base_url = base_url.rstrip("/")
    url = f"{base_url}/models"
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
    except requests.RequestException:
        raise LocalModelError(
            f"Could not reach an OpenAI-compatible server at {base_url}. Is it running?"
        )

    if response.status_code in (401, 403):
        raise LocalModelError(
            f"The API key was rejected by {url} (HTTP {response.status_code})."
        )
    if response.status_code != 200:
        raise LocalModelError(f"{url} returned HTTP {response.status_code}.")

    try:
        data = response.json()
        ids = [str(item["id"]) for item in data["data"]]
    except (ValueError, KeyError, TypeError):
        raise LocalModelError(f"{url} returned an unexpected response.")

    return sorted(ids)


def is_local_url(url):
    """Return True if url is an http(s) URL pointing at this machine."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return False
    if parts.scheme not in ("http", "https"):
        return False
    return parts.hostname in ("localhost", "127.0.0.1", "::1")
