<div align="center">

# pairforge

**AI pair programming in your terminal.**
Edit code in your local git repository through a conversation with an LLM.

[![License](https://img.shields.io/github/license/imardagokce/pairforge?style=for-the-badge&color=22d3ee&labelColor=0b1020)](LICENSE.txt)
[![Python](https://img.shields.io/badge/python-3.10%20%E2%80%93%203.14-a78bfa?style=for-the-badge&logo=python&logoColor=white&labelColor=0b1020)](pyproject.toml)
[![Last commit](https://img.shields.io/github/last-commit/imardagokce/pairforge?style=for-the-badge&color=34d399&labelColor=0b1020)](https://github.com/imardagokce/pairforge/commits/main)
[![Stars](https://img.shields.io/github/stars/imardagokce/pairforge?style=for-the-badge&color=fbbf24&labelColor=0b1020&logo=github)](https://github.com/imardagokce/pairforge/stargazers)
[![Issues](https://img.shields.io/github/issues/imardagokce/pairforge?style=for-the-badge&color=f472b6&labelColor=0b1020)](https://github.com/imardagokce/pairforge/issues)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-34d399?style=for-the-badge&labelColor=0b1020)](CONTRIBUTING.md)

[Features](#features) · [Quick start](#quick-start) · [Architecture](#architecture) · [Contributing](#contributing) · [Attribution](#attribution)

</div>

> [!NOTE]
> pairforge is a fork of [Aider-AI/aider](https://github.com/Aider-AI/aider) (Apache-2.0). It is an independent project and is **not** affiliated with or endorsed by the Aider maintainers. The command-line entry point is still `aider`. See [Attribution](#attribution).

---

## Features

| | |
| --- | --- |
| **Any LLM** | Cloud or local models: Claude, GPT, DeepSeek, Gemini, Ollama and more via [LiteLLM](https://github.com/BerriAI/litellm). |
| **Repo map** | Builds a map of your whole codebase so the model works well in larger projects. |
| **Git-native** | Auto-commits every change with a sensible message. Diff, review and undo AI edits with the git tools you already use. |
| **Multiple edit formats** | Edit-block, unified diff, whole-file and patch formats, selected per model. |
| **100+ languages** | Syntax-aware repo mapping through tree-sitter. |
| **Lint and test loop** | Runs your linters and tests after each change and can fix what they report. |
| **IDE friendly** | Ask for changes by adding comments to your code from any editor. |
| **Images and web pages** | Add screenshots and URLs to the chat as context. |
| **Voice-to-code** | Dictate requests and let the model implement them. |

## Quick start

pairforge requires Python 3.10 or newer.

```bash
# 1. Get the code
git clone https://github.com/imardagokce/pairforge.git
cd pairforge

# 2. Install in a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .

# 3. Run it inside the project you want to edit
cd /path/to/your/project
export ANTHROPIC_API_KEY=<key>   # or OPENAI_API_KEY, DEEPSEEK_API_KEY, ...
aider --model sonnet
```

### Local models in one command

Start Ollama, LM Studio or a llama.cpp server, then:

```bash
aider --local                 # picks the best coding model it finds
aider --local qwen2.5-coder:7b
```

`--local` uses the whole edit format (the most reliable one for small models) and the `auto` permission mode, so in a trusted folder it edits files and runs commands without asking each time. Pass `--permission-mode ask` or `--edit-format diff` to override. Inside a session, `/local` lists every model the local servers offer.

### Driving pairforge from another tool

An agent such as Claude Code can plan the work and hand each small step to pairforge, which edits and commits with your local model:

```bash
aider --local --permission-mode ask --yes-always --no-pretty --no-stream \
      --message-file step.md path/to/file.py
```

`--yes-always` accepts edits and new files but always refuses shell commands and package installs, so a scripted run never executes or installs anything. Review each step with `git show HEAD`.

Run `aider --help` for every option. Model, provider and configuration details are covered in the [upstream documentation](https://aider.chat/docs/), which still applies to this codebase.

## Architecture

```mermaid
flowchart LR
  main["main.py<br/>startup and args"] --> Commands["Commands<br/>/slash commands"]
  main --> Coder["Coder<br/>chat loop"]
  Commands --> Coder
  Coder --> Model["Model<br/>settings and metadata"]
  Coder --> IO["InputOutput<br/>terminal I/O"]
  Coder --> Repo["GitRepo<br/>commits and diffs"]
  Coder --> Edit["Edit-format coders<br/>editblock, udiff, wholefile, patch"]
```

| Path | Role |
| --- | --- |
| `aider/main.py` | Argument parsing and startup |
| `aider/coders/` | `Coder` base class and the edit-format implementations |
| `aider/commands.py` | In-chat `/` commands |
| `aider/models.py` | Model definitions and settings |
| `aider/repo.py` | Git integration |
| `aider/io.py` | Terminal input and output |
| `tests/` | Test suite |
| `benchmark/` | Benchmark harness |

## Development

```bash
pip install -r requirements/requirements-dev.txt
pytest
```

## Contributing

Issues and pull requests are welcome. See the [roadmap](ROADMAP.md) for planned work. Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Attribution

pairforge is a modified version of [Aider](https://github.com/Aider-AI/aider), copyright Aider-AI contributors, used under the [Apache License 2.0](LICENSE.txt). Modifications are recorded in the git history, and the required notice is in [NOTICE](NOTICE). "Aider" is the name of the original project and is not claimed by pairforge. The original README is kept in [docs/UPSTREAM_README.md](docs/UPSTREAM_README.md).

## License

Licensed under the [Apache License 2.0](LICENSE.txt).
