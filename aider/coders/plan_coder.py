import re

from .ask_coder import AskCoder
from .base_coder import Coder
from .plan_prompts import PlanPrompts

MAX_PLAN_STEPS = 8

_STEP_RE = re.compile(r"^\s*\d+[.)]\s+(\S.*?)\s*$")


def parse_plan_steps(text):
    """Return the numbered steps ("1." or "1)") found in text, at most MAX_PLAN_STEPS."""
    steps = []
    for line in (text or "").splitlines():
        match = _STEP_RE.match(line)
        if match:
            steps.append(match.group(1))
            if len(steps) == MAX_PLAN_STEPS:
                break
    return steps


class PlanCoder(AskCoder):
    """Asks the main model for a plan. It makes no edits itself."""

    edit_format = "plan"
    gpt_prompts = PlanPrompts()


def _make_editor(coder):
    editor_model = coder.main_model.editor_model or coder.main_model
    editor = Coder.create(
        io=coder.io,
        from_coder=coder,
        main_model=editor_model,
        edit_format=coder.main_model.editor_edit_format,
        suggest_shell_commands=False,
        map_tokens=0,
        total_cost=coder.total_cost,
        cache_prompts=False,
        num_cache_warming_pings=0,
        summarize_from_coder=False,
    )
    editor.cur_messages = []
    editor.done_messages = []
    return editor


def _step_message(steps, index, step):
    plan = "\n".join(f"{n}. {s}" for n, s in enumerate(steps, 1))
    return (
        "We are carrying out this plan one step at a time:\n"
        f"{plan}\n\n"
        f"Do ONLY step {index} now: {step}\n"
        "Do not start the other steps. Make only the changes this step needs."
    )


def run_plan(coder, request):
    """Plan request with the main model, then run each step with the editor model.

    Returns True if all steps ran, False otherwise.
    """
    io = coder.io

    planner = Coder.create(
        io=io,
        from_coder=coder,
        edit_format=PlanCoder.edit_format,
        summarize_from_coder=False,
    )
    message = PlanPrompts.plan_request.format(request=request)
    reply = planner.run(with_message=message, preproc=False)

    steps = parse_plan_steps(reply)
    if not steps:
        io.tool_warning("The planner returned no numbered steps; nothing was run.")
        return False

    total = len(steps)
    io.tool_output(f"Plan ({total} steps):")
    for i, step in enumerate(steps, 1):
        io.tool_output(f"[ ] {i}. {step}")

    approved = coder.auto_approved(f"run the {total}-step plan")
    if not (approved or io.confirm_ask("Run this plan?")):
        io.tool_output("Plan not run.")
        return False

    current = 0
    try:
        for i, step in enumerate(steps, 1):
            current = i
            io.tool_output(f"Step {i}/{total}: {step}")
            editor = _make_editor(coder)
            editor.run(with_message=_step_message(steps, i, step), preproc=False)
            coder.total_cost = editor.total_cost
            coder.aider_commit_hashes = editor.aider_commit_hashes
            io.tool_output(f"[x] {i}. {step}")
    except KeyboardInterrupt:
        io.tool_warning(f"Plan stopped by user after {current - 1} of {total} steps.")
        return False
    except Exception as err:
        io.tool_error(f"Step {current}/{total} failed: {err}. Plan stopped.")
        return False

    io.tool_output(f"Plan complete: {total} steps done.")
    return True
