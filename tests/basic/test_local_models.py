import os
import unittest
from unittest import mock

import requests

from aider.commands import Commands
from aider.io import InputOutput
from aider.local_models import (
    LocalModelError,
    is_local_url,
    list_ollama_models,
    list_openai_compatible_models,
)


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


class TestListOpenAICompatibleModels(unittest.TestCase):
    def test_parses_normal_response(self):
        payload = {"data": [{"id": "gpt-4o"}, {"id": "claude-3-5-sonnet"}]}
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload=payload)
            result = list_openai_compatible_models("http://localhost:20128/v1")

        self.assertEqual(get.call_args[0][0], "http://localhost:20128/v1/models")
        self.assertEqual(result, ["claude-3-5-sonnet", "gpt-4o"])

    def test_sorted_order(self):
        payload = {"data": [{"id": "z-model"}, {"id": "a-model"}, {"id": "m-model"}]}
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload=payload)
            result = list_openai_compatible_models("http://localhost:20128/v1")

        self.assertEqual(result, ["a-model", "m-model", "z-model"])

    def test_trailing_slash_stripped(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload={"data": []})
            list_openai_compatible_models("http://localhost:20128/v1/")

        self.assertEqual(get.call_args[0][0], "http://localhost:20128/v1/models")

    def test_bearer_header_sent_when_key_given(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload={"data": []})
            list_openai_compatible_models("http://localhost:20128/v1", api_key="secret")

        self.assertEqual(get.call_args.kwargs["headers"], {"Authorization": "Bearer secret"})

    def test_no_auth_header_without_key(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload={"data": []})
            list_openai_compatible_models("http://localhost:20128/v1")

        self.assertNotIn("Authorization", get.call_args.kwargs["headers"])

    def test_401_says_key_rejected(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(status=401, payload={})
            with self.assertRaises(LocalModelError) as ctx:
                list_openai_compatible_models("http://localhost:20128/v1", api_key="bad")

        self.assertIn("API key was rejected", str(ctx.exception))
        self.assertIn("http://localhost:20128/v1/models", str(ctx.exception))

    def test_other_status_raises(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(status=500, payload={})
            with self.assertRaises(LocalModelError) as ctx:
                list_openai_compatible_models("http://localhost:20128/v1")

        self.assertIn("HTTP 500", str(ctx.exception))

    def test_connection_error_raises_local_model_error(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.side_effect = requests.ConnectionError("refused")
            with self.assertRaises(LocalModelError) as ctx:
                list_openai_compatible_models("http://localhost:20128/v1")

        self.assertIn("http://localhost:20128/v1", str(ctx.exception))

    def test_bad_json_raises_local_model_error(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(json_error=ValueError("not json"))
            with self.assertRaises(LocalModelError):
                list_openai_compatible_models("http://localhost:20128/v1")

    def test_missing_data_key_raises_local_model_error(self):
        with mock.patch("aider.local_models.requests.get") as get:
            get.return_value = _fake_response(payload={"models": []})
            with self.assertRaises(LocalModelError):
                list_openai_compatible_models("http://localhost:20128/v1")


class TestIsLocalUrl(unittest.TestCase):
    def test_localhost(self):
        self.assertTrue(is_local_url("http://localhost:20128/v1"))

    def test_ipv4_loopback(self):
        self.assertTrue(is_local_url("http://127.0.0.1:20128/v1"))

    def test_ipv6_loopback(self):
        self.assertTrue(is_local_url("http://[::1]:20128/v1"))

    def test_remote_host_is_not_local(self):
        self.assertFalse(is_local_url("http://gateway.example.com:20128/v1"))

    def test_https_remote_is_not_local(self):
        self.assertFalse(is_local_url("https://gateway.example.com/v1"))

    def test_non_http_scheme_is_not_local(self):
        self.assertFalse(is_local_url("ftp://localhost/v1"))


class TestCmdOmniroute(unittest.TestCase):
    def setUp(self):
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()
        for name in (
            "OMNIROUTE_API_BASE",
            "OMNIROUTE_API_KEY",
            "OPENAI_API_BASE",
            "OPENAI_API_KEY",
        ):
            os.environ.pop(name, None)

    def tearDown(self):
        self._env.stop()

    def test_cmd_omniroute_prints_models(self):
        io = InputOutput(pretty=False, fancy_input=False, yes=True)
        commands = Commands(io, None)

        with mock.patch(
            "aider.commands.list_openai_compatible_models", return_value=["gpt-4o", "qwen"]
        ) as lister, mock.patch.object(io, "tool_output") as tool_output:
            commands.cmd_omniroute("")

        lister.assert_called_once_with("http://localhost:20128/v1", None)
        printed = [c.args[0] for c in tool_output.call_args_list if c.args]
        self.assertIn("openai/gpt-4o", printed)
        self.assertIn("openai/qwen", printed)
        self.assertIn("Use one with: /model openai/<id>", printed)

    def test_cmd_omniroute_uses_env_base_and_key(self):
        os.environ["OMNIROUTE_API_BASE"] = "http://10.0.0.5:20128/v1"
        os.environ["OMNIROUTE_API_KEY"] = "omni-key"
        io = InputOutput(pretty=False, fancy_input=False, yes=True)
        commands = Commands(io, None)

        with mock.patch(
            "aider.commands.list_openai_compatible_models", return_value=[]
        ) as lister, mock.patch.object(io, "tool_output"):
            commands.cmd_omniroute("")

        lister.assert_called_once_with("http://10.0.0.5:20128/v1", "omni-key")

    def test_cmd_omniroute_falls_back_to_openai_base_and_key(self):
        os.environ["OPENAI_API_BASE"] = "http://127.0.0.1:9999/v1"
        os.environ["OPENAI_API_KEY"] = "openai-key"
        io = InputOutput(pretty=False, fancy_input=False, yes=True)
        commands = Commands(io, None)

        with mock.patch(
            "aider.commands.list_openai_compatible_models", return_value=[]
        ) as lister, mock.patch.object(io, "tool_output"):
            commands.cmd_omniroute("")

        lister.assert_called_once_with("http://127.0.0.1:9999/v1", "openai-key")

    def test_cmd_omniroute_argument_wins(self):
        os.environ["OMNIROUTE_API_BASE"] = "http://10.0.0.5:20128/v1"
        io = InputOutput(pretty=False, fancy_input=False, yes=True)
        commands = Commands(io, None)

        with mock.patch(
            "aider.commands.list_openai_compatible_models", return_value=[]
        ) as lister, mock.patch.object(io, "tool_output"):
            commands.cmd_omniroute("http://192.168.1.2:20128/v1")

        lister.assert_called_once_with("http://192.168.1.2:20128/v1", None)

    def test_cmd_omniroute_empty_list(self):
        io = InputOutput(pretty=False, fancy_input=False, yes=True)
        commands = Commands(io, None)

        with mock.patch(
            "aider.commands.list_openai_compatible_models", return_value=[]
        ), mock.patch.object(io, "tool_output") as tool_output:
            commands.cmd_omniroute("")

        printed = [c.args[0] for c in tool_output.call_args_list if c.args]
        self.assertTrue(any("No models are available" in p for p in printed))

    def test_cmd_omniroute_reports_error(self):
        io = InputOutput(pretty=False, fancy_input=False, yes=True)
        commands = Commands(io, None)

        with mock.patch(
            "aider.commands.list_openai_compatible_models",
            side_effect=LocalModelError("boom"),
        ), mock.patch.object(io, "tool_error") as tool_error:
            commands.cmd_omniroute("")

        tool_error.assert_called_once_with("boom")


if __name__ == "__main__":
    unittest.main()
