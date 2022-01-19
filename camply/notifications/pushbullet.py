#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Push Notifications via Pushbullet
"""

from abc import ABC
from datetime import datetime
import logging
from typing import List, Optional

import requests

from camply.config import CampsiteContainerFields, PushbulletConfig
from .base_notifications import BaseNotifications
from ..containers import AvailableCampsite

logger = logging.getLogger(__name__)


class PushbulletNotifications(BaseNotifications, ABC):
    """
    Push Notifications via PushBullet
    """

    def __init__(self):
        if any([PushbulletConfig.API_TOKEN is None,
                PushbulletConfig.API_TOKEN == ""]):
            warning_message = (
                "Pushbullet is not configured properly. To send Pushbullet messages "
                "make sure to run `camply configure` or set the "
                "proper environment variable: `PUSHBULLET_API_TOKEN`.")
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

    def __repr__(self):
        """
        String Representation
        """
        return "<PushbulletNotifications>"

    @staticmethod
    def send_message(message: str, **kwargs) -> Optional[requests.Response]:
        """
        Send a message via PushBullet - if environment variables are configured

        Parameters
        ----------
        message: str

        Returns
        -------
        Response
        """
        pushbullet_headers = PushbulletConfig.API_HEADERS.copy()
        pushbullet_headers.update({"Access-Token": PushbulletConfig.API_TOKEN})
        message_type = kwargs.pop("type", "note")
        message_title = kwargs.pop("title", "Camply Notification")
        message_json = dict(type=message_type, title=message_title, body=message,
                            **kwargs)
        logger.debug(message_json)
        response = requests.post(url=PushbulletConfig.PUSHBULLET_API_ENDPOINT,
                                 headers=pushbullet_headers,
                                 json=message_json)
        if response.status_code != 200:
            logger.warning("Notifications weren't able to be sent to Pushbullet. "
                           "Your configuration might be incorrect.")
            logger.debug(response.text)
        return response

    @staticmethod
    def send_campsites(campsites: List[AvailableCampsite], **kwargs):
        """
        Send a message with a campsite object

        Parameters
        ----------
        campsites: AvailableCampsite
        """
        for campsite in campsites:
            fields = list()
            for key, value in campsite._asdict().items():
                if key == CampsiteContainerFields.BOOKING_URL:
                    key = "booking_link"
                elif key in [CampsiteContainerFields.BOOKING_DATE,
                             CampsiteContainerFields.BOOKING_END_DATE]:
                    value: datetime = value.strftime("%Y-%m-%d")
                formatted_key = key.replace("_", " ").title()
                fields.append(f"{formatted_key}: {value}")
            composed_message = "\n".join(fields)
            message_title = (f"{campsite.recreation_area} | {campsite.facility_name} | "
                             f"{campsite.booking_date.strftime('%Y-%m-%d')}")
            PushbulletNotifications.send_message(message=composed_message,
                                                 title=message_title,
                                                 type="note")
