#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Pushover Variables
"""

import logging
from os import environ

logger = logging.getLogger(__name__)


class PushoverConfig(object):
    """
    Pushover Notification Config Class
    """

    PUSHOVER_API_ENDPOINT: str = "https://api.pushover.net/1/messages.json"
    API_HEADERS: dict = {"Content-Type": "application/json"}

    try:
        PUSH_TOKEN: str = environ["PUSHOVER_PUSH_TOKEN"]
        PUSH_USER: str = environ["PUSHOVER_PUSH_USER"]

        if any([''.join(set(PUSH_TOKEN)).lower() == "x",
                ''.join(set(PUSH_USER)).lower() == "x",
                PUSH_TOKEN == "",
                PUSH_USER == ""]):
            PUSH_TOKEN = None
            PUSH_USER = None
    except KeyError:
        PUSH_TOKEN = None
        PUSH_USER = None
