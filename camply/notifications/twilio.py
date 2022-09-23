"""
Push Notifications via Twilio
"""

import logging
from typing import List

from twilio.rest import Client

from camply.config import TwilioConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class TwilioNotifications(BaseNotifications):
    """
    Push Notifications via Twilio
    """

    def __init__(self):
        if any([TwilioConfig.ACCOUNT_SID == "", TwilioConfig.AUTH_TOKEN == ""]):
            warning_message = (
                "Twilio is not configured properly. To send Twilio messages "
                "make sure to run `camply configure` or set the "
                "proper environment variable: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`."
            )
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

        phone_nums = TwilioConfig.DEST_NUMBERS.split(",")
        logger.info("Twilio: will notify these phone numbers: " + ", ".join(phone_nums))

    def __repr__(self):
        """
        String Representation
        """
        return "<TwilioNotifications>"

    @staticmethod
    def send_message(message: str, **kwargs):
        """
        Send a message via Twilio - if environment variables are configured

        Parameters
        ----------
        message: str
        """
        client = Client(TwilioConfig.ACCOUNT_SID, TwilioConfig.AUTH_TOKEN)

        phone_nums = TwilioConfig.DEST_NUMBERS.split(",")

        for phone_num in phone_nums:
            client.messages.create(
                to=phone_num, from_=TwilioConfig.SOURCE_NUMBER, body=message
            )

    @classmethod
    def send_campsites(cls, campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: AvailableCampsite
        """
        for campsite in campsites:
            message_title, formatted_dict = cls.format_standard_campsites(
                campsite=campsite,
            )
            fields = [message_title]
            for key, value in formatted_dict.items():
                fields.append(f"{key}: {value}")
            composed_message = "\n".join(fields)
            TwilioNotifications.send_message(message=composed_message)
