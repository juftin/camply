#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Push Notifications via Pushover
"""

from abc import ABC
import base64
from datetime import datetime
import logging
from typing import List, Optional

import requests

from camply.config import CampsiteContainerFields, PushoverConfig
from .base_notifications import BaseNotifications
from ..containers import AvailableCampsite

logger = logging.getLogger(__name__)


class PushoverNotifications(BaseNotifications, logging.StreamHandler, ABC):
    """
    Push Notifications via Pushover + a Logging Handler
    """

    def __init__(self, level: Optional[int] = logging.INFO):
        logging.StreamHandler.__init__(self)
        self.setLevel(level=level)
        if any([PushoverConfig.PUSH_USER is None, PushoverConfig.PUSH_USER == ""]):
            warning_message = ("Pushover is not configured properly. To send pushover messages "
                               "make sure to run `camply configure` or set the "
                               "proper environment variables: `PUSHOVER_PUSH_USER`, "
                               "`PUSHOVER_PUSH_TOKEN`.")
            logger.error(warning_message)
            raise EnvironmentError(warning_message)

    def __repr__(self):
        """
        String Representation
        """
        return "<PushoverNotifications>"

    @staticmethod
    def send_message(message: str, **kwargs) -> Optional[requests.Response]:
        """
        Send a message via Pushover - if environment variables are configured

        Parameters
        ----------
        message: str

        Returns
        -------
        Response
        """
        token = PushoverConfig.PUSH_TOKEN if PushoverConfig.PUSH_TOKEN not in [None, ""] \
            else base64.b64decode(PushoverConfig.PUSHOVER_DEFAULT_API_TOKEN).decode("utf-8")
        response = requests.post(url=PushoverConfig.PUSHOVER_API_ENDPOINT,
                                 headers=PushoverConfig.API_HEADERS,
                                 params=dict(token=token,
                                             user=PushoverConfig.PUSH_USER,
                                             message=message,
                                             **kwargs)
                                 )
        if response.status_code != 200:
            logger.warning("Notifications weren't able to be sent to Pushover. "
                           "Your configuration might be incorrect.")
            raise ConnectionError(response.text)
        return response

    def emit(self, record: logging.LogRecord):
        """
        Produce a logging record

        Parameters
        ----------
        record: str
            Message to log
        """
        log_formatted_message = "[{:>10}]: {}".format(record.levelname.upper(),
                                                      record.msg)
        title = f"Pushover {record.levelname.title()} Message"
        self.send_message(message=log_formatted_message, title=title)

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
                    key = "Booking Link"
                    value = f"<a href='{value}'>{value}"
                elif key in [CampsiteContainerFields.BOOKING_DATE,
                             CampsiteContainerFields.BOOKING_END_DATE]:
                    value: datetime = value.strftime("%Y-%m-%d")
                formatted_key = key.replace("_", " ").title()
                fields.append(f"<b>{formatted_key}:</b> {value}")
            composed_message = "\n".join(fields)
            message_title = (f"{campsite.recreation_area} | {campsite.facility_name} | "
                             f"{campsite.booking_date.strftime('%Y-%m-%d')}")
            PushoverNotifications.send_message(message=composed_message, title=message_title,
                                               html=1)
