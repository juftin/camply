"""
Notification Testing
"""

from camply import AvailableCampsite
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
