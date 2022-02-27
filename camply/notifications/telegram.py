#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Push Notifications via Telegram
"""

from abc import ABC
from datetime import datetime
import logging
from typing import List, Optional

import requests

from camply.config import CampsiteContainerFields, TelegramConfig
from .base_notifications import BaseNotifications
from ..containers import AvailableCampsite

logger = logging.getLogger(__name__)


class TelegramNotifications(BaseNotifications, ABC):
    """
    Push Notifications via Telegram
    """

    def __init__(self):
        if any([TelegramConfig.BOT_TOKEN is None,
                TelegramConfig.BOT_TOKEN == "",
                TelegramConfig.CHAT_ID is None,
                TelegramConfig.CHAT_ID == ""]):
            warning_message = (
                "Telegram is not configured properly. To send Telegram messages "
                "make sure to run `camply configure` or set the "
                "proper environment variables: `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.")
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

    def __repr__(self):
        """
        String Representation
        """
        return "<TelegramNotifications>"

    @staticmethod
    def send_message(message: str, escaped=False, **kwargs) -> Optional[requests.Response]:
        """
        Send a message via Telegram - if environment variables are configured

        Parameters
        ----------
        message: str
        escaped: bool

        Returns
        -------
        Response
        """
        if not escaped:
            message = TelegramNotifications.escape_text(message)

        telegram_headers = TelegramConfig.API_HEADERS.copy()
        message_json = TelegramConfig.API_CONTENT.copy()
        message_json.update({"text": message})
        logger.debug(message_json)
        response = requests.post(url=TelegramConfig.API_ENDPOINT,
                                 headers=telegram_headers,
                                 json=message_json)
        if response.status_code != 200:
            logger.warning("Notifications weren't able to be sent to Telegram. "
                           "Your configuration might be incorrect.")
            logger.debug(response.text)
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
        fields = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for f in fields:
            message = message.replace(f, f"\{f}")
        return message

    @staticmethod
    def send_campsites(campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: AvailableCampsite
        """
        for campsite in campsites:
            fields = list()
            for key, value in campsite.dict().items():
                if key == CampsiteContainerFields.BOOKING_URL:
                    key = "booking_link"
                elif key in [CampsiteContainerFields.BOOKING_DATE,
                             CampsiteContainerFields.BOOKING_END_DATE]:
                    value: datetime = value.strftime("%Y-%m-%d")
                formatted_key = TelegramNotifications.escape_text(key.replace("_", " ").title())
                formatted_value = TelegramNotifications.escape_text(str(value))
                fields.append(f"{formatted_key}: {formatted_value}")
            message_fields = "\n".join(fields)
            message = (f"*{TelegramNotifications.escape_text(campsite.recreation_area)} "
                       f"\| {TelegramNotifications.escape_text(campsite.facility_name)} "
                       f"\| {TelegramNotifications.escape_text(campsite.booking_date.strftime('%Y-%m-%d'))}*"
                       f"\n{message_fields}")
            TelegramNotifications.send_message(message, escaped=True)
