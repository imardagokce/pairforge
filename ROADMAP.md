# Roadmap

pairforge is an independent project derived from [Aider](https://github.com/Aider-AI/aider). This roadmap lists what we plan to change, add and remove. It is a plan, not a promise: items move as we learn more. Status values are **Planned**, **In progress** and **Done**.

## Starting point

What the inherited codebase already provides (found by mapping the source), so we extend it rather than rewrite it:

| Area | What exists today | Where |
| --- | --- | --- |
| Chat history compaction | `ChatSummary` summarizes older messages when history exceeds `--max-chat-history-tokens` | `aider/history.py` |
| Reasoning effort | `--reasoning-effort` flag and `/reasoning-effort` command, set manually | `aider/args.py`, `aider/commands.py` |
| Local models | Ollama detection (`Model.is_ollama`) and generic model settings through LiteLLM | `aider/models.py` |
| Response language | `--chat-language` makes the model answer in a chosen language | `aider/args.py`, `aider/coders/base_coder.py` |
| Terminal UI | `prompt_toolkit` input and `rich` output | `aider/io.py` |

## Milestones

### 1. Local models made easy
**Goal:** running a locally hosted model should take one command, not manual configuration.
- [x] Discover running local servers (Ollama, LM Studio, llama.cpp server) and list their models. **Done** (`/local` checks all three at once; `/ollama` still lists Ollama alone)
- [x] `--local [MODEL]` quick start: finds a local server, prefers coding models, then the largest, uses the whole edit format for models without known settings, and turns on `auto` permission mode unless told otherwise. The Ollama context size was already set per request (`num_ctx`). **Done**
- [x] Per-model presets for common local models (context window, edit format, token limits). **Done** (`ollama/`, `ollama_chat/` and `lm_studio/` names of qwen, deepseek, llama, gemma, phi, mistral and codellama families: context window when the model has no known info, diff for 14B and up, whole below, `think` reasoning tag for qwen3 and deepseek-r1)
- [ ] Clear, actionable errors when the server is down or the context window is too small. **Planned**

### 2. Automatic compaction
**Goal:** long sessions stay usable without the user managing context.
- [x] Trigger compaction automatically at a configurable fraction of the context window, instead of only at a fixed history token limit. **Done** (`--auto-compact-at PERCENT`, default 75: before each send, if the whole prompt passes that share of the window, the history is summarized to the room left)
- [x] A manual `/compact` command, plus a visible notice of what was summarized. **Done**
- [x] `/autocompact [N | N% | default]` to set the auto-summarize threshold during a session. **Done**
- [ ] Keep recent turns and file edits verbatim; summarize only older discussion. **Planned**
- [ ] Tests covering summary quality limits and token accounting. **Planned**

### 3. Automatic effort level
**Goal:** the tool chooses how much reasoning a task needs.
- [x] An `auto` value for `--reasoning-effort` that selects low, medium or high per message with a local heuristic (no extra LLM call). **Done**
- [x] Respect models that do not support the parameter (no error). **Done**
- [x] Effort chosen per model by default: `auto` for models that accept a reasoning effort and for local thinking models, unless `--reasoning-effort` is given. **Done**
- [x] Show the chosen level in the status line. **Done**
- [ ] Allow an override per message. **In progress** (a line is printed when the level changes; per-message override is still to do)

### 4. Language support
**Goal:** a first-class experience in more languages.
- [x] Localizable interface strings: `_()` in `aider/i18n.py` with catalogs in `aider/locales`; messages, yes/no questions and `/help` command descriptions. Prompts to the model stay English. **Done**
- [x] Turkish as the first additional interface language (`--ui-language tr`, `PAIRFORGE_LANG` or the system language); yes/no questions accept (E)vet/(H)ayır. **Done**
- [x] Make the response language follow the interface language by default, with `--chat-language` as an override. **Done**

### 5. Terminal interface
**Goal:** a polished, consistent and pleasant terminal experience.
- [ ] A design pass: color theme, spacing and consistent message styles (user, assistant, tool, error). **Planned**
- [ ] Better diff and edit presentation. **Planned**
- [x] A status line under the prompt showing model, context usage, effort and git state (`--no-status-line` turns it off). **Done**
- [ ] Accessible themes (light, dark, high contrast) and a no-color mode. **Planned**

### 6. Feature pruning
**Goal:** remove what we do not use so the codebase is smaller and easier to change.
- [x] Audit features and decide what to keep (candidates: voice input, GUI mode, analytics, benchmark harness, website assets). Removed: GUI mode, voice input, benchmark harness. Analytics is now a no-op stub (pairforge collects nothing). Website assets are kept. **Done**
- [x] Remove each item in its own change with tests updated. Removed in separate commits: the browser GUI (`--gui`/`--browser`, streamlit), `/voice` and its voice arguments, the benchmark harness (`benchmark/`), and analytics (the analytics arguments, the opt-in prompt and the posthog/mixpanel calls). `aider/analytics.py` is now a no-op `Analytics` class with the same interface, so call sites are unchanged. **Done**
- [x] Drop unused dependencies as features go. Removed from the requirements: streamlit (with altair, blinker, cachetools, narwhals, pyarrow, pydeck, toml, tornado), pydub (with audioop-lts on Python 3.13+), sounddevice and soundfile (with cffi and pycparser), posthog and mixpanel (with asgiref, python-dateutil and six), and the dev dependencies lox and imgcat. Also removed the `browser` extra and the pydub requirements file. **Done**

### 7. Project identity
**Goal:** make pairforge a clearly separate product.
- [x] Command and distribution renamed: `pairforge` is the command (`aider` kept as an alias), the distribution is `pairforge`. The import package stays `aider` so upstream fixes still cherry-pick cleanly. **Done**
- [x] Update documentation, badges and entry points to match. **Done**
- [ ] Keep `LICENSE.txt`, `NOTICE` and attribution to the original project intact. **Planned**

### 8. Fewer prompts and trusted folders
**Goal:** stop asking permission for harmless reads, and ask once for the thing that matters: whether to trust a folder.
- [x] A `--permission-mode auto` (and `/permissions`) that, inside a trusted folder, stops asking before adding files, creating or editing files, running shell commands and similar actions. The default mode `ask` keeps today's behavior. **Done**
- [x] A one-time "Trust this folder?" question when pairforge starts in a folder it has not seen before; the answer is remembered. **Done**
- [x] `/permissions trust` and `/permissions untrust` change a folder's trust during a session, so a "no" answer is not permanent. **Done**
- [x] Respect the model's context size: add small files in full, and give an outline for large ones instead of overflowing small local models or wasting paid tokens. **Done** (in auto mode a mentioned file that fits in 25% of the context window is added in full; a larger one is sent as an outline of its classes and functions, built from the repo map, with a note to `/add` it for editing)
- [x] No routine questions in auto mode: creating the git repo, updating `.gitignore`, opening documentation links (printed instead), sending a request near the context limit, `/lint` fixes and creating files named in `/add`. The analytics opt-in question is gone (off unless `--analytics`). Installing packages still asks. **Done**
- [ ] Optional graphify integration (an install extra, not a hard dependency) so reading a folder or file uses a code graph and targeted queries rather than raw file contents. **Planned**

### 9. Plan-first workflow
**Goal:** for larger tasks, work the way a careful engineer does: plan, split the work, then code.
- [x] `/plan <request>`: a numbered plan of at most 8 small steps, then the edits for each step with the whole plan as context. **Done**
- [x] Show the plan and task list as they progress, and in `auto` permission mode run through them without stopping to ask (ask mode confirms once). **Done**

### 11. Small local models (up to about 17B)
**Goal:** models that fit on a laptop should edit code reliably.
- [x] Compact prompts: no example conversation and a shorter main system prompt for local models of 17B or fewer (`--compact-prompts` / `--no-compact-prompts`); the edit format rules stay verbatim. **Done**
- [x] Cap Ollama's `num_ctx` at the model's context window so requests do not overflow VRAM. **Done**
- [x] Fall back to the whole edit format, once per session, when a local model sends malformed edits twice in one request, and retry the request. **Done**
- [x] Repo map sized to 5% of a local model's window (512 to 4096 tokens). **Done**
- [x] Add `/no_think` to the request for local qwen3 models when the reasoning effort is low. **Done**

## Working principles

- Prefer small, reviewable changes with tests.
- Change the inherited behavior deliberately and record why.
- Pull useful upstream fixes by cherry-picking from the `upstream` remote. We do not track upstream wholesale.

## Long-term ideas

- [ ] **Faster, lighter core in a compiled language (Rust or Go).** The slow part of a session is the LLM, not Python, so this is about startup time, install size and shipping a single binary, not raw speed. We defer it until the feature set and architecture have settled. A staged path is possible: first move heavy parts such as the repo map into a separate core called from Python, and rewrite the rest only if that proves worthwhile. A full rewrite would no longer be a fork; the original project would still be credited. **Idea**

## Ideas

Add new ideas here as they come up. Open an issue to discuss anything that is not on this list.
