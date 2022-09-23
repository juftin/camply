"""
Project Configuration for Pushover Variables
"""

import logging
from os import getenv
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
    PUSHOVER_DEFAULT_API_TOKEN: bytes = b"YWpjN3M1a2hhYTRlOG1zYWhncnFnaHduZGdtbmI3"
    API_HEADERS: dict = {"Content-Type": "application/json"}

    PUSH_TOKEN: str = getenv("PUSHOVER_PUSH_TOKEN", None)
    PUSH_USER: str = getenv("PUSHOVER_PUSH_USER", None)


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

    ENVIRONMENT_VARIABLE_NAMES: List[str] = [
        "EMAIL_TO_ADDRESS",
        "EMAIL_USERNAME",
        "EMAIL_PASSWORD",
    ]
    OPTIONAL_ENVIRONMENT_VARIABLE: List[str] = [
        f"EMAIL_SMTP_SERVER (default: {DEFAULT_SMTP_SERVER})",
        f"EMAIL_FROM_ADDRESS (default: {DEFAULT_FROM_ADDRESS})",
        f'EMAIL_SUBJECT_LINE (default: "{DEFAULT_SUBJECT_LINE}")',
        f"EMAIL_SMTP_PORT (default: {DEFAULT_SMTP_PORT})",
    ]


class PushbulletConfig:
    """
    Pushbullet Notification Config Class
    """

    PUSHBULLET_API_ENDPOINT: str = "https://api.pushbullet.com/v2/pushes"
    API_HEADERS: dict = {"Content-Type": "application/json"}

    API_TOKEN = getenv("PUSHBULLET_API_TOKEN", None)


class TwilioConfig:
    """
    Twilio Notification Config Class
    """

    ACCOUNT_SID = getenv("TWILIO_ACCOUNT_SID", None)
    AUTH_TOKEN = getenv("TWILIO_AUTH_TOKEN", None)
    SOURCE_NUMBER = getenv("TWILIO_SOURCE_NUMBER", None)
    # comma separated set of phone numbers
    DEST_NUMBERS = getenv("TWILIO_DEST_NUMBERS", None)


class SlackConfig:
    """
    Slack Notification Config Class
    """

    SLACK_WEBHOOK: Optional[str] = getenv("SLACK_WEBHOOK", None)


class TelegramConfig:
    """
    Telegram Notification Config Class
    """

    BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN", None)
    CHAT_ID = getenv("TELEGRAM_CHAT_ID", None)

    API_ENDPOINT: str = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    API_HEADERS: dict = {"Content-Type": "application/json"}
    API_CONTENT: dict = {
        "chat_id": CHAT_ID,
        "parse_mode": "MarkdownV2",
        "disable_web_page_preview": "true",
    }
