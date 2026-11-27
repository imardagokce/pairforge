from pathlib import Path

from aider.dump import dump  # noqa: F401

VERSION_CHECK_FNAME = Path.home() / ".aider" / "caches" / "versioncheck"

# pairforge is not published on PyPI, so upstream Aider releases are never offered as
# updates (pip-installing the upstream package would replace pairforge with upstream Aider).
UPDATE_TEXT = "pairforge is updated with `git pull` in its checkout."


def install_from_main_branch(io):
    """
    pairforge is updated by pulling its git checkout, not by pip.
    """

    io.tool_output(UPDATE_TEXT)
    return False


def install_upgrade(io, latest_version=None):
    """
    pairforge is updated by pulling its git checkout, not by pip.
    """

    io.tool_output(UPDATE_TEXT)
    return False


def check_version(io, just_check=False, verbose=False):
    """
    Update checks are disabled for pairforge: it is not on PyPI.
    """

    return False
