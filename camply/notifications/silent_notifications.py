"""
Silent Notifications
"""

import logging
from pprint import pformat
from typing import Iterable, List

from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class SilentNotifications(BaseNotifications):
    """
    Silent Notifications
    """

    def send_message(self, message: Iterable, **kwargs) -> None:
        """
        Send a message via Email

        Parameters
        ----------
        message: Iterable
            Email Body
        **kwargs
            kwargs are disregarded

        Returns
        -------
        None
        """
        message_string = "\n\t• " + "\n\t• ".join(list(message))
        logger.debug(f"SilentNotification: {message_string}")

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
            self.send_message(campsite_tuple)
            campsite_formatted = pformat(campsite.dict())
            logger.debug("Campsite Info: " + campsite_formatted)
