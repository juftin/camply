"""
Project Configuration for Yellowstone Variables
"""

from collections import OrderedDict
from os.path import abspath, join
from pathlib import Path


class FileConfig:
    """
    File Path Storage Class
    """

    HOME_PATH = abspath(Path.home())
    DOT_CAMPLY_FILE = join(HOME_PATH, ".camply")
    _file_config_file = Path(abspath(__file__))
    _config_dir = _file_config_file.parent

    CAMPLY_DIRECTORY = _config_dir.parent
    ROOT_DIRECTORY = CAMPLY_DIRECTORY.parent

    DOT_CAMPLY_FIELDS = OrderedDict(
        PUSHOVER_PUSH_USER={"default": "", "notes": "Enables Pushover Notifications"},
        PUSHBULLET_API_TOKEN={
            "default": "",
            "notes": "Enables Pushbullet Notifications",
        },
        SLACK_WEBHOOK={"default": "", "notes": "Enables Slack Notifications"},
        TELEGRAM_BOT_TOKEN={"default": "", "notes": "Enables Telegram Notifications"},
        TELEGRAM_CHAT_ID={
            "default": "",
            "notes": "Telegram Notification will be sent here",
        },
        TWILIO_ACCOUNT_SID={"default": "", "notes": "Twilio Account SID"},
        TWILIO_AUTH_TOKEN={"default": "", "notes": "Twilio Auth Token"},
        TWILIO_SOURCE_NUMBER={
            "default": "",
            "notes": "Twilio Source number. E.164 format",
        },
        TWILIO_DEST_NUMBERS={
            "default": "",
            "notes": "Comma-separated list of phone numbers.",
        },
        EMAIL_TO_ADDRESS={
            "default": "",
            "notes": "Email Notifications will be sent here",
        },
        EMAIL_USERNAME={"default": "", "notes": "Email Authorization Login Username"},
        EMAIL_PASSWORD={"default": "", "notes": "Email Authorization Login Password"},
        EMAIL_SMTP_SERVER={
            "default": "smtp.gmail.com",
            "notes": "Email Authorization SMTP Server Address",
        },
        EMAIL_SMTP_PORT={
            "default": 465,
            "notes": "Email Authorization SMTP Server Port",
        },
        EMAIL_FROM_ADDRESS={
            "default": "camply@juftin.com",
            "notes": "Email Notifications Will Come From this Email",
        },
        EMAIL_SUBJECT_LINE={
            "default": "Camply Notification",
            "notes": "Email Notifications Will Have This Subject Line",
        },
        PUSHOVER_PUSH_TOKEN={
            "default": "",
            "notes": "Pushover Notifications From Your Custom App " "(not required)",
        },
        NTFY_TOPIC={
            "default": "",
            "notes": "NTFY Notification Topic",
        },
        APPRISE_URL={"default": "", "notes": "Apprise notification URL"},
        RIDB_API_KEY={
            "default": "",
            "notes": "Personal Recreation.gov API Key (not required)",
        },
    )

    PROVIDERS_DIRECTORY = CAMPLY_DIRECTORY.joinpath("providers")
    RESERVE_CALIFORNIA_PROVIDER = PROVIDERS_DIRECTORY.joinpath("reserve_california")
    USEDIRECT_PROVIDER = PROVIDERS_DIRECTORY.joinpath("usedirect")
