#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Push Notifications via Pushover
"""

import logging
from typing import Optional

import requests

from camply.config import PushoverConfig

logger = logging.getLogger(__name__)


class PushoverNotifications(logging.StreamHandler):
    """
    Push Notifications via Pushover + a Logging Handler
    """

    def __init__(self, level: Optional[int] = logging.INFO):
        logging.StreamHandler.__init__(self)
        self.setLevel(level=level)

    def __repr__(self):
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
        if PushoverConfig.PUSH_TOKEN is not None:
            response = requests.post(url=PushoverConfig.PUSHOVER_API_ENDPOINT,
                                     headers=PushoverConfig.API_HEADERS,
                                     params=dict(token=PushoverConfig.PUSH_TOKEN,
                                                 user=PushoverConfig.PUSH_USER,
                                                 message=message,
                                                 **kwargs)
                                     )
            if response.status_code != 200:
                logger.warning(f"Notifications weren't able to be sent to Pushover. "
                               "Your configuration might be incorrect.")
            return response
        else:
            logger.warning(f"Pushover isn't currently configured. "
                           "I hope you're watching these logs :)")

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
