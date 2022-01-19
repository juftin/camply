#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Pushover Variables
"""

import logging
from os import environ, getenv
from typing import List, Optional

from dotenv import load_dotenv

from camply.config.file_config import FileConfig

logger = logging.getLogger(__name__)
load_dotenv(FileConfig.DOT_CAMPLY_FILE, override=False)


class PushoverConfig:
    """
    Pushover Notification Config Class
    """

    PUSHOVER_API_ENDPOINT: str = "https://api.pushover.net/1/messages.json"
    PUSHOVER_DEFAULT_API_TOKEN: bytes = b"YXAycjN2aW9tcXVmNzRnM3A4YWptbjc2YXlzbngz"
    API_HEADERS: dict = {"Content-Type": "application/json"}

    try:
        PUSH_TOKEN: str = environ["PUSHOVER_PUSH_TOKEN"]
        PUSH_USER: str = environ["PUSHOVER_PUSH_USER"]
    except KeyError:
        PUSH_TOKEN = None
        PUSH_USER = None


class EmailConfig:
    """
    Email Notification Config Class
    """

    EMAIL_TO_ADDRESS: Optional[str] = getenv("EMAIL_TO_ADDRESS", None)
    DEFAULT_FROM_ADDRESS: str = "camply@juftin.com"
    EMAIL_FROM_ADDRESS: str = getenv("EMAIL_FROM_ADDRESS", DEFAULT_FROM_ADDRESS)
    DEFAULT_SUBJECT_LINE: str = "Camply Notification"
    EMAIL_SUBJECT_LINE: str = getenv("EMAIL_SUBJECT_LINE", DEFAULT_SUBJECT_LINE)
    DEFAULT_SMTP_SERVER: str = "smtp.gmail.com"
    EMAIL_SMTP_SERVER: str = getenv("EMAIL_SMTP_SERVER", DEFAULT_SMTP_SERVER)
    EMAIL_USERNAME: Optional[str] = getenv("EMAIL_USERNAME", None)
    EMAIL_PASSWORD: Optional[str] = getenv("EMAIL_PASSWORD", None)
    DEFAULT_SMTP_PORT: int = 465
    EMAIL_SMTP_PORT: int = int(getenv("EMAIL_SMTP_PORT", DEFAULT_SMTP_PORT))

    ENVIRONMENT_VARIABLE_NAMES: List[str] = ["EMAIL_TO_ADDRESS",
                                             "EMAIL_USERNAME",
                                             "EMAIL_PASSWORD"]
    OPTIONAL_ENVIRONMENT_VARIABLE: List[str] = [
        f"EMAIL_SMTP_SERVER (default: {DEFAULT_SMTP_SERVER})",
        f"EMAIL_FROM_ADDRESS (default: {DEFAULT_FROM_ADDRESS})",
        f'EMAIL_SUBJECT_LINE (default: "{DEFAULT_SUBJECT_LINE}")',
        f"EMAIL_SMTP_PORT (default: {DEFAULT_SMTP_PORT})"]


class PushbulletConfig:
    """
    Pushbullet Notification Config Class
    """

    PUSHBULLET_API_ENDPOINT: str = "https://api.pushbullet.com/v2/pushes"
    API_HEADERS: dict = {"Content-Type": "application/json"}

    try:
        API_TOKEN: str = environ["PUSHBULLET_API_TOKEN"]
    except KeyError:
        API_TOKEN = None
