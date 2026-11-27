import unittest

from aider.local_models import local_model_preset
from aider.models import Model


class TestLocalModelPreset(unittest.TestCase):
    def test_qwen_coder_small_uses_whole_format(self):
        preset = local_model_preset("ollama_chat/qwen2.5-coder:7b")
        self.assertEqual(preset["family"], "qwen2.5-coder")
        self.assertEqual(preset["max_input_tokens"], 32768)
        self.assertEqual(preset["edit_format"], "whole")
        self.assertTrue(preset["use_repo_map"])
        self.assertNotIn("reasoning_tag", preset)

    def test_qwen_coder_large_uses_diff_format(self):
        preset = local_model_preset("ollama_chat/qwen2.5-coder:32b")
        self.assertEqual(preset["edit_format"], "diff")

    def test_qwen3_has_think_reasoning_tag(self):
        preset = local_model_preset("ollama_chat/qwen3.5:4b")
        self.assertEqual(preset["family"], "qwen3")
        self.assertEqual(preset["reasoning_tag"], "think")

    def test_llama32_context(self):
        preset = local_model_preset("ollama/llama3.2:3b")
        self.assertEqual(preset["max_input_tokens"], 131072)

    def test_plain_llama3_context(self):
        preset = local_model_preset("ollama/llama3:8b")
        self.assertEqual(preset["family"], "llama3")
        self.assertEqual(preset["max_input_tokens"], 8192)

    def test_lm_studio_phi4_is_diff_with_16k_context(self):
        preset = local_model_preset("lm_studio/phi4:14b")
        self.assertEqual(preset["max_input_tokens"], 16384)
        self.assertEqual(preset["edit_format"], "diff")

    def test_deepseek_r1_has_think_reasoning_tag(self):
        preset = local_model_preset("ollama_chat/deepseek-r1:8b")
        self.assertEqual(preset["reasoning_tag"], "think")

    def test_max_output_tokens_capped_at_quarter_of_context(self):
        preset = local_model_preset("ollama/phi3:3.8b")
        self.assertEqual(preset["max_input_tokens"], 4096)
        self.assertEqual(preset["max_output_tokens"], 1024)

    def test_max_output_tokens_default_8192_for_large_context(self):
        preset = local_model_preset("ollama/llama3.1:8b")
        self.assertEqual(preset["max_output_tokens"], 8192)

    def test_unknown_family_returns_none(self):
        self.assertIsNone(local_model_preset("ollama/foo:7b"))

    def test_non_local_names_return_none(self):
        self.assertIsNone(local_model_preset("gpt-4o"))
        self.assertIsNone(local_model_preset("openrouter/qwen/qwen-2.5-coder-32b-instruct"))


class TestLocalPresetModelIntegration(unittest.TestCase):
    def test_model_gets_preset_settings(self):
        model = Model("ollama_chat/qwen2.5-coder:7b")
        self.assertEqual(model.edit_format, "whole")
        self.assertTrue(model.use_repo_map)
        self.assertEqual(model.info["max_input_tokens"], 32768)
        self.assertEqual(model.max_chat_history_tokens, 2048)

    def test_model_gets_reasoning_tag_from_preset(self):
        model = Model("ollama_chat/deepseek-r1:8b")
        self.assertEqual(model.reasoning_tag, "think")

    def test_non_local_model_has_no_preset(self):
        self.assertIsNone(local_model_preset("gpt-4o"))
