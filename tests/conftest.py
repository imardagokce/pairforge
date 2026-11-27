import os

import pytest

# Tests assert on English messages; a Turkish system locale must not switch them.
os.environ["PAIRFORGE_LANG"] = "en"


@pytest.fixture(autouse=True)
def _english_interface():
    from aider import i18n

    i18n.set_language("en")
    yield
    i18n.set_language("en")
