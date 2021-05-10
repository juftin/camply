#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Silent Notifications
"""

from abc import ABC
import logging
from typing import List

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
        return f"<SilentNotifications>"

    @staticmethod
    def send_message(message: str, **kwargs) -> None:
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
        logger.info(f"SilentNotification: {message}")

    @staticmethod
    def send_campsites(campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        for campsite in campsites:
            SilentNotifications.send_message((campsite.recreation_area,
                                              campsite.facility_name,
                                              campsite.booking_date.strftime("%Y-%m-%d"),
                                              campsite.booking_url))
