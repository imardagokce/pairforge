import unittest
from unittest.mock import MagicMock

from aider.coders import Coder
from aider.io import InputOutput
from aider.local_models import is_small_local_model
from aider.models import Model

SMALL = "ollama_chat/qwen2.5-coder:7b"
LARGE = "ollama_chat/qwen2.5-coder:32b"


def fake_token_count(messages):
    """Avoid tokenizer downloads: one token per character of message content."""
    if isinstance(messages, str):
        return len(messages)
    return sum(len(m.get("content") or "") for m in messages)


def make_io():
    io = InputOutput(pretty=False, yes=True)
    io.tool_output = MagicMock()
    io.tool_warning = MagicMock()
    return io


def make_coder(model_name, edit_format, io=None, **kwargs):
    coder = Coder.create(Model(model_name), edit_format, io or make_io(), **kwargs)
    coder.main_model.token_count = fake_token_count
    return coder


def system_text(coder):
    chunks = coder.format_messages()
    return chunks.system[0]["content"]


class TestIsSmallLocalModel(unittest.TestCase):
    def test_small_local_model_is_true(self):
        self.assertTrue(is_small_local_model(SMALL))

    def test_large_local_model_is_false(self):
        self.assertFalse(is_small_local_model(LARGE))

    def test_hosted_model_is_false(self):
        self.assertFalse(is_small_local_model("gpt-4o"))

    def test_unknown_size_is_false(self):
        self.assertFalse(is_small_local_model("ollama_chat/some-model"))

    def test_max_billions_is_respected(self):
        self.assertFalse(is_small_local_model(SMALL, max_billions=5))


class TestCompactPrompts(unittest.TestCase):
    def test_auto_enables_for_small_local_model(self):
        coder = make_coder(SMALL, "whole")
        self.assertTrue(coder.compact_prompts)

    def test_auto_disabled_for_large_local_model(self):
        coder = make_coder(LARGE, "whole")
        self.assertFalse(coder.compact_prompts)

    def test_compact_drops_example_messages(self):
        coder = make_coder(SMALL, "whole")
        chunks = coder.format_messages()
        self.assertEqual(chunks.examples, [])

    def test_compact_system_prompt_is_shorter_and_keeps_reminder(self):
        compact = make_coder(SMALL, "whole", compact_prompts=True)
        full = make_coder(SMALL, "whole", compact_prompts=False)

        compact_sys = system_text(compact)
        full_sys = system_text(full)

        self.assertLess(len(compact_sys), len(full_sys))
        self.assertIn("MUST return the entire content of the updated file", compact_sys)
        self.assertIn("*file listing* format", compact_sys)

    def test_explicit_false_disables_on_small_model(self):
        coder = make_coder(SMALL, "whole", compact_prompts=False)
        self.assertFalse(coder.compact_prompts)
        self.assertTrue(coder.format_messages().examples)

    def test_setting_carries_over_on_format_switch(self):
        coder = make_coder(SMALL, "whole")
        self.assertTrue(coder.compact_prompts)

        new_coder = Coder.create(from_coder=coder, edit_format="diff")
        self.assertEqual(new_coder.edit_format, "diff")
        self.assertTrue(new_coder.compact_prompts)

    def test_editblock_compact_keeps_search_replace_format(self):
        coder = make_coder(SMALL, "diff")
        self.assertTrue(coder.compact_prompts)

        sys_text = system_text(coder)
        self.assertIn("<<<<<<< SEARCH", sys_text)
        self.assertIn("=======", sys_text)
        self.assertIn(">>>>>>> REPLACE", sys_text)
        self.assertIn("*SEARCH/REPLACE block* Rules:", sys_text)
        self.assertEqual(coder.format_messages().examples, [])

    def test_editblock_compact_is_shorter(self):
        compact = make_coder(SMALL, "diff", compact_prompts=True)
        full = make_coder(SMALL, "diff", compact_prompts=False)
        self.assertLess(len(system_text(compact)), len(system_text(full)))


if __name__ == "__main__":
    unittest.main()
