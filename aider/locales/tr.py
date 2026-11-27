"""Turkish interface messages: English text -> Turkish text.

The catalog is split by area so parts can be edited independently; keep each
translation's {placeholders} identical to the English text.
"""

from aider.locales import tr_coders, tr_commands, tr_core, tr_main

MESSAGES = {}
for _part in (tr_core, tr_main, tr_coders, tr_commands):
    MESSAGES.update(_part.MESSAGES)
