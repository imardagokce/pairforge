"""Local heuristic for choosing a reasoning effort level per user message.

Used when reasoning effort is set to ``auto``. No LLM call is made; the choice
is a deterministic function of the message text.

Rules (checked in this order):

1. high: the message is longer than 600 characters, OR it contains any
   high-signal word (whole words, case-insensitive): architecture, redesign,
   refactor, race condition, deadlock, concurrency, performance, optimize,
   debug, root cause, security, migrate, algorithm, prove, design.
2. low: the message is under 80 characters (and so not high), OR it contains
   any low-signal word (whole words, case-insensitive): typo, rename, comment,
   docstring, format, formatting, lint, whitespace, AND the message is under
   300 characters.
3. medium: everything else.

Length is measured in Python characters (``len(message)``).
"""

import re

AUTO = "auto"

LEVELS = ("low", "medium", "high")

HIGH_WORDS = (
    "architecture",
    "redesign",
    "refactor",
    "race condition",
    "deadlock",
    "concurrency",
    "performance",
    "optimize",
    "debug",
    "root cause",
    "security",
    "migrate",
    "algorithm",
    "prove",
    "design",
)

LOW_WORDS = (
    "typo",
    "rename",
    "comment",
    "docstring",
    "format",
    "formatting",
    "lint",
    "whitespace",
)

HIGH_LENGTH = 600
LOW_LENGTH = 80
LOW_WORD_LENGTH = 300


def _word_pattern(phrase):
    """Compile a whole-word, case-insensitive pattern for a phrase.

    Spaces in the phrase match any run of whitespace.
    """
    body = r"\s+".join(re.escape(part) for part in phrase.split())
    return re.compile(r"\b" + body + r"\b", re.IGNORECASE)


_HIGH_PATTERNS = [_word_pattern(w) for w in HIGH_WORDS]
_LOW_PATTERNS = [_word_pattern(w) for w in LOW_WORDS]


def _contains_any(message, patterns):
    return any(p.search(message) for p in patterns)


def choose_reasoning_effort(message: str) -> str:
    """Return "low", "medium" or "high" for a user message.

    See the module docstring for the exact rules.
    """
    message = message or ""
    length = len(message)

    if length > HIGH_LENGTH or _contains_any(message, _HIGH_PATTERNS):
        return "high"

    if length < LOW_LENGTH:
        return "low"

    if length < LOW_WORD_LENGTH and _contains_any(message, _LOW_PATTERNS):
        return "low"

    return "medium"
