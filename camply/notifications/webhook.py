"""
Generic Webhook Notifications
"""

import json
import logging
from typing import Any, Dict, List, Union

import requests
from pydantic.json import pydantic_encoder

from camply.config.notification_config import WebhookConfig
from camply.containers import AvailableCampsite
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

    def send_message(
        self, message: List[Union[AvailableCampsite, Dict[str, Any]]], **kwargs
    ) -> requests.Response:
        """
        Send a message via Webhook

        Parameters
        ----------
        message: str

        Returns
        -------
        requests.Response
        """
        json_message = json.dumps(message, default=pydantic_encoder)
        resp = self.session.post(url=self.webhook_url, json=json_message)
        return resp

    def send_campsites(self, campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        self.send_message(message=campsites)
