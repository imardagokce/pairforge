"""No-op analytics stub.

pairforge collects no telemetry. This class keeps the interface that the rest
of the codebase calls (``event``, ``enable``, ``disable``, ``need_to_ask``,
``save_data``, ...) so call sites do not need to change. Every method does
nothing, and nothing is written to disk or sent over the network.
"""


class Analytics:
    # Kept for attribute reads elsewhere; always unset.
    mp = None
    ph = None
    user_id = None
    permanently_disable = None
    asked_opt_in = None
    logfile = None

    def __init__(
        self,
        logfile=None,
        permanently_disable=False,
        posthog_host=None,
        posthog_project_api_key=None,
    ):
        pass

    def enable(self):
        pass

    def disable(self, permanently=False):
        pass

    def need_to_ask(self, args_analytics):
        return False

    def load_data(self):
        pass

    def save_data(self):
        pass

    def event(self, event_name, main_model=None, **kwargs):
        pass
