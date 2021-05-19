#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Push Notifications Template
"""

from abc import ABC, abstractmethod
import logging
from typing import List

from camply.containers import AvailableCampsite

logger = logging.getLogger(__name__)


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
