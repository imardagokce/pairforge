import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import git

from aider.coders import Coder
from aider.io import InputOutput
from aider.models import Model
from aider.permissions import PermissionPolicy
from aider.utils import GitTemporaryDirectory


def big_python_source(functions=60):
    body = "\n".join(f"    total = total + {i}" for i in range(12))
    return "\n\n".join(
        f"def func_{n}(value):\n    total = value\n{body}\n    return total"
        for n in range(functions)
    )


class TestLargeFileOutline(unittest.TestCase):
    def setUp(self):
        self.model = Model("gpt-3.5-turbo")

    def make_coder(self, mode="auto", window=2000):
        io = InputOutput(pretty=False, yes=True)
        io.confirm_ask = MagicMock(return_value=False)
        io.tool_output = MagicMock()
        policy = PermissionPolicy(mode, True, Path.cwd())
        coder = Coder.create(self.model, None, io, permission_policy=policy, map_tokens=0)
        coder.main_model.info = {"max_input_tokens": window}
        return coder, io

    def commit(self, name, text):
        Path(name).write_text(text)
        repo = git.Repo()
        repo.git.add(name)
        repo.git.commit("-m", "init")

    def test_user_mention_of_large_file_sends_outline_without_asking(self):
        with GitTemporaryDirectory():
            self.commit("big.py", big_python_source())
            coder, io = self.make_coder()

            inp = coder.preproc_user_input("Please explain big.py")

            io.confirm_ask.assert_not_called()
            self.assertEqual(coder.abs_fnames, set())
            self.assertIn("def func_0(value):", inp)
            self.assertIn("/add big.py", inp)
            self.assertTrue(inp.startswith("Please explain big.py"))

    def test_reply_mention_of_large_file_returns_outline(self):
        with GitTemporaryDirectory():
            self.commit("big.py", big_python_source())
            coder, io = self.make_coder()

            message = coder.check_for_file_mentions("We should change big.py")

            io.confirm_ask.assert_not_called()
            self.assertIn("def func_0(value):", message)
            self.assertIn("big.py", coder.ignore_mentions)

    def test_outline_is_trimmed_to_budget(self):
        with GitTemporaryDirectory():
            self.commit("big.py", big_python_source())
            coder, io = self.make_coder(window=400)

            outline = coder.large_file_outline("big.py", max_tokens=100)

            self.assertIsNotNone(outline)
            self.assertLessEqual(coder.main_model.token_count(outline), 100)
            self.assertIn("def func_0(value):", outline)
            self.assertIn("more", outline)

    def test_file_without_outline_still_asks(self):
        with GitTemporaryDirectory():
            self.commit("big.txt", "word " * 5000)
            coder, io = self.make_coder()

            coder.check_for_file_mentions("Please look at big.txt")

            io.confirm_ask.assert_called()
            self.assertEqual(io.confirm_ask.call_args[0][0], "Add file to the chat?")

    def test_ask_mode_still_asks_for_large_file(self):
        with GitTemporaryDirectory():
            self.commit("big.py", big_python_source())
            coder, io = self.make_coder(mode="ask")

            coder.check_for_file_mentions("Please look at big.py")

            io.confirm_ask.assert_called()

    def test_small_file_is_still_added_in_full(self):
        with GitTemporaryDirectory():
            self.commit("small.py", "def tiny():\n    return 1\n")
            coder, io = self.make_coder()

            coder.check_for_file_mentions("Please look at small.py")

            self.assertIn(str(Path(coder.root) / "small.py"), coder.abs_fnames)

    def test_outline_budget_is_much_smaller_than_add_limit(self):
        with GitTemporaryDirectory():
            self.commit("big.py", big_python_source(functions=400))
            for window, expected in ((2000, 256), (100000, 1500), (20000, 1000)):
                coder, io = self.make_coder(window=window)
                with patch.object(coder, "large_file_outline", return_value="x") as outline:
                    coder.check_for_file_mentions("Please explain big.py")
                self.assertEqual(outline.call_args.kwargs["max_tokens"], expected)

    def test_repomap_failure_gives_no_outline(self):
        with GitTemporaryDirectory():
            self.commit("big.py", big_python_source())
            coder, io = self.make_coder()
            with patch("aider.repomap.RepoMap", side_effect=RuntimeError("no tags")):
                self.assertIsNone(coder.large_file_outline("big.py", max_tokens=500))
