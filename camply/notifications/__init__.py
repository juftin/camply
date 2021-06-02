#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Notifications __init__ file
"""

from .email_notifications import EmailNotifications
from .pushbullet import PushbulletNotifications
from .pushover import PushoverNotifications
from .silent_notifications import SilentNotifications

CAMPSITE_NOTIFICATIONS: dict = {
    "pushover": PushoverNotifications,
    "email": EmailNotifications,
    "silent": SilentNotifications,
    "pushbullet": PushbulletNotifications
}
