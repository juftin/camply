"""
Push Notifications via Apprise
"""

import logging
from typing import List

from camply.config import AppriseConfig
from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)
logging.getLogger("apprise").setLevel(logging.ERROR)


class AppriseNotifications(BaseNotifications):
    """
    Push Notifications via Apprise
    """

    def __init__(self):
        super().__init__()
        try:
            import apprise
        except ImportError as ie:
            raise RuntimeError(
                "Looks like `apprise` isn't installed. Install it with `pip install camply[apprise]`"
            ) from ie

        if any(
            [
                AppriseConfig.APPRISE_URL is None,
            ]
        ):
            warning_message = (
                "Apprise is not configured properly. To send Apprise notifications "
                "make sure to run `camply configure` or set the "
                "proper environment variable: `APPRISE_URL`."
            )
            logger.error(warning_message)
            raise EnvironmentError(warning_message)
        self.client = apprise.Apprise()
        self.client.add(AppriseConfig.APPRISE_URL)
        logger.info("Apprise: will notify specified URL")

    def send_message(self, message: str, **kwargs):
        """
        Send a message via Apprise - if environment variables are configured

        Parameters
        ----------
        message: str
        """
        self.client.notify(
            body=message,
            title="Camply Notification",
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
