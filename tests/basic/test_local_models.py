import os
import unittest
from unittest import mock

import requests

from aider.commands import Commands
from aider.io import InputOutput
from aider import models
from aider.local_models import (
    LocalModelError,
    apply_local_quickstart,
    choose_local_model,
    discover_local_servers,
    list_ollama_models,
    list_openai_compatible_models,
)
from aider.models import ModelSettings


def _ollama(models_and_sizes):
    return {
        "name": "Ollama",
        "base_url": "http://127.0.0.1:11434",
        "models": [name for name, _ in models_and_sizes],
        "sizes": dict(models_and_sizes),
    }


def _args(**overrides):
    values = dict(local="", model=None, edit_format=None, permission_mode=None)
    values.update(overrides)
    return mock.Mock(spec=list(values), **values)


class TestChooseLocalModel(unittest.TestCase):
    def test_prefers_coder_model_over_bigger_general_model(self):
        servers = [_ollama([("ollama_chat/llama3:70b", 40.0), ("ollama_chat/qwen-coder:7b", 4.0)])]
        model, server = choose_local_model(servers)
        self.assertEqual(model, "ollama_chat/qwen-coder:7b")
        self.assertEqual(server["name"], "Ollama")

    def test_picks_largest_when_no_coder_model(self):
        servers = [_ollama([("ollama_chat/small:1b", 1.0), ("ollama_chat/big:8b", 5.0)])]
        model, _ = choose_local_model(servers)
        self.assertEqual(model, "ollama_chat/big:8b")

    def test_wanted_name_matches_without_prefix(self):
        servers = [
            _ollama([("ollama_chat/qwen-coder:7b", 4.0), ("ollama_chat/qwen3.5:4b", 3.0)])
        ]
        model, _ = choose_local_model(servers, "qwen3.5:4b")
        self.assertEqual(model, "ollama_chat/qwen3.5:4b")

    def test_wanted_name_not_found_lists_available(self):
        servers = [_ollama([("ollama_chat/qwen-coder:7b", 4.0)])]
        with self.assertRaises(LocalModelError) as ctx:
            choose_local_model(servers, "missing-model")
        self.assertIn("missing-model", str(ctx.exception))
        self.assertIn("ollama_chat/qwen-coder:7b", str(ctx.exception))

    def test_no_servers_raises(self):
        with self.assertRaises(LocalModelError) as ctx:
            choose_local_model([])
        self.assertIn("No local model servers", str(ctx.exception))

    def test_servers_without_models_raise(self):
        with self.assertRaises(LocalModelError) as ctx:
            choose_local_model([_ollama([])])
        self.assertIn("no models", str(ctx.exception))


