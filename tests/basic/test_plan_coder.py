from unittest import TestCase, mock

from aider.coders import Coder
from aider.coders.plan_coder import MAX_PLAN_STEPS, parse_plan_steps, run_plan
from aider.commands import Commands


def make_coder(auto=False):
    coder = mock.MagicMock()
    coder.main_model.editor_model = None
    coder.main_model.editor_edit_format = "whole"
    coder.total_cost = 0
    coder.aider_commit_hashes = set()
    coder.auto_approved.return_value = auto
    coder.io = mock.MagicMock()
    coder.io.confirm_ask.return_value = True
    return coder


def make_create(plan_text, editors):
    """Fake Coder.create: the planner returns plan_text, each editor is recorded in editors."""

    def create(**kwargs):
        if kwargs.get("edit_format") == "plan":
            planner = mock.MagicMock()
            planner.run.return_value = plan_text
            return planner
        editor = mock.MagicMock()
        editors.append(editor)
        return editor

    return create


class TestParsePlanSteps(TestCase):
    def test_numbered_steps_and_other_text_ignored(self):
        text = "Here is the plan:\n1. a\n2) b\n- not a step\n3. c\nThanks"
        self.assertEqual(parse_plan_steps(text), ["a", "b", "c"])

    def test_caps_at_eight_steps(self):
        text = "\n".join(f"{i}. step {i}" for i in range(1, 12))
        steps = parse_plan_steps(text)
        self.assertEqual(MAX_PLAN_STEPS, 8)
        self.assertEqual(len(steps), 8)
        self.assertEqual(steps[0], "step 1")
        self.assertEqual(steps[-1], "step 8")

    def test_empty_text_has_no_steps(self):
        self.assertEqual(parse_plan_steps(""), [])
        self.assertEqual(parse_plan_steps(None), [])


class TestRunPlan(TestCase):
    plan_text = "1. Add helper in aider/utils.py\n2. Wire it in aider/commands.py\n3. Add tests"

    def test_auto_approved_runs_each_step_without_asking(self):
        coder = make_coder(auto=True)
        editors = []
        with mock.patch.object(Coder, "create", side_effect=make_create(self.plan_text, editors)):
            ok = run_plan(coder, "add a helper")

        self.assertTrue(ok)
        coder.io.confirm_ask.assert_not_called()
        coder.auto_approved.assert_called_once_with("run the 3-step plan")
        self.assertEqual(len(editors), 3)
        steps = ["Add helper in aider/utils.py", "Wire it in aider/commands.py", "Add tests"]
        for i, (editor, step) in enumerate(zip(editors, steps), 1):
            editor.run.assert_called_once()
            message = editor.run.call_args.kwargs["with_message"]
            self.assertIn(step, message)
            self.assertIn(f"ONLY step {i}", message)
            self.assertIn(self.plan_text.splitlines()[0], message)

    def test_ask_mode_confirms_once_and_decline_runs_nothing(self):
        coder = make_coder(auto=False)
        coder.io.confirm_ask.return_value = False
        editors = []
        with mock.patch.object(Coder, "create", side_effect=make_create(self.plan_text, editors)):
            ok = run_plan(coder, "add a helper")

        self.assertFalse(ok)
        coder.io.confirm_ask.assert_called_once_with("Run this plan?")
        self.assertEqual(editors, [])

    def test_ask_mode_accept_runs_steps(self):
        coder = make_coder(auto=False)
        editors = []
        with mock.patch.object(Coder, "create", side_effect=make_create(self.plan_text, editors)):
            run_plan(coder, "add a helper")

        coder.io.confirm_ask.assert_called_once_with("Run this plan?")
        self.assertEqual(len(editors), 3)

    def test_empty_plan_prints_message_and_runs_nothing(self):
        coder = make_coder(auto=True)
        editors = []
        with mock.patch.object(
            Coder, "create", side_effect=make_create("Sorry, no idea.", editors)
        ):
            ok = run_plan(coder, "do something")

        self.assertFalse(ok)
        self.assertEqual(editors, [])
        coder.io.tool_warning.assert_called_once()
        coder.io.confirm_ask.assert_not_called()


class TestCmdPlan(TestCase):
    def test_slash_plan_without_args_prints_usage(self):
        io = mock.MagicMock()
        coder = make_coder()
        commands = Commands(io, coder)
        with mock.patch.object(Coder, "create") as create:
            commands.cmd_plan("")

        create.assert_not_called()
        printed = " ".join(str(c) for c in io.tool_output.call_args_list)
        self.assertIn("Usage: /plan <request>", printed)
