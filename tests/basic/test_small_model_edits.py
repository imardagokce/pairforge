import unittest
from pathlib import Path
from unittest.mock import patch

import git

from aider.coders import Coder
from aider.commands import SwitchCoder
from aider.io import InputOutput
from aider.models import Model
from aider.utils import GitTemporaryDirectory


def _make_coder(model_name, **kwargs):
    return Coder.create(
        main_model=Model(model_name),
        io=InputOutput(yes=True, pretty=False),
        **kwargs,
    )


class TestRepoMapScalesForLocalModels(unittest.TestCase):
    def _repo_map_tokens(self, model_name, **kwargs):
        with GitTemporaryDirectory():
            repo = git.Repo()
            fname = Path("added.txt")
            fname.touch()
            repo.git.add(str(fname))
            repo.git.commit("-m", "init")

            # map_tokens=None is what a caller passes to get the model-based default.
            kwargs.setdefault("map_tokens", None)
            coder = _make_coder(model_name, fnames=[str(fname)], **kwargs)
            self.assertIsNotNone(coder.repo_map)
            return coder.repo_map.max_map_tokens

    def test_local_model_with_32k_window_gets_5_percent(self):
        self.assertEqual(self._repo_map_tokens("ollama_chat/qwen2.5-coder:7b"), 1638)

    def test_small_local_window_is_clamped_to_512(self):
        self.assertEqual(self._repo_map_tokens("ollama_chat/llama3:8b"), 512)

    def test_cloud_model_keeps_1024(self):
        self.assertEqual(self._repo_map_tokens("gpt-4o"), 1024)

    def test_explicit_map_tokens_is_respected(self):
        model = "ollama_chat/qwen2.5-coder:7b"
        self.assertEqual(self._repo_map_tokens(model, map_tokens=2048), 2048)


class TestMalformedEditFallback(unittest.TestCase):
    def _failing_run(self, coder, message="fix it"):
        """Run one user message where every edit application fails to parse."""

        def fake_send(msg):
            coder.apply_updates()
            yield from ()

        with patch.object(coder, "get_edits", side_effect=ValueError("bad edit")):
            with patch.object(coder, "send_message", side_effect=fake_send):
                coder.run_one(message, False)

    def test_second_malformed_edit_switches_to_whole_and_retries(self):
        coder = _make_coder("ollama_chat/qwen2.5-coder:14b", edit_format="diff")
        with self.assertRaises(SwitchCoder) as cm:
            self._failing_run(coder, "fix it")
        self.assertEqual(cm.exception.kwargs["edit_format"], "whole")
        self.assertEqual(cm.exception.retry_message, "fix it")

    def test_cloud_model_never_switches(self):
        coder = _make_coder("gpt-4o", edit_format="diff")
        self._failing_run(coder)  # stops at max_reflections, no SwitchCoder

    def test_first_malformed_edit_does_not_switch(self):
        coder = _make_coder("ollama_chat/qwen2.5-coder:14b", edit_format="diff")
        coder.init_before_message()
        with patch.object(coder, "get_edits", side_effect=ValueError("bad edit")):
            coder.apply_updates()
        self.assertIsNotNone(coder.reflected_message)

    def test_whole_format_never_switches(self):
        coder = _make_coder("ollama_chat/qwen2.5-coder:14b", edit_format="whole")
        self._failing_run(coder)

    def test_fallback_happens_only_once_per_session(self):
        io = InputOutput(yes=True, pretty=False)
        first = Coder.create(
            main_model=Model("ollama_chat/qwen2.5-coder:14b"), edit_format="diff", io=io
        )
        with self.assertRaises(SwitchCoder):
            self._failing_run(first)

        second = Coder.create(
            main_model=Model("ollama_chat/qwen2.5-coder:14b"), edit_format="diff", io=io
        )
        self._failing_run(second)  # must not switch again


if __name__ == "__main__":
    unittest.main()
