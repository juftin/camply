"""
Notification Testing
"""

import logging
from typing import Optional

import pytest
from pytest import LogCaptureFixture, MonkeyPatch

from camply import AvailableCampsite
from camply.config import PushoverConfig
from camply.notifications import PushoverNotifications
from tests.conftest import vcr_cassette


@vcr_cassette
def test_pushover_message():
    """
    Send a Pushover Message
    """
    pusher = PushoverNotifications()
    pusher.send_message(message="This is a test message!")


@vcr_cassette
def test_pushover_campsite(available_campsite: AvailableCampsite):
    """
    Send a Pushover Campsite
    """
    pusher = PushoverNotifications()
    pusher.send_campsites(campsites=[available_campsite])


@pytest.mark.parametrize(
    ("token", "expected_warnings"),
    [(None, 1), ("custom-token", 0)],
)
def test_pushover_default_token_warning_at_initialization(
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
    token: Optional[str],
    expected_warnings: int,
) -> None:
    """Warn at initialization when using the built-in Pushover token."""
    monkeypatch.setattr(PushoverConfig, "PUSH_USER", "test-user")
    monkeypatch.setattr(PushoverConfig, "PUSH_TOKEN", token)

    with caplog.at_level(logging.WARNING, logger="camply.notifications.pushover"):
        PushoverNotifications()
        warnings = [
            record
            for record in caplog.records
            if "built-in Pushover token" in record.message
        ]
        assert len(warnings) == expected_warnings