class TestApplyLocalQuickstart(unittest.TestCase):
    def setUp(self):
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()
        for name in ("LM_STUDIO_API_BASE", "OPENAI_API_BASE"):
            os.environ.pop(name, None)
        self.io = mock.Mock()
        self.servers = [_ollama([("ollama_chat/qwen-coder:7b", 4.0)])]

    def tearDown(self):
        self._env.stop()

    def run_quickstart(self, args, servers=None):
        servers = self.servers if servers is None else servers
        return apply_local_quickstart(args, self.io, discover=lambda: servers)

    def test_without_local_flag_changes_nothing(self):
        args = _args(local=None)
        discover = mock.Mock()
        self.assertTrue(apply_local_quickstart(args, self.io, discover=discover))
        discover.assert_not_called()
        self.assertIsNone(args.model)
        self.assertIsNone(args.edit_format)
        self.assertIsNone(args.permission_mode)

    def test_sets_model_whole_format_and_auto_permissions(self):
        args = _args()
        self.assertTrue(self.run_quickstart(args))
        self.assertEqual(args.model, "ollama_chat/qwen-coder:7b")
        self.assertEqual(args.edit_format, "whole")
        self.assertEqual(args.permission_mode, "auto")

    def test_named_model_is_used(self):
        servers = [_ollama([("ollama_chat/qwen-coder:7b", 4.0), ("ollama_chat/phi4:14b", 9.0)])]
        args = _args(local="phi4:14b")
        self.assertTrue(self.run_quickstart(args, servers))
        self.assertEqual(args.model, "ollama_chat/phi4:14b")

    def test_explicit_permission_mode_is_kept(self):
        args = _args(permission_mode="ask")
        self.run_quickstart(args)
        self.assertEqual(args.permission_mode, "ask")

    def test_explicit_edit_format_is_kept(self):
        args = _args(edit_format="diff")
        self.run_quickstart(args)
        self.assertEqual(args.edit_format, "diff")

    def test_known_model_keeps_its_own_edit_format(self):
        known = ModelSettings(name="ollama_chat/qwen-coder:7b", edit_format="diff")
        with mock.patch.object(models, "MODEL_SETTINGS", [known]):
            args = _args()
            self.run_quickstart(args)
        self.assertIsNone(args.edit_format)

    def test_explicit_model_skips_discovery(self):
        args = _args(model="ollama_chat/mine")
        discover = mock.Mock()
        self.assertTrue(apply_local_quickstart(args, self.io, discover=discover))
        discover.assert_not_called()
        self.assertEqual(args.model, "ollama_chat/mine")
        self.assertEqual(args.edit_format, "whole")
        self.assertEqual(args.permission_mode, "auto")

    def test_lm_studio_sets_api_base(self):
        servers = [
            {"name": "LM Studio", "base_url": "http://127.0.0.1:1234/v1", "models": ["lm_studio/q"]}
        ]
        args = _args()
        self.run_quickstart(args, servers)
        self.assertEqual(os.environ["LM_STUDIO_API_BASE"], "http://127.0.0.1:1234/v1")

    def test_llama_cpp_sets_openai_api_base(self):
        servers = [
            {"name": "llama.cpp", "base_url": "http://127.0.0.1:8080/v1", "models": ["openai/m"]}
        ]
        args = _args()
        self.run_quickstart(args, servers)
        self.assertEqual(args.model, "openai/m")
        self.assertEqual(os.environ["OPENAI_API_BASE"], "http://127.0.0.1:8080/v1")

    def test_nothing_found_reports_error_and_returns_false(self):
        args = _args()
        self.assertFalse(self.run_quickstart(args, []))
        self.io.tool_error.assert_called_once()
        self.assertIsNone(args.model)


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


def _fake_get_by_port(responses):
    """Return a requests.get replacement that answers by URL prefix, else refuses."""

    def fake_get(url, **kwargs):
        for prefix, resp in responses.items():
            if url.startswith(prefix):
                return resp
        raise requests.ConnectionError("refused")

    return fake_get


