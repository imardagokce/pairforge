import unittest
from unittest.mock import MagicMock, patch

from aider.coders import Coder
from aider.history import ChatSummary
from aider.io import InputOutput
from aider.models import Model


def fake_token_count(messages):
    """One token per character of message content, so sizes are easy to reason about."""
    if isinstance(messages, str):
        return len(messages)
    return sum(len(m.get("content") or "") for m in messages)


class TestCompactForContext(unittest.TestCase):
    def make_coder(self, window=1000, auto_compact_at=75):
        io = InputOutput(pretty=False, yes=True)
        io.tool_output = MagicMock()
        io.tool_warning = MagicMock()
        coder = Coder.create(Model("gpt-3.5-turbo"), None, io, auto_compact_at=auto_compact_at)
        coder.main_model.info = {"max_input_tokens": window} if window else {}
        coder.main_model.token_count = fake_token_count
        coder.summarizer = MagicMock()
        coder.summarizer.summarize.return_value = [
            dict(role="user", content="S" * 50),
            dict(role="assistant", content="Ok."),
        ]
        return coder

    def history(self, size):
        return [dict(role="user", content="h" * size), dict(role="assistant", content="ok")]

    def prompt(self, coder, other):
        return [dict(role="system", content="x" * other)] + coder.done_messages

    def test_below_threshold_does_nothing(self):
        coder = self.make_coder()
        coder.done_messages = self.history(300)
        self.assertFalse(coder.compact_for_context(self.prompt(coder, 100)))
        coder.summarizer.summarize.assert_not_called()

    def test_above_threshold_summarizes_history_to_remaining_budget(self):
        coder = self.make_coder()
        coder.done_messages = self.history(600)
        # total 902 > 750; other = 300, so history must fit in 750 - 300 = 450
        self.assertTrue(coder.compact_for_context(self.prompt(coder, 300)))

        args, kwargs = coder.summarizer.summarize.call_args
        self.assertEqual(kwargs["max_tokens"], 450)
        self.assertEqual(coder.done_messages[0]["content"], "S" * 50)
        notice = " ".join(c.args[0] for c in coder.io.tool_output.call_args_list)
        self.assertIn("summarized", notice)

    def test_zero_disables(self):
        coder = self.make_coder(auto_compact_at=0)
        coder.done_messages = self.history(900)
        self.assertFalse(coder.compact_for_context(self.prompt(coder, 300)))
        coder.summarizer.summarize.assert_not_called()

    def test_unknown_context_window_does_nothing(self):
        coder = self.make_coder(window=None)
        coder.done_messages = self.history(900)
        self.assertFalse(coder.compact_for_context(self.prompt(coder, 300)))

    def test_empty_history_does_nothing(self):
        coder = self.make_coder()
        coder.done_messages = []
        self.assertFalse(coder.compact_for_context(self.prompt(coder, 900)))
        coder.summarizer.summarize.assert_not_called()

    def test_history_already_within_floor_is_left_alone(self):
        coder = self.make_coder()
        coder.done_messages = self.history(100)
        # files alone overflow the limit; summarizing 102 tokens of history cannot help
        self.assertFalse(coder.compact_for_context(self.prompt(coder, 900)))
        coder.summarizer.summarize.assert_not_called()

    def test_summarizer_failure_warns_and_keeps_history(self):
        coder = self.make_coder()
        coder.done_messages = self.history(600)
        original = list(coder.done_messages)
        coder.summarizer.summarize.side_effect = ValueError("model down")
        self.assertFalse(coder.compact_for_context(self.prompt(coder, 300)))
        self.assertEqual(coder.done_messages, original)
        coder.io.tool_warning.assert_called_once()

    def test_send_message_rebuilds_prompt_after_compacting(self):
        coder = self.make_coder()
        with (
            patch.object(coder, "compact_for_context", return_value=True) as compact,
            patch.object(coder, "format_messages", wraps=coder.format_messages) as fmt,
            patch.object(coder, "check_tokens", return_value=False),
        ):
            list(coder.send_message("hi"))
        compact.assert_called_once()
        self.assertEqual(fmt.call_count, 2)

    def test_setting_carries_across_coder_switch(self):
        coder = self.make_coder(auto_compact_at=60)
        switched = Coder.create(from_coder=coder, edit_format="ask")
        self.assertEqual(switched.auto_compact_at, 60)


class TestChatSummaryMaxTokensOverride(unittest.TestCase):
    def test_override_is_used_and_restored(self):
        model = MagicMock()
        model.token_count = fake_token_count
        model.info = {"max_input_tokens": 4096}
        summary = ChatSummary([model], max_tokens=1000)
        seen = []

        def fake_real(messages, depth=0):
            seen.append(summary.max_tokens)
            return messages

        summary.summarize_real = fake_real
        summary.summarize([dict(role="user", content="a")], max_tokens=200)
        self.assertEqual(seen, [200])
        self.assertEqual(summary.max_tokens, 1000)


class TestCompactReviewFixes(TestCompactForContext):
    def test_zero_token_count_falls_back_to_estimate(self):
        coder = self.make_coder()
        coder.main_model.token_count = lambda m: 0 if isinstance(m, list) else len(m)
        coder.done_messages = self.history(4000)
        self.assertTrue(coder.compact_for_context(self.prompt(coder, 300)))
        coder.summarizer.summarize.assert_called_once()

    def test_summary_that_is_not_smaller_is_discarded(self):
        coder = self.make_coder()
        coder.done_messages = self.history(600)
        original = list(coder.done_messages)
        coder.summarizer.summarize.return_value = [dict(role="user", content="L" * 900)]
        self.assertFalse(coder.compact_for_context(self.prompt(coder, 300)))
        self.assertEqual(coder.done_messages, original)
        coder.io.tool_warning.assert_called_once()
