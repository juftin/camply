"""
Notification Testing
"""

import logging
from typing import Optional
from unittest.mock import Mock

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
def test_pushover_default_token_warning(
    available_campsite: AvailableCampsite,
    monkeypatch: MonkeyPatch,
    caplog: LogCaptureFixture,
    token: Optional[str],
    expected_warnings: int,
) -> None:
    """Warn once per instance when sending campsites with the built-in token."""
    monkeypatch.setattr(PushoverConfig, "PUSH_USER", "test-user")
    monkeypatch.setattr(PushoverConfig, "PUSH_TOKEN", token)
    send_message = Mock()
    monkeypatch.setattr(PushoverNotifications, "send_message", send_message)
    pusher = PushoverNotifications()

    with caplog.at_level(logging.WARNING, logger="camply.notifications.pushover"):
        pusher.send_campsites(campsites=[available_campsite])
        warnings = [
            record
            for record in caplog.records
            if "built-in Pushover token" in record.message
        ]
        assert len(warnings) == expected_warnings

        pusher.send_campsites(campsites=[available_campsite])
        warnings = [
            record
            for record in caplog.records
            if "built-in Pushover token" in record.message
        ]
        assert len(warnings) == expected_warnings

    assert send_message.call_count == 2
