"""Permission modes and folder trust for file prompts."""

import json
import os
import tempfile
from pathlib import Path

MODES = ("ask", "auto")
DEFAULT_MODE = "ask"


def trust_file_path():
    override = os.environ.get("AIDER_TRUST_FILE")
    if override:
        return Path(override)
    return Path.home() / ".aider" / "trusted_folders.json"


def _as_str_list(value):
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _load():
    try:
        data = json.loads(trust_file_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    return {
        "trusted": _as_str_list(data.get("trusted")),
        "declined": _as_str_list(data.get("declined")),
    }


def _save(data):
    path = trust_file_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), prefix=".trusted_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def path_inside(root, path):
    """True if path equals root or lies inside it (both resolved)."""
    root = Path(root).resolve()
    path = Path(path).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def is_trusted(path):
    path = Path(path).resolve()
    return any(path_inside(entry, path) for entry in _load()["trusted"])


def is_declined(path):
    resolved = str(Path(path).resolve())
    return resolved in _load()["declined"]


def trust(path):
    resolved = str(Path(path).resolve())
    data = _load()
    if resolved not in data["trusted"]:
        data["trusted"].append(resolved)
    data["declined"] = [p for p in data["declined"] if p != resolved]
    _save(data)


def decline(path):
    resolved = str(Path(path).resolve())
    data = _load()
    if resolved not in data["declined"]:
        data["declined"].append(resolved)
    _save(data)


class PermissionPolicy:
    """Decides whether file prompts may be skipped in the current session."""

    def __init__(self, mode=DEFAULT_MODE, trusted=False, root=None):
        self.mode = mode
        self.trusted = trusted
        self.root = Path(root or Path.cwd()).resolve()

    def auto_allows(self, abs_path):
        return self.mode == "auto" and self.trusted and path_inside(self.root, abs_path)

    def auto_allows_action(self):
        """Shell commands, URLs, lint/test fixes and the like: no path check."""
        return self.mode == "auto" and self.trusted
