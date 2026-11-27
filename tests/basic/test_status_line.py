import os
import subprocess
from unittest import TestCase
from unittest.mock import patch

from prompt_toolkit.input import DummyInput
from prompt_toolkit.output import DummyOutput

from aider.coders import Coder
from aider.io import InputOutput
from aider.main import main
from aider.models import AUTO, Model, default_reasoning_effort
from aider.utils import GitTemporaryDirectory, IgnorantTemporaryDirectory


def _commit_file(name="f.txt", content="one\n"):
    with open(name, "w") as f:
        f.write(content)
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@example.com")
    env.update(GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@example.com")
    subprocess.run(["git", "add", name], check=True, env=env)
    subprocess.run(["git", "commit", "-q", "-m", "init"], check=True, env=env)


class TestDefaultReasoningEffort(TestCase):
    def test_model_accepting_reasoning_effort_gets_auto(self):
        model = Model("gpt-4o")
        model.accepts_settings = ["reasoning_effort"]
        self.assertEqual(default_reasoning_effort(model), AUTO)

    def test_model_without_setting_support_gets_none(self):
        model = Model("gpt-4o")
        model.accepts_settings = []
        self.assertIsNone(default_reasoning_effort(model))

    def test_gpt4o_matches_its_accepts_settings(self):
        model = Model("gpt-4o")
        expected = AUTO if "reasoning_effort" in (model.accepts_settings or []) else None
        self.assertEqual(default_reasoning_effort(model), expected)

    def test_local_thinking_model_gets_auto(self):
        self.assertEqual(default_reasoning_effort(Model("ollama_chat/qwen3:8b")), AUTO)

    def test_local_non_thinking_model_gets_none(self):
        self.assertIsNone(default_reasoning_effort(Model("ollama_chat/qwen2.5-coder:7b")))

    def test_explicit_reasoning_effort_is_not_overridden(self):
        coder = main(
            [
                "--model",
                "o3-mini",
                "--reasoning-effort",
                "low",
                "--exit",
                "--yes",
                "--no-git",
            ],
            input=DummyInput(),
            output=DummyOutput(),
            return_coder=True,
        )
        self.assertEqual(coder.main_model.get_reasoning_effort(), "low")
        self.assertFalse(coder.main_model.auto_reasoning_effort)

    def test_default_auto_applied_by_main(self):
        coder = main(
            ["--model", "ollama_chat/qwen3:8b", "--exit", "--yes", "--no-git"],
            input=DummyInput(),
            output=DummyOutput(),
            return_coder=True,
        )
        self.assertTrue(coder.main_model.auto_reasoning_effort)


class TestStatusLine(TestCase):
    def test_status_line_in_git_repo(self):
        with GitTemporaryDirectory():
            _commit_file()
            io = InputOutput(yes=True)
            coder = Coder.create(main_model=Model("gpt-4o"), io=io)
            branch = coder.repo.repo.active_branch.name

            line = coder.status_line()
            self.assertIn("gpt-4o", line)
            self.assertIn("ctx", line)
            self.assertIn(f"git {branch}", line)
            self.assertNotIn("*", line)

            with open("f.txt", "w") as f:
                f.write("changed\n")
            line = coder.status_line()
            self.assertIn(f"git {branch}*", line)

    def test_context_shows_ratio_when_window_known(self):
        with GitTemporaryDirectory():
            _commit_file()
            coder = Coder.create(main_model=Model("gpt-4o"), io=InputOutput(yes=True))
            coder.main_model.info["max_input_tokens"] = 32000
            line = coder.status_line()
            self.assertIn("/", line)
            self.assertIn("%", line)

    def test_no_git_part_without_repo(self):
        with IgnorantTemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                coder = Coder.create(
                    main_model=Model("gpt-4o"), io=InputOutput(yes=True), use_git=False
                )
                self.assertIsNone(coder.repo)
                line = coder.status_line()
                self.assertIn("gpt-4o", line)
                self.assertNotIn("git", line)
            finally:
                os.chdir(cwd)

    def test_effort_auto_shows_chosen_level(self):
        with GitTemporaryDirectory():
            _commit_file()
            coder = Coder.create(main_model=Model("gpt-4o"), io=InputOutput(yes=True))
            coder.main_model.set_reasoning_effort(AUTO)
            coder.main_model.last_auto_effort = "low"
            self.assertIn("effort auto:low", coder.status_line())

    def test_effort_omitted_when_unset(self):
        with GitTemporaryDirectory():
            _commit_file()
            coder = Coder.create(main_model=Model("gpt-4o"), io=InputOutput(yes=True))
            self.assertNotIn("effort", coder.status_line())

    def test_status_line_toolbar_passed_to_io(self):
        with GitTemporaryDirectory():
            _commit_file()
            coder = Coder.create(
                main_model=Model("gpt-4o"), io=InputOutput(yes=True), status_line=True
            )
            with patch.object(coder.io, "get_input", return_value="x") as mock_get:
                coder.get_input()
            self.assertIn("status_line", mock_get.call_args.kwargs)
            self.assertIn("gpt-4o", mock_get.call_args.kwargs["status_line"])

    def test_status_line_disabled_passes_no_toolbar(self):
        with GitTemporaryDirectory():
            _commit_file()
            coder = Coder.create(
                main_model=Model("gpt-4o"), io=InputOutput(yes=True), status_line=False
            )
            with patch.object(coder.io, "get_input", return_value="x") as mock_get:
                coder.get_input()
            self.assertIsNone(mock_get.call_args.kwargs.get("status_line"))


class TestLocalThinkingAutoEffort(TestCase):
    """auto effort must reach /no_think and the status line for local qwen3."""

    def test_auto_low_on_local_qwen3_is_kept_and_reported(self):
        from aider.models import Model

        model = Model("ollama_chat/qwen3:8b")
        model.set_reasoning_effort("auto")
        with patch("aider.models.choose_reasoning_effort", return_value="low"):
            self.assertEqual(model.apply_auto_reasoning_effort("hi"), "low")
        self.assertEqual(model.get_reasoning_effort(), "low")
        self.assertNotIn("reasoning_effort", str(model.extra_params or {}))

    def test_auto_low_adds_no_think_to_request(self):
        from aider.models import Model

        model = Model("ollama_chat/qwen3:8b")
        model.set_reasoning_effort("auto")
        with patch("aider.models.choose_reasoning_effort", return_value="low"):
            model.apply_auto_reasoning_effort("rename x to y")
        with patch("aider.models.litellm.completion") as completion:
            model.send_completion([dict(role="user", content="rename x")], None, False)
        sent = completion.call_args.kwargs["messages"]
        self.assertTrue(sent[-1]["content"].endswith("/no_think"))
