#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Pushover Variables
"""

import logging
from os import environ, getenv
from typing import List

from dotenv import load_dotenv

from camply.config.file_config import FileConfig

logger = logging.getLogger(__name__)
load_dotenv(FileConfig.DOT_ENV_FILE)


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


class EmailConfig(object):
    """
    Email Notification Config Class
    """
    EMAIL_TO_ADDRESS: str = getenv("EMAIL_TO_ADDRESS", None)
    EMAIL_FROM_ADDRESS: str = getenv("EMAIL_FROM_ADDRESS", "camply@juftin.com")
    EMAIL_SUBJECT: str = getenv("EMAIL_SUBJECT", "Camply Notification")
    SMTP_EMAIL_SERVER: str = getenv("SMTP_EMAIL_SERVER", "smtp.gmail.com")
    SMTP_EMAIL_SERVER_USERNAME: str = getenv("SMTP_EMAIL_SERVER_USERNAME", None)
    SMTP_EMAIL_SERVER_PASSWORD: str = getenv("SMTP_EMAIL_SERVER_PASSWORD", None)
    SMTP_EMAIL_SERVER_PORT: int = int(getenv("SMTP_EMAIL_SERVER_PORT", 465))

    ENVIRONMENT_VARIABLE_NAMES: List[str] = ["EMAIL_TO_ADDRESS",
                                             "SMTP_EMAIL_SERVER",
                                             "SMTP_EMAIL_SERVER_USERNAME",
                                             "SMTP_EMAIL_SERVER_PASSWORD"]
