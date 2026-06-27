"""
Notification Testing
"""

from unittest.mock import MagicMock

from pytest import MonkeyPatch

from camply import AvailableCampsite
from camply.config.notification_config import WebhookConfig
from camply.notifications import PushoverNotifications
from camply.notifications.webhook import WebhookNotifications
from camply.search.base_search import BaseCampingSearch
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


def test_no_notifications_when_no_new_campsites():
    """
    Verify that notifications are not sent when no new campsites are found
    """
    self_mock = MagicMock(spec=BaseCampingSearch)
    self_mock._get_polling_minutes.return_value = 10
    self_mock._search_matching_campsites_available.return_value = ["campsite1"]
    self_mock.campsites_found = {"campsite1"}

    BaseCampingSearch._continuous_search_retry(
        self=self_mock,
        log=False,
        verbose=False,
        polling_interval=10,
        continuous_search_attempts=1,
        notification_provider="silent",
        notify_first_try=False,
        search_once=True,
    )

    self_mock.assemble_availabilities.assert_called_once_with(
        matching_data=[], log=False, verbose=False
    )
    self_mock._handle_notifications.assert_not_called()


def test_webhook_notifier_empty_campsites(monkeypatch: MonkeyPatch):
    """
    Verify WebhookNotifications does not send empty campsite lists
    """
    monkeypatch.setattr(WebhookConfig, "WEBHOOK_URL", "http://example.com/webhook")

    mock_session = MagicMock()

    notifier = WebhookNotifications()
    notifier.session = mock_session

    notifier.send_campsites([])

    mock_session.post.assert_not_called()
