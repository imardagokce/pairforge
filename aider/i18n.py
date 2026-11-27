"""Interface language for pairforge's own messages.

Messages are written in English in the code and wrapped in ``_()``. When the
interface language is not English, ``_()`` looks the English text up in that
language's catalog (``aider/locales/<lang>.py``) and returns the translation,
or the English text when there is none. Placeholders such as ``{fname}`` are
kept in the translation and filled in by the caller with ``.format()``.

Prompts sent to the model are never translated here.
"""

import importlib
import locale
import os

SUPPORTED = ("en", "tr")
LANGUAGE_NAMES = {"en": "English", "tr": "Turkish"}

_language = "en"
_catalog = {}


def _system_language():
    for var in ("LC_ALL", "LC_MESSAGES", "LANG", "LANGUAGE"):
        value = os.environ.get(var)
        if value:
            return value
    if os.name == "nt":
        try:
            import ctypes

            lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
            return locale.windows_locale.get(lang_id, "")
        except Exception:
            pass
    try:
        return locale.getlocale()[0] or ""
    except ValueError:
        return ""


def normalize(value):
    """Map a language or locale string ("tr_TR.UTF-8", "Turkish", "tr") to a supported code."""
    value = (value or "").strip().lower()
    if value.startswith(("tr", "turkish")):
        return "tr"
    return "en"


def detect_language(explicit=None):
    """Interface language: explicit choice, then PAIRFORGE_LANG, then the system language."""
    if explicit:
        return normalize(explicit)
    env = os.environ.get("PAIRFORGE_LANG")
    if env:
        return normalize(env)
    return normalize(_system_language())


def set_language(lang):
    global _language, _catalog
    _language = normalize(lang)
    if _language == "en":
        _catalog = {}
        return _language
    try:
        module = importlib.import_module(f"aider.locales.{_language}")
        _catalog = dict(module.MESSAGES)
    except (ImportError, AttributeError):
        _language, _catalog = "en", {}
    return _language


def get_language():
    return _language


def _(text):
    """Translate an English interface message to the current language."""
    return _catalog.get(text, text)
