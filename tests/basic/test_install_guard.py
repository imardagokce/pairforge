"""--yes-always must not install packages: a scripted run should never change the environment."""

import unittest
from unittest.mock import patch

from aider.io import InputOutput
from aider.scrape import install_playwright
from aider.utils import check_pip_install_extra


class TestInstallGuard(unittest.TestCase):
    def test_yes_always_does_not_run_pip_install(self):
        io = InputOutput(pretty=False, yes=True)
        with patch("aider.utils.run_install") as run_install:
            result = check_pip_install_extra(
                io, "module_that_does_not_exist_xyz", "Needs an extra", ["some-package"]
            )
        run_install.assert_not_called()
        self.assertFalse(result)

    def test_interactive_yes_still_installs(self):
        io = InputOutput(pretty=False, yes=None)
        with (
            patch.object(io, "prompt_session", None),
            patch("builtins.input", return_value="y"),
            patch("aider.utils.run_install", return_value=(False, "")) as run_install,
        ):
            check_pip_install_extra(
                io, "module_that_does_not_exist_xyz", "Needs an extra", ["some-package"]
            )
        run_install.assert_called_once()

    def test_yes_always_does_not_install_playwright(self):
        io = InputOutput(pretty=False, yes=True)
        with (
            patch("aider.scrape.check_env", return_value=(False, False)),
            patch("aider.utils.run_install") as run_install,
        ):
            self.assertFalse(install_playwright(io))
        run_install.assert_not_called()
