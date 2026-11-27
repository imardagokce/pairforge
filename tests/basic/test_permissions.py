import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import git

from aider.coders import Coder
from aider.commands import Commands
from aider.io import InputOutput
from aider.models import Model
from aider.permissions import (
    PermissionPolicy,
    decline,
    is_declined,
    is_trusted,
    path_inside,
    trust,
    trusted_entry,
    untrust,
)
from aider.utils import GitTemporaryDirectory


class TrustStoreTestBase(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.trust_file = Path(self.tempdir) / "store" / "trusted_folders.json"
        self.env_patcher = patch.dict(os.environ, {"AIDER_TRUST_FILE": str(self.trust_file)})
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()
        shutil.rmtree(self.tempdir, ignore_errors=True)


class TestTrustStore(TrustStoreTestBase):
    def test_round_trip(self):
        root = Path(self.tempdir) / "project"
        root.mkdir()

        self.assertFalse(is_trusted(root))
        self.assertFalse(is_declined(root))

        trust(root)

        self.assertTrue(is_trusted(root))
        self.assertFalse(is_declined(root))
        self.assertTrue(self.trust_file.exists())
        data = json.loads(self.trust_file.read_text(encoding="utf-8"))
        self.assertIn(str(root.resolve()), data["trusted"])

    def test_corrupt_file_is_treated_as_empty(self):
        root = Path(self.tempdir) / "project"
        root.mkdir()
        self.trust_file.parent.mkdir(parents=True)
        self.trust_file.write_text("{not json", encoding="utf-8")

        self.assertFalse(is_trusted(root))
        self.assertFalse(is_declined(root))

        trust(root)
        self.assertTrue(is_trusted(root))
        json.loads(self.trust_file.read_text(encoding="utf-8"))

    def test_non_object_json_is_treated_as_empty(self):
        root = Path(self.tempdir) / "project"
        root.mkdir()
        self.trust_file.parent.mkdir(parents=True)
        self.trust_file.write_text("[1, 2]", encoding="utf-8")

        self.assertFalse(is_trusted(root))

    def test_nested_path_is_trusted(self):
        root = Path(self.tempdir) / "project"
        nested = root / "sub" / "deeper"
        nested.mkdir(parents=True)
        trust(root)

        self.assertTrue(is_trusted(nested))
        self.assertTrue(is_trusted(root))

    def test_sibling_with_shared_prefix_is_not_trusted(self):
        root = Path(self.tempdir) / "proj"
        sibling = Path(self.tempdir) / "proj2"
        root.mkdir()
        sibling.mkdir()
        trust(root)

        self.assertFalse(is_trusted(sibling))

    def test_declined_is_exact_match(self):
        root = Path(self.tempdir) / "project"
        nested = root / "sub"
        nested.mkdir(parents=True)
        decline(root)

        self.assertTrue(is_declined(root))
        self.assertFalse(is_declined(nested))
        self.assertFalse(is_trusted(root))

    def test_trust_clears_declined(self):
        root = Path(self.tempdir) / "project"
        root.mkdir()
        decline(root)
        trust(root)

        self.assertTrue(is_trusted(root))
        self.assertFalse(is_declined(root))

    def test_untrust_removes_entry_and_declines(self):
        root = Path(self.tempdir) / "project"
        other = Path(self.tempdir) / "other"
        root.mkdir()
        other.mkdir()
        trust(root)
        trust(other)
        untrust(root)

        self.assertFalse(is_trusted(root))
        self.assertTrue(is_declined(root))
        self.assertTrue(is_trusted(other))

    def test_trusted_entry_names_the_matching_parent(self):
        root = Path(self.tempdir) / "project"
        nested = root / "sub"
        nested.mkdir(parents=True)
        self.assertIsNone(trusted_entry(nested))

        trust(root)
        self.assertEqual(trusted_entry(nested), str(root.resolve()))

    def test_path_inside(self):
        root = Path(self.tempdir) / "project"
        self.assertTrue(path_inside(root, root))
        self.assertTrue(path_inside(root, root / "a" / "b.txt"))
        self.assertFalse(path_inside(root, Path(self.tempdir) / "project2"))
        self.assertFalse(path_inside(root, Path(self.tempdir)))


class TestPermissionPolicy(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.root = Path(self.tempdir) / "project"
        self.root.mkdir()

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_auto_allows_matrix(self):
        inside = self.root / "file.txt"
        outside = Path(self.tempdir) / "other.txt"

        cases = [
            ("ask", True, inside, False),
            ("auto", False, inside, False),
            ("auto", True, outside, False),
            ("auto", True, inside, True),
            ("auto", True, self.root / "new" / "nested.txt", True),
        ]
        for mode, trusted, path, expected in cases:
            with self.subTest(mode=mode, trusted=trusted, path=str(path)):
                policy = PermissionPolicy(mode, trusted, self.root)
                self.assertEqual(policy.auto_allows(path), expected)

    def test_auto_allows_action_ignores_path(self):
        self.assertTrue(PermissionPolicy("auto", True, self.root).auto_allows_action())
        self.assertFalse(PermissionPolicy("ask", True, self.root).auto_allows_action())
        self.assertFalse(PermissionPolicy("auto", False, self.root).auto_allows_action())

    def test_attributes(self):
        policy = PermissionPolicy("auto", True, self.root)
        self.assertEqual(policy.mode, "auto")
        self.assertTrue(policy.trusted)
        self.assertEqual(policy.root, self.root.resolve())


class TestPermissionsCommand(TrustStoreTestBase):
    def make_commands(self, policy_mode=None, trusted=False):
        io = InputOutput(pretty=False, yes=True)
        coder = Coder.create(Model("gpt-3.5-turbo"), None, io)
        if policy_mode is not None:
            coder.permission_policy = PermissionPolicy(policy_mode, trusted, coder.root)
        commands = Commands(io, coder)
        io.tool_output = MagicMock()
        io.tool_error = MagicMock()
        io.tool_warning = MagicMock()
        return commands, coder, io

    def test_show_without_policy(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands()
            commands.cmd_permissions("")

            io.tool_output.assert_any_call("Permission mode: ask")
            self.assertIsNone(coder.permission_policy)

    def test_show_with_policy(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands("auto", True)
            commands.cmd_permissions("")

            io.tool_output.assert_any_call("Permission mode: auto")
            io.tool_output.assert_any_call("Trusted: True")

    def test_set_auto_in_trusted_folder(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands("ask", True)
            commands.cmd_permissions("auto")

            self.assertEqual(coder.permission_policy.mode, "auto")
            self.assertTrue(coder.permission_policy.auto_allows_action())
            io.tool_warning.assert_not_called()

    def test_set_auto_in_untrusted_folder_warns_and_does_not_trust(self):
        with GitTemporaryDirectory() as tmp:
            commands, coder, io = self.make_commands("ask", False)
            commands.cmd_permissions("auto")

            self.assertEqual(coder.permission_policy.mode, "auto")
            self.assertFalse(coder.permission_policy.trusted)
            self.assertFalse(coder.permission_policy.auto_allows_action())
            io.tool_warning.assert_called_once()
            self.assertIn("trusted folders", io.tool_warning.call_args[0][0])
            self.assertFalse(self.trust_file.exists())
            self.assertFalse(is_trusted(tmp))

    def test_set_creates_policy_when_missing(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands()
            commands.cmd_permissions("auto")

            self.assertIsNotNone(coder.permission_policy)
            self.assertEqual(coder.permission_policy.mode, "auto")
            self.assertFalse(coder.permission_policy.trusted)

    def test_set_ask(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands("auto", True)
            commands.cmd_permissions("ask")

            self.assertEqual(coder.permission_policy.mode, "ask")

    def test_invalid_value_shows_usage(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands("ask", True)
            commands.cmd_permissions("bogus")

            io.tool_error.assert_called_once()
            self.assertIn("/permissions [ask|auto|trust|untrust]", io.tool_error.call_args[0][0])
            self.assertEqual(coder.permission_policy.mode, "ask")

    def test_trust_trusts_root_and_enables_auto(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands("auto", False)
            decline(coder.root)
            commands.cmd_permissions("trust")

            self.assertTrue(coder.permission_policy.trusted)
            self.assertTrue(coder.permission_policy.auto_allows_action())
            self.assertTrue(is_trusted(coder.root))
            self.assertFalse(is_declined(coder.root))

    def test_trust_creates_policy_when_missing(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands()
            commands.cmd_permissions("trust")

            self.assertIsNotNone(coder.permission_policy)
            self.assertEqual(coder.permission_policy.mode, "ask")
            self.assertTrue(coder.permission_policy.trusted)

    def test_untrust_removes_trust_and_marks_declined(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands("auto", True)
            trust(coder.root)
            commands.cmd_permissions("untrust")

            self.assertFalse(coder.permission_policy.trusted)
            self.assertFalse(coder.permission_policy.auto_allows_action())
            self.assertFalse(is_trusted(coder.root))
            self.assertTrue(is_declined(coder.root))
            io.tool_warning.assert_not_called()

    def test_untrust_warns_when_parent_is_trusted(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands("auto", True)
            parent = Path(coder.root).resolve().parent
            trust(parent)
            commands.cmd_permissions("untrust")

            self.assertTrue(coder.permission_policy.trusted)
            io.tool_warning.assert_called_once()
            self.assertIn(str(parent), io.tool_warning.call_args[0][0])

    def test_completions(self):
        with GitTemporaryDirectory():
            commands, coder, io = self.make_commands()
            self.assertEqual(
                sorted(commands.completions_permissions()), ["ask", "auto", "trust", "untrust"]
            )


class TestCoderPermissions(unittest.TestCase):
    def setUp(self):
        self.GPT35 = Model("gpt-3.5-turbo")

    def make_coder(self, mode, trusted):
        io = InputOutput(pretty=False, yes=True)
        io.confirm_ask = MagicMock(return_value=True)
        policy = PermissionPolicy(mode, trusted, Path.cwd())
        coder = Coder.create(self.GPT35, None, io, permission_policy=policy)
        return coder, io

    def commit_files(self, *names):
        repo = git.Repo()
        for name in names:
            Path(name).write_text("content\n")
            repo.git.add(name)
        repo.git.commit("-m", "init")

    def test_auto_adds_small_mentioned_file_without_asking(self):
        with GitTemporaryDirectory():
            self.commit_files("small.txt")
            coder, io = self.make_coder("auto", True)

            coder.check_for_file_mentions("Please look at small.txt")

            io.confirm_ask.assert_not_called()
            self.assertIn(str(Path(coder.root) / "small.txt"), coder.abs_fnames)

    def test_large_mentioned_file_still_asks(self):
        with GitTemporaryDirectory():
            self.commit_files("big.txt")
            coder, io = self.make_coder("auto", True)
            io.confirm_ask = MagicMock(return_value=False)
            with patch.object(coder.main_model, "token_count", return_value=10**6):
                coder.check_for_file_mentions("Please look at big.txt")

            io.confirm_ask.assert_called()
            self.assertEqual(io.confirm_ask.call_args[0][0], "Add file to the chat?")
            self.assertEqual(coder.abs_fnames, set())

    def test_ask_mode_still_asks(self):
        with GitTemporaryDirectory():
            self.commit_files("small.txt")
            coder, io = self.make_coder("ask", True)

            coder.check_for_file_mentions("Please look at small.txt")

            io.confirm_ask.assert_called()
            self.assertEqual(io.confirm_ask.call_args[0][0], "Add file to the chat?")

    def test_untrusted_auto_still_asks(self):
        with GitTemporaryDirectory():
            self.commit_files("small.txt")
            coder, io = self.make_coder("auto", False)

            coder.check_for_file_mentions("Please look at small.txt")

            io.confirm_ask.assert_called()

    def test_create_new_file_skips_prompt_in_auto_trusted(self):
        with GitTemporaryDirectory():
            self.commit_files("init.txt")
            coder, io = self.make_coder("auto", True)

            self.assertTrue(coder.allowed_to_edit("new.txt"))

            io.confirm_ask.assert_not_called()
            self.assertTrue((Path(coder.root) / "new.txt").exists())

    def test_create_new_file_asks_in_ask_mode(self):
        with GitTemporaryDirectory():
            self.commit_files("init.txt")
            coder, io = self.make_coder("ask", True)
            io.confirm_ask = MagicMock(return_value=False)

            self.assertFalse(coder.allowed_to_edit("new.txt"))

            io.confirm_ask.assert_called_once()
            self.assertEqual(io.confirm_ask.call_args[0][0], "Create new file?")
            self.assertFalse((Path(coder.root) / "new.txt").exists())

    def test_edit_unadded_file_skips_prompt_in_auto_trusted(self):
        with GitTemporaryDirectory():
            self.commit_files("other.txt")
            coder, io = self.make_coder("auto", True)

            self.assertTrue(coder.allowed_to_edit("other.txt"))

            io.confirm_ask.assert_not_called()
            self.assertIn(str(Path(coder.root) / "other.txt"), coder.abs_fnames)

    def test_shell_command_runs_without_asking_in_auto_trusted(self):
        with GitTemporaryDirectory():
            self.commit_files("init.txt")
            coder, io = self.make_coder("auto", True)

            with patch("aider.coders.base_coder.run_cmd", return_value=(0, "hi\n")) as run:
                coder.handle_shell_commands("echo hi", None)

            run.assert_called_once()
            io.confirm_ask.assert_not_called()

    def test_shell_command_asks_in_ask_mode(self):
        with GitTemporaryDirectory():
            self.commit_files("init.txt")
            coder, io = self.make_coder("ask", True)
            io.confirm_ask = MagicMock(return_value=False)

            with patch("aider.coders.base_coder.run_cmd", return_value=(0, "hi\n")) as run:
                coder.handle_shell_commands("echo hi", None)

            run.assert_not_called()
            self.assertEqual(io.confirm_ask.call_args[0][0], "Run shell command?")

    def test_shell_command_asks_in_untrusted_auto(self):
        with GitTemporaryDirectory():
            self.commit_files("init.txt")
            coder, io = self.make_coder("auto", False)
            io.confirm_ask = MagicMock(return_value=False)

            with patch("aider.coders.base_coder.run_cmd", return_value=(0, "hi\n")) as run:
                coder.handle_shell_commands("echo hi", None)

            run.assert_not_called()
            self.assertEqual(io.confirm_ask.call_args[0][0], "Run shell command?")


class TestPolicyCarriesAcrossSwitch(unittest.TestCase):
    def test_from_coder_keeps_policy(self):
        with GitTemporaryDirectory():
            io = InputOutput(pretty=False, yes=True)
            policy = PermissionPolicy("auto", True, Path.cwd())
            first = Coder.create(Model("gpt-3.5-turbo"), None, io, permission_policy=policy)
            second = Coder.create(io=io, from_coder=first)

            self.assertIs(second.permission_policy, policy)


if __name__ == "__main__":
    unittest.main()
