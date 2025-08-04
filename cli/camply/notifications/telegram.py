"""
Push Notifications via Telegram
"""

import logging
from typing import List

import requests

from camply.config import TelegramConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class TelegramNotifications(BaseNotifications):
    """
    Push Notifications via Telegram
    """

    def __init__(self):
        super().__init__()
        self.session.headers.update(TelegramConfig.API_HEADERS)
        if any(
            [
                TelegramConfig.BOT_TOKEN is None,
                TelegramConfig.BOT_TOKEN == "",
                TelegramConfig.CHAT_ID is None,
                TelegramConfig.CHAT_ID == "",
            ]
        ):
            warning_message = (
                "Telegram is not configured properly. To send Telegram messages "
                "make sure to run `camply configure` or set the "
                "proper environment variables: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`."
            )
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

    def send_message(self, message: str, escaped=False, **kwargs) -> requests.Response:
        """
        Send a message via Telegram - if environment variables are configured

        Parameters
        ----------
        message: str
        escaped: bool

        Returns
        -------
        requests.Response
        """
        if not escaped:
            message = self.escape_text(message)
        message_json = TelegramConfig.API_CONTENT.copy()
        message_json.update({"text": message})
        logger.debug(message_json)
        response = self.session.post(url=TelegramConfig.API_ENDPOINT, json=message_json)
        try:
            response.raise_for_status()
        except requests.HTTPError as he:
            logger.warning(
                "Notifications weren't able to be sent to Telegram. "
                "Your configuration might be incorrect."
            )
            raise ConnectionError(response.text) from he
        return response

    @staticmethod
    def escape_text(message: str) -> str:
        """
        Escape a message for use in Telegram

        Parameters
        ----------
        message: str

        Returns
        -------
        String
        """
        fields = [
            "_",
            "*",
            "[",
            "]",
            "(",
            ")",
            "~",
            "`",
            ">",
            "#",
            "+",
            "-",
            "=",
            "|",
            "{",
            "}",
            ".",
            "!",
        ]
        for f in fields:
            message = message.replace(f, f"\\{f}")
        return message

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
                fields.append(self.escape_text(f"{key}: {value}"))
            message_fields = "\n".join(fields)
            message = f"*{self.escape_text(message_title)}*\n{message_fields}"
            self.send_message(message, escaped=True)
