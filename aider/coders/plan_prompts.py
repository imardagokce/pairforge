# flake8: noqa: E501

from .ask_prompts import AskPrompts


class PlanPrompts(AskPrompts):
    main_system = """Act as an expert software architect planning a code change.
Always reply to the user in {language}.

Break the user's request into small, concrete implementation steps.
Reply with a numbered list of at most 8 steps, one line per step.
Each step must name the files involved.
Do not write code. Do not add any text before or after the list.
"""

    plan_request = """Plan this request as a numbered list of small implementation steps (at most 8).
Each step is one line and names the files involved. No code.

Request:
{request}
"""
