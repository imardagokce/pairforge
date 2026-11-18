import os
import unittest
from unittest import mock

import requests

from aider.commands import Commands
from aider.io import InputOutput
from aider.local_models import LocalModelError, list_ollama_models


def _fake_response(status=200, payload=None, json_error=None):
    resp = mock.Mock()
    resp.status_code = status
    if json_error is not None:
        resp.json.side_effect = json_error
    else:
        resp.json.return_value = payload
    return resp


class TestListOllamaModels(unittest.TestCase):
    def setUp(self):
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()
        os.environ.pop("OLLAMA_API_BASE", None)

    def tearDown(self):
        self._env.stop()

    def test_parses_normal_response(self):
        payload = {
            "models": [
                {"name": "llama3:latest", "size": 4661224676},
                {"name": "qwen2.5-coder:7b", "size": 1073741824},
            ]
        }
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload=payload)
            result = list_ollama_models()

        get.assert_called_once()
        self.assertEqual(get.call_args[0][0], "http://127.0.0.1:11434/api/tags")
        self.assertEqual(
            result,
            [
                {"name": "llama3:latest", "size_gb": 4.3},
                {"name": "qwen2.5-coder:7b", "size_gb": 1.0},
            ],
        )

    def test_empty_list(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload={"models": []})
            self.assertEqual(list_ollama_models(), [])

    def test_trailing_slash_stripped(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload={"models": []})
            list_ollama_models("http://example.local:9999/")

        self.assertEqual(get.call_args[0][0], "http://example.local:9999/api/tags")

    def test_env_var_used_when_no_base_url(self):
        os.environ["OLLAMA_API_BASE"] = "http://remote-host:11434/"
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload={"models": []})
            list_ollama_models()

        self.assertEqual(get.call_args[0][0], "http://remote-host:11434/api/tags")

    def test_connection_error_raises_local_model_error(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.side_effect = requests.ConnectionError("refused")
            with self.assertRaises(LocalModelError) as ctx:
                list_ollama_models("http://127.0.0.1:11434")

        self.assertIn("Could not reach Ollama at http://127.0.0.1:11434", str(ctx.exception))
        self.assertIn("ollama serve", str(ctx.exception))

    def test_bad_json_raises_local_model_error(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(json_error=ValueError("not json"))
            with self.assertRaises(LocalModelError):
                list_ollama_models()


class TestCmdOllama(unittest.TestCase):
    def test_cmd_ollama_prints_models(self):
        io = InputOutput(pretty=False, fancy_input=False, yes=True)
        commands = Commands(io, None)
        found = [{"name": "llama3:latest", "size_gb": 4.3}]

        with mock.patch(
            "aider.commands.list_ollama_models", return_value=found
        ) as lister, mock.patch.object(io, "tool_output") as tool_output:
            commands.cmd_ollama("")

        lister.assert_called_once_with(None)
        printed = [c.args[0] for c in tool_output.call_args_list if c.args]
        self.assertIn("ollama_chat/llama3:latest  (4.3 GB)", printed)
        self.assertIn("Use one with: /model ollama_chat/<name>", printed)


if __name__ == "__main__":
    unittest.main()
