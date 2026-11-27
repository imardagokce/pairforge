import copy
import unittest
from unittest.mock import patch

from aider.models import Model


class TestOllamaNumCtxCap(unittest.TestCase):
    @patch("aider.models.litellm.completion")
    @patch.object(Model, "token_count")
    def test_num_ctx_capped_at_max_input_tokens(self, mock_token_count, mock_completion):
        mock_token_count.return_value = 30000

        model = Model("ollama_chat/qwen2.5-coder:7b")
        self.assertEqual(model.info.get("max_input_tokens"), 32768)

        messages = [{"role": "user", "content": "Hello"}]
        model.send_completion(messages, functions=None, stream=False)

        self.assertEqual(mock_completion.call_args.kwargs["num_ctx"], 32768)

    @patch("aider.models.litellm.completion")
    @patch.object(Model, "token_count")
    def test_num_ctx_not_capped_when_under_max(self, mock_token_count, mock_completion):
        mock_token_count.return_value = 1000

        model = Model("ollama_chat/qwen2.5-coder:7b")

        messages = [{"role": "user", "content": "Hello"}]
        model.send_completion(messages, functions=None, stream=False)

        self.assertEqual(mock_completion.call_args.kwargs["num_ctx"], 1000 * 1.25 + 8192)


class TestNoThinkForLocalQwen3(unittest.TestCase):
    def _send(self, model_name, effort, messages):
        model = Model(model_name)
        model.set_reasoning_effort(effort)
        with patch("aider.models.litellm.completion") as mock_completion:
            model.send_completion(messages, functions=None, stream=False)
        return mock_completion.call_args.kwargs["messages"]

    def test_low_effort_appends_no_think_to_last_user_message(self):
        messages = [
            {"role": "user", "content": "first"},
            {"role": "assistant", "content": "ok"},
            {"role": "user", "content": "thanks"},
        ]
        sent = self._send("ollama_chat/qwen3:8b", "low", messages)

        self.assertEqual(sent[-1]["content"], "thanks /no_think")
        self.assertEqual(sent[0]["content"], "first")

    def test_auto_low_effort_appends_no_think(self):
        model = Model("ollama_chat/qwen3:8b")
        model.set_reasoning_effort("auto")
        model.accepts_settings = ["reasoning_effort"]
        messages = [{"role": "user", "content": "thanks"}]

        with patch("aider.models.choose_reasoning_effort", return_value="low"):
            model.apply_auto_reasoning_effort("thanks")
        with patch("aider.models.litellm.completion") as mock_completion:
            model.send_completion(messages, functions=None, stream=False)

        sent = mock_completion.call_args.kwargs["messages"]
        self.assertEqual(sent[-1]["content"], "thanks /no_think")

    def test_medium_effort_unchanged(self):
        messages = [{"role": "user", "content": "thanks"}]
        sent = self._send("ollama_chat/qwen3:8b", "medium", messages)

        self.assertEqual(sent[-1]["content"], "thanks")

    def test_non_qwen3_local_model_unchanged(self):
        messages = [{"role": "user", "content": "thanks"}]
        sent = self._send("ollama_chat/llama3.2:3b", "low", messages)

        self.assertEqual(sent[-1]["content"], "thanks")

    def test_caller_messages_not_mutated(self):
        messages = [{"role": "user", "content": "thanks"}]
        original = copy.deepcopy(messages)
        sent = self._send("ollama_chat/qwen3:8b", "low", messages)

        self.assertEqual(messages, original)
        self.assertEqual(sent[-1]["content"], "thanks /no_think")

    def test_non_string_content_unchanged(self):
        content = [{"type": "text", "text": "thanks"}]
        messages = [{"role": "user", "content": content}]
        sent = self._send("ollama_chat/qwen3:8b", "low", messages)

        self.assertEqual(sent[-1]["content"], [{"type": "text", "text": "thanks"}])


if __name__ == "__main__":
    unittest.main()
