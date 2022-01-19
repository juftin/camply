#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Silent Notifications
"""

from abc import ABC
import logging
from pprint import pformat
from typing import Iterable, List

from camply.containers import AvailableCampsite
from camply.notifications.base_notifications import BaseNotifications

logger = logging.getLogger(__name__)


class SilentNotifications(BaseNotifications, ABC):
    """
    Silent Notifications
    """

    def __init__(self):
        """
        Initialize Silent Notifications
        """
        logger.info(f"{self} enabled. I hope you're watching these logs.")

    def __repr__(self):
        """
        String Representation
        """
        return "<SilentNotifications>"

    @staticmethod
    def send_message(message: Iterable, **kwargs) -> None:
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

    @staticmethod
    def send_campsites(campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        for campsite in campsites:
            campsite_tuple = (
                (f"{campsite.booking_date.strftime('%Y-%m-%d')} - "
                 f"{campsite.booking_end_date.strftime('%Y-%m-%d')}"),
                campsite.campsite_type,
                campsite.campsite_site_name,
                campsite.recreation_area,
                campsite.facility_name,
                campsite.booking_url)
            SilentNotifications.send_message(campsite_tuple)
            campsite_formatted = pformat(dict(campsite._asdict()))
            logger.debug("Campsite Info: " + campsite_formatted)
