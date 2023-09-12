"""
Default Notifier: Silent + Extras
"""

import datetime
import logging
from typing import Dict, List, Type, Union

from camply.containers import AvailableCampsite
from camply.notifications.apprise import AppriseNotifications
from camply.notifications.base_notifications import BaseNotifications, NotificationError
from camply.notifications.email_notifications import EmailNotifications
from camply.notifications.ntfy import NtfyNotifications
from camply.notifications.pushbullet import PushbulletNotifications
from camply.notifications.pushover import PushoverNotifications
from camply.notifications.silent_notifications import SilentNotifications
from camply.notifications.slack import SlackNotifications
from camply.notifications.telegram import TelegramNotifications
from camply.notifications.twilio import TwilioNotifications
from camply.notifications.webhook import WebhookNotifications

logger = logging.getLogger(__name__)

CAMPSITE_NOTIFICATIONS: Dict[str, Type[BaseNotifications]] = {
    "pushover": PushoverNotifications,
    "email": EmailNotifications,
    "ntfy": NtfyNotifications,
    "apprise": AppriseNotifications,
    "pushbullet": PushbulletNotifications,
    "slack": SlackNotifications,
    "telegram": TelegramNotifications,
    "twilio": TwilioNotifications,
    "webhook": WebhookNotifications,
    "silent": SilentNotifications,
}


class MultiNotifierProvider(BaseNotifications):
    """
    Notifications Supported from Multiple Providers
    """

    def __init__(self, provider: Union[str, List[str], BaseNotifications, None]):
        """
        Initialize with a Notifier Class Object, a string or list of strings

        Parameters
        ----------
        provider: Union[str, List[str], BaseNotifications, None]
            Provider String, Comma Separated Provider String, or list of provider
            strings
        """
        super().__init__()
        self.providers = [SilentNotifications()]
        if isinstance(provider, str):
            provider = [prov_string.strip() for prov_string in provider.split(",")]
        for notifier_object in provider:
            if isinstance(notifier_object, BaseNotifications):
                notifier = notifier_object
            elif isinstance(notifier_object, str):
                notifier = CAMPSITE_NOTIFICATIONS.get(notifier_object.lower(), None)()
            elif notifier_object is None:
                notifier = None
            else:
                raise NotificationError(
                    "You must provide a proper Notification Identifier"
                )
            if notifier is not None and not isinstance(notifier, SilentNotifications):
                self.providers.append(notifier)

    def send_message(self, message: str, **kwargs):
        """
        Send a message

        Parameters
        ----------
        message: str
            Message Text
        **kwargs
            All kwargs passed to underlying notification method
        """
        for provider in self.providers:
            provider.send_message(message=message, **kwargs)

    def send_campsites(self, campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        for provider in self.providers:
            provider.send_campsites(campsites=campsites, **kwargs)

    def log_providers(self) -> None:
        """
        Log All Providers

        Returns
        -------
        None
        """
        provider_names = [str(provider) for provider in self.providers]
        logger.info(f"Notifications active via: {', '.join(provider_names)}")
        if len(self.providers) == 1:
            logger.info(
                f"Only {self.providers[0]} enabled. "
                "I hope you're watching these logs."
            )

    def last_gasp(self, error: Exception) -> None:
        """
        Make a `last gasp` notification before exiting

        Returns
        -------
        None
        """
        logger.info("Exception encountered, emitting notification last gasp.")
        date_string = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_string = str(error)
        error_message = (
            "camply encountered an error and exited 😟 "
            f"[{date_string}] - ({error.__class__.__name__}) {error_string}"
        )
        for provider in self.providers:
            if provider.last_gasp is True:
                provider.send_message(error_message)
        raise RuntimeError(error_message) from error
