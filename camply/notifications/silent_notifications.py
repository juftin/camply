"""
Silent Notifications
"""

import logging
from pprint import pformat
from typing import List

from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class SilentNotifications(BaseNotifications):
    """
    Silent Notifications
    """

    def send_message(self, message: str, **kwargs) -> None:
        """
        Send a message via Email

        Parameters
        ----------
        message: str
            Email Body
        **kwargs
            kwargs are disregarded

        Returns
        -------
        None
        """
        logger.debug(f"SilentNotification: {message}")

    def send_campsites(self, campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        for campsite in campsites:
            campsite_tuple = (
                (
                    f"{campsite.booking_date.strftime('%Y-%m-%d')} - "
                    f"{campsite.booking_end_date.strftime('%Y-%m-%d')}"
                ),
                campsite.campsite_type,
                campsite.campsite_site_name,
                campsite.recreation_area,
                campsite.facility_name,
                campsite.booking_url,
            )
            message_string = "\n\t• " + "\n\t• ".join(campsite_tuple)
            self.send_message(message_string)
            campsite_formatted = pformat(campsite.dict())
            logger.debug("Campsite Info: " + campsite_formatted)
