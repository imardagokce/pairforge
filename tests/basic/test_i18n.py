import ast
import os
import string
import unittest
from pathlib import Path
from unittest.mock import patch

from aider import i18n
from aider.locales import tr


def wrapped_messages():
    """Every string literal passed to _() in the aider package."""
    found = set()
    root = Path(i18n.__file__).parent
    for path in root.rglob("*.py"):
        if "locales" in path.parts or "website" in path.parts:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                found.add(node.args[0].value)
    return found


def placeholders(text):
    return {name for _, name, _, _ in string.Formatter().parse(text) if name is not None}


class TestI18n(unittest.TestCase):
    def tearDown(self):
        i18n.set_language("en")

    def test_normalize(self):
        for value in ("tr", "tr_TR.UTF-8", "Turkish", "TR"):
            self.assertEqual(i18n.normalize(value), "tr")
        for value in ("en_US", "de_DE", "", None):
            self.assertEqual(i18n.normalize(value), "en")

    def test_detect_prefers_explicit_then_env_then_system(self):
        with patch.dict(os.environ, {"PAIRFORGE_LANG": "tr"}):
            self.assertEqual(i18n.detect_language("en"), "en")
            self.assertEqual(i18n.detect_language(), "tr")
        with patch.dict(os.environ, {"PAIRFORGE_LANG": "", "LC_ALL": "tr_TR.UTF-8"}):
            self.assertEqual(i18n.detect_language(), "tr")

    def test_translate_and_fallback(self):
        i18n.set_language("tr")
        some_key = next(iter(tr.MESSAGES))
        self.assertEqual(i18n._(some_key), tr.MESSAGES[some_key])
        self.assertEqual(i18n._("No translation for this one"), "No translation for this one")
        i18n.set_language("en")
        self.assertEqual(i18n._(some_key), some_key)

    def test_catalog_keeps_placeholders(self):
        for english, turkish in tr.MESSAGES.items():
            with self.subTest(english=english):
                self.assertEqual(placeholders(english), placeholders(turkish))

    def test_every_wrapped_message_has_a_turkish_translation(self):
        missing = sorted(wrapped_messages() - set(tr.MESSAGES))
        self.assertEqual(missing, [], "add these to aider/locales/tr.py")

    def test_no_stale_catalog_entries(self):
        stale = sorted(set(tr.MESSAGES) - wrapped_messages())
        self.assertEqual(stale, [], "remove these from aider/locales/tr.py or wrap them with _()")


class TestConfirmAskTurkish(unittest.TestCase):
    def tearDown(self):
        i18n.set_language("en")

    def ask(self, answer, **kwargs):
        from aider.io import InputOutput

        io = InputOutput(pretty=False, fancy_input=False)
        prompts = []

        def fake_input(question):
            prompts.append(question)
            return answer

        with patch("builtins.input", fake_input):
            result = io.confirm_ask("Dosya eklensin mi?", **kwargs)
        return result, prompts[0]

    def test_turkish_labels_and_answers(self):
        i18n.set_language("tr")
        result, prompt = self.ask("e")
        self.assertTrue(result)
        self.assertIn("(E)vet/(H)ayır", prompt)
        self.assertIn("[Evet]", prompt)
        self.assertFalse(self.ask("h")[0])
        self.assertFalse(self.ask("hayır")[0])
        self.assertTrue(self.ask("y")[0])

    def test_turkish_never_ask_again(self):
        i18n.set_language("tr")
        result, prompt = self.ask("b", allow_never=True)
        self.assertFalse(result)
        self.assertIn("(B)ir daha sorma", prompt)

    def test_english_unchanged(self):
        result, prompt = self.ask("y")
        self.assertTrue(result)
        self.assertIn("(Y)es/(N)o", prompt)
        self.assertFalse(self.ask("n")[0])
