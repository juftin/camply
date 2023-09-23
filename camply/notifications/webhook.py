"""
Generic Webhook Notifications
"""

import logging
from typing import List

import requests

from camply.config.notification_config import WebhookConfig
from camply.containers import AvailableCampsite
from camply.containers.data_containers import WebhookBody
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class WebhookNotifications(BaseNotifications):
    """
    Push Notifications via Webhooks
    """

    last_gasp: bool = False

    def __init__(self):
        super().__init__()
        self.webhook_url = WebhookConfig.WEBHOOK_URL
        self.webhook_headers = WebhookConfig.DEFAULT_HEADERS
        self.webhook_headers.update(WebhookConfig.WEBHOOK_HEADERS)
        self.session.headers = self.webhook_headers
        if self.webhook_url is None:
            warning_message = (
                "Webhook notifications are not configured properly. "
                "To send webhook messages "
                "make sure to run `camply configure` or set the "
                "proper environment variables: "
                "`WEBHOOK_URL` / `WEBHOOK_HEADERS`."
            )
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

    def send_message(self, message: str, **kwargs) -> None:
        """
        Webhooks only send campsite objects, not messages.
        """
        pass

    def send_campsites(self, campsites: List[AvailableCampsite], **kwargs) -> None:
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        webhook_body = WebhookBody(campsites=campsites).json().encode("utf-8")
        response = self.session.post(url=self.webhook_url, data=webhook_body)
        try:
            response.raise_for_status()
        except requests.HTTPError as he:
            logger.warning(
                f"Notifications weren't able to be sent to {self.webhook_url}. "
                "Your configuration might be incorrect."
            )
            raise ConnectionError(response.text) from he
