"""
Push Notifications via Slack
"""

import logging
from typing import List

import requests

from camply.config import SlackConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class SlackNotifications(BaseNotifications):
    """
    Push Notifications via Slack
    """

    def __init__(self):
        super().__init__()
        self.session.headers.update({"Content-Type": "application/json"})
        if any([SlackConfig.SLACK_WEBHOOK is None, SlackConfig.SLACK_WEBHOOK == ""]):
            warning_message = (
                "Slack is not configured properly. To send Slack messages "
                "make sure to run `camply configure` or set the "
                "proper environment variable: `SLACK_WEBHOOK`."
            )
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

    def send_message(self, message: str, **kwargs) -> requests.Response:
        """
        Send a message via Slack - if environment variables are configured.

        Parameters
        ----------
        message: str

        Returns
        -------
        requests.Response
        """
        message_blocks = kwargs.pop("blocks", [])
        message_json = {
            "text": message,
        }
        if message_blocks:
            message_json = {
                "blocks": message_blocks,
            }
        logger.debug(message_json)
        response = self.session.post(
            url=SlackConfig.SLACK_WEBHOOK,
            json=message_json,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as he:
            logger.warning(
                "Notifications weren't able to be sent to Slack. "
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
                fields.append(
                    {
                        "type": "mrkdwn",
                        "text": f"*{key}*",
                    }
                )
                if key in ["Permitted Equipment", "Booking Link"]:
                    data_type = "mrkdwn"
                else:
                    data_type = "plain_text"
                fields.append(
                    {
                        "type": data_type,
                        "text": str(value),
                    }
                )

            blocks = []
            blocks.append(
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": message_title,
                    },
                }
            )
            # Slack only allows 10 fields (k+v) per section
            for chunk in range(0, len(fields) + 1, 10):
                chunk_max = chunk + 10
                blocks.append(
                    {
                        "type": "section",
                        "fields": fields[chunk:chunk_max],
                    }
                )
            self.send_message(
                message=message_title,
                blocks=blocks,
            )
