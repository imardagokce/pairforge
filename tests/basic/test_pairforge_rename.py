"""pairforge must never install upstream Aider from PyPI ("aider-chat") at runtime."""

import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import aider
from aider import utils, versioncheck
from aider.help import install_help_extra
from aider.scrape import install_playwright


def _all_strings(obj):
    if isinstance(obj, (list, tuple)):
        for item in obj:
            yield from _all_strings(item)
    else:
        yield str(obj)


class TestPairforgeRename(unittest.TestCase):
    def test_no_source_builds_aider_chat_package(self):
        pkg_dir = Path(aider.__file__).parent
        offenders = []
        for path in pkg_dir.rglob("*.py"):
            if "website" in path.parts:
                continue
            if "aider-chat" in path.read_text(encoding="utf-8"):
                offenders.append(str(path))
        self.assertEqual(offenders, [])

    def test_help_extra_does_not_install_aider_chat(self):
        io = MagicMock()
        with patch("aider.utils.check_pip_install_extra", return_value=True) as check:
            install_help_extra(io)
        pip_args = check.call_args.args[3]
        self.assertFalse(any("aider-chat" in s for s in _all_strings(pip_args)))
        self.assertIn("llama-index-embeddings-huggingface", pip_args)

    def test_playwright_extra_does_not_install_aider_chat(self):
        io = MagicMock()
        io.confirm_ask.return_value = True
        with patch("aider.scrape.check_env", return_value=(False, False)), patch(
            "aider.utils.run_install", return_value=(True, "")
        ) as run_install:
            install_playwright(io)
        self.assertTrue(run_install.called)
        for call in run_install.call_args_list:
            self.assertFalse(any("aider-chat" in s for s in _all_strings(call.args[0])))
        self.assertIn("playwright", utils.EXTRA_PACKAGES["playwright"])

    def test_upgrade_paths_never_call_pip(self):
        io = MagicMock()
        with patch("aider.utils.check_pip_install_extra") as check, patch(
            "aider.utils.run_install"
        ) as run_install:
            self.assertFalse(versioncheck.install_upgrade(io, "9.9.9"))
            self.assertFalse(versioncheck.install_from_main_branch(io))
        check.assert_not_called()
        run_install.assert_not_called()

    def test_check_version_is_silent_and_false(self):
        io = MagicMock()
        self.assertFalse(versioncheck.check_version(io, just_check=True, verbose=True))
        self.assertFalse(versioncheck.check_version(io))
        io.tool_output.assert_not_called()
        io.tool_error.assert_not_called()