class TestDiscoverLocalServers(unittest.TestCase):
    def setUp(self):
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()
        for name in ("OLLAMA_API_BASE", "LM_STUDIO_API_BASE", "LLAMA_CPP_API_BASE"):
            os.environ.pop(name, None)

    def tearDown(self):
        self._env.stop()

    def test_nothing_running(self):
        with mock.patch("aider.local_models.requests.get", side_effect=_fake_get_by_port({})):
            self.assertEqual(discover_local_servers(), [])

    def test_all_three_running(self):
        responses = {
            "http://127.0.0.1:11434": _fake_response(
                payload={"models": [{"name": "llama3:latest", "size": 0}]}
            ),
            "http://127.0.0.1:1234": _fake_response(payload={"data": [{"id": "qwen-7b"}]}),
            "http://127.0.0.1:8080": _fake_response(payload={"data": [{"id": "gguf-model"}]}),
        }
        with mock.patch(
            "aider.local_models.requests.get", side_effect=_fake_get_by_port(responses)
        ):
            servers = discover_local_servers()

        by_name = {s["name"]: s for s in servers}
        self.assertEqual([s["name"] for s in servers], ["Ollama", "LM Studio", "llama.cpp"])
        self.assertEqual(by_name["Ollama"]["models"], ["ollama_chat/llama3:latest"])
        self.assertEqual(by_name["LM Studio"]["models"], ["lm_studio/qwen-7b"])
        self.assertEqual(by_name["LM Studio"]["base_url"], "http://127.0.0.1:1234/v1")
        self.assertEqual(by_name["llama.cpp"]["models"], ["openai/gguf-model"])
        self.assertEqual(by_name["llama.cpp"]["base_url"], "http://127.0.0.1:8080/v1")

    def test_unrelated_server_on_port_is_skipped(self):
        responses = {"http://127.0.0.1:8080": _fake_response(json_error=ValueError("html"))}
        with mock.patch(
            "aider.local_models.requests.get", side_effect=_fake_get_by_port(responses)
        ):
            self.assertEqual(discover_local_servers(), [])

    def test_env_overrides_addresses(self):
        os.environ["LM_STUDIO_API_BASE"] = "http://box:5555/v1/"
        os.environ["LLAMA_CPP_API_BASE"] = "http://box:6666/v1"
        responses = {
            "http://box:5555/v1/models": _fake_response(payload={"data": [{"id": "a"}]}),
            "http://box:6666/v1/models": _fake_response(payload={"data": [{"id": "b"}]}),
        }
        with mock.patch(
            "aider.local_models.requests.get", side_effect=_fake_get_by_port(responses)
        ):
            servers = discover_local_servers()

        self.assertEqual(
            [(s["name"], s["base_url"]) for s in servers],
            [("LM Studio", "http://box:5555/v1"), ("llama.cpp", "http://box:6666/v1")],
        )


class TestCmdLocal(unittest.TestCase):
    def setUp(self):
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()
        os.environ.pop("LM_STUDIO_API_BASE", None)
        self.io = InputOutput(pretty=False, fancy_input=False, yes=True)
        self.commands = Commands(self.io, None)

    def tearDown(self):
        self._env.stop()

    def run_local(self, servers):
        with mock.patch(
            "aider.commands.discover_local_servers", return_value=servers
        ), mock.patch.object(self.io, "tool_output") as tool_output:
            self.commands.cmd_local("")
        return [c.args[0] for c in tool_output.call_args_list if c.args]

    def test_none_found_lists_probed_addresses(self):
        printed = self.run_local([])
        text = "\n".join(printed)
        self.assertIn("No local model servers found", text)
        self.assertIn("11434", text)
        self.assertIn("1234", text)
        self.assertIn("8080", text)

    def test_lm_studio_sets_api_base_for_session(self):
        servers = [
            {"name": "LM Studio", "base_url": "http://127.0.0.1:1234/v1", "models": ["lm_studio/q"]}
        ]
        printed = self.run_local(servers)

        self.assertIn("lm_studio/q", printed)
        self.assertEqual(os.environ["LM_STUDIO_API_BASE"], "http://127.0.0.1:1234/v1")

    def test_lm_studio_keeps_existing_api_base(self):
        os.environ["LM_STUDIO_API_BASE"] = "http://other:1/v1"
        servers = [
            {"name": "LM Studio", "base_url": "http://127.0.0.1:1234/v1", "models": ["lm_studio/q"]}
        ]
        self.run_local(servers)
        self.assertEqual(os.environ["LM_STUDIO_API_BASE"], "http://other:1/v1")

    def test_llama_cpp_hints_openai_api_base_without_setting_it(self):
        os.environ.pop("OPENAI_API_BASE", None)
        servers = [
            {"name": "llama.cpp", "base_url": "http://127.0.0.1:8080/v1", "models": ["openai/m"]}
        ]
        printed = self.run_local(servers)

        self.assertIn("openai/m", printed)
        self.assertTrue(any("OPENAI_API_BASE=http://127.0.0.1:8080/v1" in p for p in printed))
        self.assertNotIn("OPENAI_API_BASE", os.environ)


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
