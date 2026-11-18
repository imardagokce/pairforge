import unittest

from aider.effort import AUTO, choose_reasoning_effort
from aider.models import Model


class TestChooseReasoningEffort(unittest.TestCase):
    def test_auto_constant(self):
        self.assertEqual(AUTO, "auto")

    def test_high_word_triggers_high(self):
        self.assertEqual(choose_reasoning_effort("Please review the architecture"), "high")

    def test_each_high_word(self):
        for word in [
            "architecture",
            "redesign",
            "refactor",
            "race condition",
            "deadlock",
            "concurrency",
            "performance",
            "optimize",
            "debug",
            "root cause",
            "security",
            "migrate",
            "algorithm",
            "prove",
            "design",
        ]:
            with self.subTest(word=word):
                self.assertEqual(choose_reasoning_effort(f"look at the {word} now"), "high")

    def test_high_word_case_insensitive(self):
        self.assertEqual(choose_reasoning_effort("ARCHITECTURE question"), "high")
        self.assertEqual(choose_reasoning_effort("Race Condition in queue"), "high")

    def test_high_word_whole_word_only(self):
        # "designs" and "debugging" are not whole-word matches for "design"/"debug"
        self.assertNotEqual(choose_reasoning_effort("designs"), "high")
        self.assertEqual(choose_reasoning_effort("the debugging session " + "y" * 80), "medium")

    def test_phrase_matches_across_whitespace(self):
        self.assertEqual(choose_reasoning_effort("a race\ncondition here"), "high")

    def test_length_boundary_600_is_not_high(self):
        self.assertEqual(choose_reasoning_effort("x" * 600), "medium")

    def test_length_boundary_601_is_high(self):
        self.assertEqual(choose_reasoning_effort("x" * 601), "high")

    def test_short_message_is_low(self):
        self.assertEqual(choose_reasoning_effort("x" * 79), "low")

    def test_length_boundary_80_is_medium(self):
        self.assertEqual(choose_reasoning_effort("x" * 80), "medium")

    def test_low_word_short(self):
        self.assertEqual(choose_reasoning_effort("fix the typo in readme"), "low")

    def test_each_low_word(self):
        for word in [
            "typo",
            "rename",
            "comment",
            "docstring",
            "format",
            "formatting",
            "lint",
            "whitespace",
        ]:
            with self.subTest(word=word):
                # Pad to 80+ chars so only the low-word rule can make it low
                msg = f"please {word} this function " + "y" * 80
                self.assertEqual(choose_reasoning_effort(msg), "low")

    def test_low_word_case_insensitive(self):
        msg = "Rename the variable " + "y" * 80
        self.assertEqual(choose_reasoning_effort(msg), "low")

    def test_low_word_whole_word_only(self):
        # "information" contains "format" but is not a whole-word match
        msg = "Tell me more information about the request " + "y" * 80
        self.assertEqual(choose_reasoning_effort(msg), "medium")

    def test_low_word_length_boundary_299_is_low(self):
        msg = "fix the typo " + "y" * (299 - len("fix the typo "))
        self.assertEqual(len(msg), 299)
        self.assertEqual(choose_reasoning_effort(msg), "low")

    def test_low_word_length_boundary_300_is_medium(self):
        msg = "fix the typo " + "y" * (300 - len("fix the typo "))
        self.assertEqual(len(msg), 300)
        self.assertEqual(choose_reasoning_effort(msg), "medium")

    def test_high_word_beats_low_word(self):
        self.assertEqual(choose_reasoning_effort("fix the typo in the design"), "high")

    def test_high_length_beats_low_word(self):
        msg = "fix the typo " + "y" * 600
        self.assertEqual(choose_reasoning_effort(msg), "high")

    def test_medium_default(self):
        msg = "Please add a helper function that parses the config file " + "y" * 40
        self.assertGreaterEqual(len(msg), 80)
        self.assertEqual(choose_reasoning_effort(msg), "medium")

    def test_empty_message_is_low(self):
        self.assertEqual(choose_reasoning_effort(""), "low")


class TestModelAutoReasoningEffort(unittest.TestCase):
    def make_model(self, accepts=True):
        model = Model("gpt-4o")
        if accepts:
            model.accepts_settings = ["reasoning_effort"]
        return model

    def test_set_auto_turns_on_flag_without_api_value(self):
        model = self.make_model()
        model.set_reasoning_effort("auto")
        self.assertTrue(model.auto_reasoning_effort)
        self.assertIsNone(model.last_auto_effort)
        self.assertIsNone(model.extra_params)
        self.assertEqual(model.get_reasoning_effort(), "auto")

    def test_set_auto_case_insensitive(self):
        model = self.make_model()
        model.set_reasoning_effort("AUTO")
        self.assertTrue(model.auto_reasoning_effort)

    def test_set_concrete_value_turns_flag_off(self):
        model = self.make_model()
        model.set_reasoning_effort("auto")
        model.set_reasoning_effort("medium")
        self.assertFalse(model.auto_reasoning_effort)
        self.assertEqual(model.get_reasoning_effort(), "medium")

    def test_concrete_value_unchanged_behaviour(self):
        model = self.make_model()
        model.set_reasoning_effort("high")
        self.assertFalse(model.auto_reasoning_effort)
        self.assertEqual(model.extra_params, {"extra_body": {"reasoning_effort": "high"}})
        self.assertEqual(model.get_reasoning_effort(), "high")

    def test_apply_writes_level_and_keeps_auto(self):
        model = self.make_model()
        model.set_reasoning_effort("auto")
        level = model.apply_auto_reasoning_effort("typo in readme")
        self.assertEqual(level, "low")
        self.assertTrue(model.auto_reasoning_effort)
        self.assertEqual(model.last_auto_effort, "low")
        self.assertEqual(model.extra_params["extra_body"]["reasoning_effort"], "low")
        self.assertEqual(model.get_reasoning_effort(), "low")

    def test_apply_updates_per_message(self):
        model = self.make_model()
        model.set_reasoning_effort("auto")
        self.assertEqual(model.apply_auto_reasoning_effort("fix the typo"), "low")
        self.assertEqual(model.apply_auto_reasoning_effort("debug the crash"), "high")
        self.assertEqual(model.last_auto_effort, "high")
        self.assertEqual(model.extra_params["extra_body"]["reasoning_effort"], "high")

    def test_apply_openrouter_format(self):
        model = Model("openrouter/openai/gpt-4o")
        model.accepts_settings = ["reasoning_effort"]
        model.set_reasoning_effort("auto")
        self.assertEqual(model.apply_auto_reasoning_effort("debug the crash"), "high")
        self.assertEqual(model.extra_params["extra_body"]["reasoning"], {"effort": "high"})

    def test_apply_noop_when_auto_off(self):
        model = self.make_model()
        model.set_reasoning_effort("medium")
        self.assertIsNone(model.apply_auto_reasoning_effort("debug the crash"))
        self.assertIsNone(model.last_auto_effort)
        self.assertEqual(model.get_reasoning_effort(), "medium")

    def test_apply_noop_when_model_does_not_accept(self):
        model = self.make_model(accepts=False)
        model.set_reasoning_effort("auto")
        self.assertIsNone(model.apply_auto_reasoning_effort("debug the crash"))
        self.assertIsNone(model.last_auto_effort)
        self.assertIsNone(model.extra_params)


if __name__ == "__main__":
    unittest.main()
