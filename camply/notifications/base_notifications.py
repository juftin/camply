"""
Push Notifications Template
"""
import datetime
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

import requests

from camply.config import CampsiteContainerFields
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

    def __init__(self) -> None:
        """
        Instantiate with a Requests Session
        """
        self.session = requests.Session()

    def __repr__(self) -> str:
        """
        String Representation
        """
        return f"<{self.__class__.__name__}>"

    @abstractmethod
    def send_message(self, message: str, **kwargs):
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

    @abstractmethod
    def send_campsites(self, campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        """
        pass

    @classmethod
    def format_standard_campsites(
        cls, campsite: AvailableCampsite
    ) -> Tuple[str, Dict[str, str]]:
        """
        Format Standard Message
        """
        fields = {}
        message_title = " | ".join(
            [
                campsite.recreation_area,
                campsite.facility_name,
                campsite.booking_date.strftime("%Y-%m-%d"),
            ]
        )
        for key, value in campsite.dict().items():
            if key in [
                CampsiteContainerFields.BOOKING_DATE,
                CampsiteContainerFields.BOOKING_END_DATE,
            ]:
                value: datetime.date
                value: str = value.strftime("%Y-%m-%d")
            elif key == CampsiteContainerFields.BOOKING_URL:
                key = "booking_link"
            elif key == CampsiteContainerFields.PERMITTED_EQUIPMENT:
                equipment = (
                    []
                    if campsite.permitted_equipment is None
                    else campsite.permitted_equipment
                )
                value = "\n  - " + "\n  - ".join(
                    {item.equipment_name for item in equipment}
                )
            if key not in [CampsiteContainerFields.CAMPSITE_ATTRIBUTES]:
                formatted_key = key.replace("_", " ").title()
                fields[formatted_key] = value
        return message_title, fields
