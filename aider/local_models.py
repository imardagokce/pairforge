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
                sizes = {f"ollama_chat/{m['name']}": m["size_gb"] for m in found}
                return {"name": name, "base_url": base_url, "models": list(sizes), "sizes": sizes}
            ids = list_openai_compatible_models(base_url, timeout=timeout)
        except LocalModelError:
            return None
        models = [prefixes[name] + model_id for model_id in ids]
        return {"name": name, "base_url": base_url, "models": models}

    # Probe in parallel: a refused connection can take about a second on Windows.
    addresses = local_server_addresses()
    with ThreadPoolExecutor(max_workers=len(addresses)) as pool:
        results = list(pool.map(lambda pair: probe(*pair), addresses))
    return [server for server in results if server]


def choose_local_model(servers, wanted=None):
    """Pick a model from discovered servers. Returns (model_name, server).

    With wanted, match it with or without the provider prefix. Otherwise prefer
    models whose name mentions "coder", then the largest one (Ollama reports
    sizes), keeping discovery order on ties.
    """
    if not servers:
        raise LocalModelError(
            "No local model servers found. Start Ollama, LM Studio or a llama.cpp server,"
            " then try again."
        )

    candidates = [(model, server) for server in servers for model in server["models"]]
    if not candidates:
        raise LocalModelError(
            "Local servers are running but have no models. Pull or load one first,"
            " for example: ollama pull qwen2.5-coder:7b"
        )

    if wanted:
        for model, server in candidates:
            if model == wanted or model.split("/", 1)[-1] == wanted:
                return model, server
        available = ", ".join(model for model, _ in candidates)
        raise LocalModelError(f"Local model {wanted} was not found. Available: {available}")

    def rank(item):
        model, server = item
        is_coder = "coder" in model.lower()
        size = server.get("sizes", {}).get(model, 0)
        return (not is_coder, -size)

    return min(candidates, key=rank)


def apply_local_quickstart(args, io, discover=None):
    """Configure args for --local. Returns False if pairforge should exit.

    Picks a local model unless --model was given, points LiteLLM at the server,
    uses the whole edit format for models without known settings, and turns on
    auto permission mode unless --permission-mode was given.
    """
    if args.local is None:
        return True

    if not args.model:
        try:
            servers = (discover or discover_local_servers)()
            model, server = choose_local_model(servers, args.local or None)
        except LocalModelError as err:
            io.tool_error(str(err))
            return False
        args.model = model
        io.tool_output(f"Using local model {model} from {server['name']} at {server['base_url']}")
        if server["name"] == "LM Studio" and not os.environ.get("LM_STUDIO_API_BASE"):
            os.environ["LM_STUDIO_API_BASE"] = server["base_url"]
        elif server["name"] == "llama.cpp":
            os.environ["OPENAI_API_BASE"] = server["base_url"]

    from aider import models

    known = any(ms.name == args.model for ms in models.MODEL_SETTINGS)
    if args.edit_format is None and not known:
        args.edit_format = "whole"
        io.tool_output("Using the whole edit format, which small models handle most reliably.")

    if args.permission_mode is None:
        args.permission_mode = "auto"

    return True
