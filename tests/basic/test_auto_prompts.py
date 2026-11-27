"""Auto permission mode in a trusted folder should not stop for routine questions."""

import os
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from aider.coders import Coder
from aider.commands import Commands
from aider.io import InputOutput
from aider.main import setup_git
from aider.models import Model
from aider.permissions import PermissionPolicy
from aider.utils import GitTemporaryDirectory, IgnorantTemporaryDirectory


def make_io(mode="auto", trusted=True, root=None):
    io = InputOutput(pretty=False, yes=False)
    io.confirm_ask = MagicMock(return_value=False)
    io.tool_output = MagicMock()
    io.permission_policy = PermissionPolicy(mode, trusted, root or Path.cwd())
    return io


class TestOfferUrl(unittest.TestCase):
    def test_auto_mode_prints_url_without_asking(self):
        io = make_io()
        with patch("webbrowser.open") as browser:
            self.assertFalse(io.offer_url("https://example.com/docs"))
        io.confirm_ask.assert_not_called()
        browser.assert_not_called()
        io.tool_output.assert_called_with("More info: https://example.com/docs")

    def test_ask_mode_still_asks(self):
        io = make_io(mode="ask")
        io.offer_url("https://example.com/docs")
        io.confirm_ask.assert_called_once()

    def test_untrusted_auto_still_asks(self):
        io = make_io(trusted=False)
        io.offer_url("https://example.com/docs")
        io.confirm_ask.assert_called_once()


class TestSetupGitAuto(unittest.TestCase):
    def test_auto_creates_repo_without_asking(self):
        with IgnorantTemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                io = make_io(root=tmp)
                git_root = setup_git(None, io, auto=True)
            finally:
                os.chdir(cwd)
            io.confirm_ask.assert_not_called()
            self.assertTrue((Path(tmp) / ".git").exists())
            self.assertEqual(Path(git_root).resolve(), Path(tmp).resolve())

    def test_without_auto_it_asks(self):
        with IgnorantTemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                io = make_io(mode="ask", root=tmp)
                setup_git(None, io)
            finally:
                os.chdir(cwd)
            io.confirm_ask.assert_called_once()
            self.assertFalse((Path(tmp) / ".git").exists())


class TestCoderAutoPrompts(unittest.TestCase):
    def make(self, mode="auto"):
        io = make_io(mode=mode)
        coder = Coder.create(
            Model("gpt-3.5-turbo"), None, io, permission_policy=io.permission_policy
        )
        return coder, io

    def test_check_tokens_over_limit_proceeds_in_auto_mode(self):
        with GitTemporaryDirectory():
            coder, io = self.make()
            coder.main_model.info = {"max_input_tokens": 10}
            self.assertTrue(coder.check_tokens([dict(role="user", content="x " * 100)]))
            io.confirm_ask.assert_not_called()

    def test_check_tokens_over_limit_asks_in_ask_mode(self):
        with GitTemporaryDirectory():
            coder, io = self.make(mode="ask")
            coder.main_model.info = {"max_input_tokens": 10}
            self.assertFalse(coder.check_tokens([dict(role="user", content="x " * 100)]))
            io.confirm_ask.assert_called_once()

    def test_add_creates_missing_file_without_asking(self):
        with GitTemporaryDirectory():
            coder, io = self.make()
            Commands(io, coder).cmd_add("new_module.py")
            io.confirm_ask.assert_not_called()
            self.assertTrue(Path("new_module.py").exists())
            self.assertIn(str(Path(coder.root) / "new_module.py"), coder.abs_fnames)
