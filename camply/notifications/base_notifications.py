"""
Push Notifications Template
"""

import logging
from abc import ABC, abstractmethod
from typing import List

from camply.containers import AvailableCampsite

logger = logging.getLogger(__name__)


class NotificationError(Exception):
    """
    Notification Exceptions
    """


class BaseNotifications(ABC):
    """
    Base Notifications
    """

    @staticmethod
    @abstractmethod
    def send_message(message: str, **kwargs):
        """
        Send a message

        Parameters
        ----------
        message: str
            Message Text
        **kwargs
            All kwargs passed to underlying notification method
        """
        pass

    @staticmethod
    @abstractmethod
    def send_campsites(campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        pass
