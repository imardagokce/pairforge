import os
import re
from concurrent.futures import ThreadPoolExecutor

import requests

from aider.i18n import _

DEFAULT_OLLAMA_BASE = "http://127.0.0.1:11434"
DEFAULT_LM_STUDIO_BASE = "http://127.0.0.1:1234/v1"
DEFAULT_LLAMA_CPP_BASE = "http://127.0.0.1:8080/v1"

LOCAL_PREFIXES = ("ollama/", "ollama_chat/", "lm_studio/")

# (substring, context window, extra settings). The first matching entry wins.
_LOCAL_FAMILIES = [
    ("qwen2.5-coder", 32768, {}),
    ("qwen2.5coder", 32768, {}),
    ("qwen3", 40960, {"reasoning_tag": "think"}),
    ("qwen2.5", 32768, {}),
    ("qwen2", 32768, {}),
    ("deepseek-r1", 131072, {"reasoning_tag": "think"}),
    ("deepseek-coder-v2", 163840, {}),
    ("deepseek-coder", 16384, {}),
    ("codellama", 16384, {}),
    ("codestral", 32768, {}),
    ("llama3.1", 131072, {}),
    ("llama3.2", 131072, {}),
    ("llama3.3", 131072, {}),
    ("llama3", 8192, {}),
    ("gemma3", 131072, {}),
    ("gemma2", 8192, {}),
    ("gemma", 8192, {}),
    ("phi4", 16384, {}),
    ("phi3", 4096, {}),
    ("mistral-nemo", 131072, {}),
    ("mistral", 32768, {}),
]

_PARAM_SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)b\b")


def local_model_preset(name):
    """Return default settings for a common local model, or None.

    Only names with a LOCAL_PREFIXES prefix are considered. The preset holds the
    context window, output limit, edit format (diff for models of 14B and up,
    whole otherwise) and, for reasoning models, the reasoning tag.
    """
    if not name or not name.startswith(LOCAL_PREFIXES):
        return None

    stripped = name.split("/", 1)[1].lower()

    family = None
    for key, context, extra in _LOCAL_FAMILIES:
        if key in stripped:
            family = (key, context, extra)
            break
    if family is None:
        return None

    key, context, extra = family
    size_match = _PARAM_SIZE_RE.search(stripped)
    size = float(size_match.group(1)) if size_match else None

    preset = {
        "family": key,
        "max_input_tokens": context,
        "max_output_tokens": min(8192, context // 4),
        "edit_format": "diff" if size is not None and size >= 14 else "whole",
        "use_repo_map": True,
    }
    preset.update(extra)
    return preset


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
            _("Could not reach Ollama at {base_url}. Is `ollama serve` running?").format(
                base_url=base_url
            )
        )

    if response.status_code != 200:
        raise LocalModelError(
            _("Ollama at {base_url} returned HTTP {status} for /api/tags.").format(
                base_url=base_url, status=response.status_code
            )
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
        raise LocalModelError(
            _("Ollama at {base_url} returned an unexpected response.").format(base_url=base_url)
        )

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
            _("Could not reach an OpenAI-compatible server at {base_url}. Is it running?").format(
                base_url=base_url
            )
        )

    if response.status_code in (401, 403):
        raise LocalModelError(
            _("The API key was rejected by {url} (HTTP {status}).").format(
                url=url, status=response.status_code
            )
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
            _(
                "No local model servers found. Start Ollama, LM Studio or a llama.cpp server,"
                " then try again."
            )
        )

    candidates = [(model, server) for server in servers for model in server["models"]]
    if not candidates:
        raise LocalModelError(
            _(
                "Local servers are running but have no models. Pull or load one first,"
                " for example: ollama pull qwen2.5-coder:7b"
            )
        )

    if wanted:
        for model, server in candidates:
            if model == wanted or model.split("/", 1)[-1] == wanted:
                return model, server
        available = ", ".join(model for model, _ in candidates)
        raise LocalModelError(
            _("Local model {wanted} was not found. Available: {available}").format(
                wanted=wanted, available=available
            )
        )

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
        io.tool_output(
            _("Using local model {model} from {name} at {base_url}").format(
                model=model, name=server["name"], base_url=server["base_url"]
            )
        )
        if server["name"] == "LM Studio" and not os.environ.get("LM_STUDIO_API_BASE"):
            os.environ["LM_STUDIO_API_BASE"] = server["base_url"]
        elif server["name"] == "llama.cpp":
            os.environ["OPENAI_API_BASE"] = server["base_url"]

    from aider import models

    exact_match = any(ms.name == args.model for ms in models.MODEL_SETTINGS)
    known = exact_match or local_model_preset(args.model) is not None
    if args.edit_format is None and not known:
        args.edit_format = "whole"
        io.tool_output(_("Using the whole edit format, which small models handle most reliably."))

    if args.permission_mode is None:
        args.permission_mode = "auto"

    return True


def is_small_local_model(name, max_billions=17):
    """True for a local model whose name gives a size of max_billions parameters or fewer."""
    if not name or not name.startswith(LOCAL_PREFIXES):
        return False
    size_match = _PARAM_SIZE_RE.search(name.split("/", 1)[1].lower())
    if size_match is None:
        return False
    return float(size_match.group(1)) <= max_billions
