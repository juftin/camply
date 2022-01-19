#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

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
        PUSHOVER_PUSH_USER=dict(default="", notes="Enables Pushover Notifications"),
        PUSHBULLET_API_TOKEN=dict(default="", notes="Enables Pushbullet Notifications"),
        EMAIL_TO_ADDRESS=dict(default="", notes="Email Notifications will be sent here"),
        EMAIL_USERNAME=dict(default="", notes="Email Authorization Login Username"),
        EMAIL_PASSWORD=dict(default="", notes="Email Authorization Login Password"),
        EMAIL_SMTP_SERVER=dict(default="smtp.gmail.com",
                               notes="Email Authorization SMTP Server Address"),
        EMAIL_SMTP_PORT=dict(default=465, notes="Email Authorization SMTP Server Port"),
        EMAIL_FROM_ADDRESS=dict(default="camply@juftin.com",
                                notes="Email Notifications Will Come From this Email"),
        EMAIL_SUBJECT_LINE=dict(default="Camply Notification",
                                notes="Email Notifications Will Have This Subject Line"),
        PUSHOVER_PUSH_TOKEN=dict(default="", notes="Pushover Notifications From Your Custom App "
                                                   "(not required)"),
        RIDB_API_KEY=dict(default="", notes="Personal Recreation.gov API Key (not required)")
    )
