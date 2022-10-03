"""
Push Notifications via Twilio
"""

import logging
from typing import List

from camply.config import TwilioConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)
logging.getLogger("twilio").setLevel(logging.ERROR)


class TwilioNotifications(BaseNotifications):
    """
    Push Notifications via Twilio
    """

    def __init__(self):
        super().__init__()
        try:
            from twilio.rest import Client
        except ImportError:
            raise RuntimeError(
                "Looks like `twilio` isn't installed. Install it with `pip install camply[twilio]`"
            )

        if any(
            [
                TwilioConfig.ACCOUNT_SID is None,
                TwilioConfig.ACCOUNT_SID == "",
                TwilioConfig.AUTH_TOKEN is None,
                TwilioConfig.AUTH_TOKEN == "",
            ]
        ):
            warning_message = (
                "Twilio is not configured properly. To send Twilio messages "
                "make sure to run `camply configure` or set the "
                "proper environment variable: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`."
            )
            logger.error(warning_message)
            raise EnvironmentError(warning_message)
        self.client = Client(TwilioConfig.ACCOUNT_SID, TwilioConfig.AUTH_TOKEN)
        self.phone_nums = TwilioConfig.DEST_NUMBERS.split(",")
        logger.info(
            "Twilio: will notify these phone numbers: " + ", ".join(self.phone_nums)
        )

    def send_message(self, message: str, **kwargs):
        """
        Send a message via Twilio - if environment variables are configured

        Parameters
        ----------
        message: str
        """
        for phone_num in self.phone_nums:
            self.client.messages.create(
                to=phone_num, from_=TwilioConfig.SOURCE_NUMBER, body=message
            )

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
            fields = [f"🏕{message_title}", ""]
            for key, value in formatted_dict.items():
                fields.append(f"{key}: {value}")
            fields.append("")
            fields.append("camply, the campsite finder ⛺️")
            composed_message = "\n".join(fields)
            self.send_message(message=composed_message)
