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
- [ ] Discover running local servers (Ollama, LM Studio, llama.cpp server) and list their models. **In progress** (`/ollama` lists Ollama models; LM Studio and llama.cpp are still to do)
- [ ] `--local` quick-start that picks a model and sets sensible context size and edit format. **Planned**
- [ ] Per-model presets for common local models (context window, edit format, token limits). **Planned**
- [ ] Clear, actionable errors when the server is down or the context window is too small. **Planned**

### 2. Automatic compaction
**Goal:** long sessions stay usable without the user managing context.
- [ ] Trigger compaction automatically at a configurable fraction of the context window, instead of only at a fixed history token limit. **Planned**
- [x] A manual `/compact` command, plus a visible notice of what was summarized. **Done**
- [x] `/autocompact [N | N% | default]` to set the auto-summarize threshold during a session. **Done**
- [ ] Keep recent turns and file edits verbatim; summarize only older discussion. **Planned**
- [ ] Tests covering summary quality limits and token accounting. **Planned**

### 3. Automatic effort level
**Goal:** the tool chooses how much reasoning a task needs.
- [x] An `auto` value for `--reasoning-effort` that selects low, medium or high per message with a local heuristic (no extra LLM call). **Done**
- [x] Respect models that do not support the parameter (no error). **Done**
- [ ] Show the chosen level in the UI and allow an override per message. **In progress** (a line is printed when the level changes; per-message override is still to do)

### 4. Language support
**Goal:** a first-class experience in more languages.
- [ ] Localizable interface strings (prompts, messages, help). **Planned**
- [ ] Turkish as the first additional interface language. **Planned**
- [ ] Make the response language follow the user's locale by default, with `--chat-language` as an override. **Planned**

### 5. Terminal interface
**Goal:** a polished, consistent and pleasant terminal experience.
- [ ] A design pass: color theme, spacing and consistent message styles (user, assistant, tool, error). **Planned**
- [ ] Better diff and edit presentation. **Planned**
- [ ] A status line showing model, context usage, effort and git state. **Planned**
- [ ] Accessible themes (light, dark, high contrast) and a no-color mode. **Planned**

### 6. Feature pruning
**Goal:** remove what we do not use so the codebase is smaller and easier to change.
- [ ] Audit features and decide what to keep (candidates: voice input, GUI mode, analytics, benchmark harness, website assets). **Planned**
- [ ] Remove each item in its own change with tests updated. **Planned**
- [ ] Drop unused dependencies as features go. **Planned**

### 7. Project identity
**Goal:** make pairforge a clearly separate product.
- [ ] Rename the command and package (the `aider` name belongs to the original project). **Planned**
- [ ] Update documentation, badges and entry points to match. **Planned**
- [ ] Keep `LICENSE.txt`, `NOTICE` and attribution to the original project intact. **Planned**

### 8. Fewer prompts and trusted folders
**Goal:** stop asking permission for harmless reads, and ask once for the thing that matters: whether to trust a folder.
- [ ] A `--permission-mode auto` (and `/permissions`) that, inside a trusted folder, stops asking before adding files, creating or editing files, running shell commands and similar actions. The default mode `ask` keeps today's behavior. **In progress**
- [ ] A one-time "Trust this folder?" question when pairforge starts in a folder it has not seen before; the answer is remembered. **Planned**
- [ ] Respect the model's context size: add small files in full, and give an outline for large ones instead of overflowing small local models or wasting paid tokens. **Planned**
- [ ] Optional graphify integration (an install extra, not a hard dependency) so reading a folder or file uses a code graph and targeted queries rather than raw file contents. **Planned**

### 9. Plan-first workflow
**Goal:** for larger tasks, work the way a careful engineer does: plan, split the work, then code.
- [ ] Build on the existing architect/editor mode: first a short plan, then a task breakdown, then the edits for each task. **Planned**
- [ ] Show the plan and task list as they progress, and in `auto` permission mode run through them without stopping to ask. **Planned**

## Working principles

- Prefer small, reviewable changes with tests.
- Change the inherited behavior deliberately and record why.
- Pull useful upstream fixes by cherry-picking from the `upstream` remote. We do not track upstream wholesale.

## Long-term ideas

- [ ] **Faster, lighter core in a compiled language (Rust or Go).** The slow part of a session is the LLM, not Python, so this is about startup time, install size and shipping a single binary, not raw speed. We defer it until the feature set and architecture have settled. A staged path is possible: first move heavy parts such as the repo map into a separate core called from Python, and rewrite the rest only if that proves worthwhile. A full rewrite would no longer be a fork; the original project would still be credited. **Idea**

## Ideas

Add new ideas here as they come up. Open an issue to discuss anything that is not on this list.
