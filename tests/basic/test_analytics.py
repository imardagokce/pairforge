from unittest.mock import patch

from aider.analytics import Analytics


def test_analytics_is_noop_stub(tmp_path):
    with patch("pathlib.Path.home", return_value=tmp_path):
        analytics = Analytics()
        analytics.enable()
        analytics.event("launched")
        analytics.event("exit", reason="done", main_model=None)
        analytics.disable(permanently=True)
        analytics.save_data()
        analytics.load_data()

    assert analytics.user_id is None
    assert analytics.mp is None
    assert analytics.ph is None
    assert not (tmp_path / ".aider").exists()


def test_need_to_ask_always_false():
    analytics = Analytics()
    for value in (True, False, None):
        assert analytics.need_to_ask(value) is False


def test_constructor_accepts_legacy_arguments():
    analytics = Analytics(
        logfile="x.log",
        permanently_disable=True,
        posthog_host="https://example.invalid",
        posthog_project_api_key="key",
    )
    analytics.event("launched")
