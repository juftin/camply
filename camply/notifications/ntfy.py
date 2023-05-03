"""
Push Notifications via ntfy.sh
"""

import logging
from typing import List

import requests

from camply.config import NtfyConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class NtfyNotifications(BaseNotifications):
    """
    Push Notifications via Ntfy
    """

    def __init__(self):
        super().__init__()
        if any([NtfyConfig.NTFY_TOPIC is None, NtfyConfig.NTFY_TOPIC == ""]):
            warning_message = (
                "Ntfy is not configured properly. To send Ntfy messages "
                "set the proper environment variable: `NTFY_TOPIC`."
            )
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

    def send_message(self, message: str, **kwargs) -> requests.Response:
        """
        Send a message via Ntfy - if environment variables are configured

        Parameters
        ----------
        message: str

        Returns
        -------
        requests.Response
        """
        response = self.session.post(
            url=NtfyConfig.NTFY_API_ENDPOINT + NtfyConfig.NTFY_TOPIC,
            data=message.encode("utf-8"),
            headers={
                "Title": kwargs.get("title", "Camply Notification"),
                "Click": kwargs.get("url", ""),
            },
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as he:
            logger.warning(
                "Notifications weren't able to be sent to Ntfy. "
                "Your configuration might be incorrect."
            )
            raise ConnectionError(response.text) from he
        return response

    def send_campsites(self, campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: AvailableCampsite
        """
        for campsite in campsites:
            message_title, formatted_dict = self.format_standard_campsites(
                campsite=campsite,
            )
            fields = []
            for key, value in formatted_dict.items():
                fields.append(f"{key}: {value}")
            composed_message = "\n".join(fields)
            self.send_message(
                message=composed_message,
                title=message_title,
                url=formatted_dict.get("Booking Link", ""),
            )
