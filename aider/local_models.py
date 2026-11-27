import os
from concurrent.futures import ThreadPoolExecutor

import requests

DEFAULT_OLLAMA_BASE = "http://127.0.0.1:11434"
DEFAULT_LM_STUDIO_BASE = "http://127.0.0.1:1234/v1"
DEFAULT_LLAMA_CPP_BASE = "http://127.0.0.1:8080/v1"


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


def _env_base(name, default):
    return (os.environ.get(name) or default).rstrip("/")


def local_server_addresses():
    """(name, base_url) for each local server type pairforge knows how to find."""
    return [
        ("Ollama", _env_base("OLLAMA_API_BASE", DEFAULT_OLLAMA_BASE)),
        ("LM Studio", _env_base("LM_STUDIO_API_BASE", DEFAULT_LM_STUDIO_BASE)),
        ("llama.cpp", _env_base("LLAMA_CPP_API_BASE", DEFAULT_LLAMA_CPP_BASE)),
    ]


def discover_local_servers(timeout=1):
    """Probe the known local model servers and return the ones that answer.

    Returns a list of dicts: {"name", "base_url", "models"}, where each model
    name already carries the prefix to pass to /model. Servers that are not
    running, or that answer with something unexpected, are left out.
    """
    prefixes = {"LM Studio": "lm_studio/", "llama.cpp": "openai/"}

    def probe(name, base_url):
        try:
            if name == "Ollama":
                found = list_ollama_models(base_url, timeout=timeout)
                models = [f"ollama_chat/{m['name']}" for m in found]
            else:
                ids = list_openai_compatible_models(base_url, timeout=timeout)
                models = [prefixes[name] + model_id for model_id in ids]
        except LocalModelError:
            return None
        return {"name": name, "base_url": base_url, "models": models}

    # Probe in parallel: a refused connection can take about a second on Windows.
    addresses = local_server_addresses()
    with ThreadPoolExecutor(max_workers=len(addresses)) as pool:
        results = list(pool.map(lambda pair: probe(*pair), addresses))
    return [server for server in results if server]
