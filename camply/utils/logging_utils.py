#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Logging Utilities for Pushover Variables
"""
import logging

CALENDARMOJI = "📅"
CAMPMOJI = "🏕"
TENTMOJI = "⛺️"
XMOJI = "❌"


def get_emoji(obj: list) -> str:
    """
    Return the Right Emoji

    Parameters
    ----------
    obj: list

    Returns
    -------
    str
    """
    assert isinstance(obj, list)
    if len(obj) >= 1:
        return TENTMOJI
    else:
        return XMOJI


def log_camply(self: logging.Logger, message: str, *args, **kwargs) -> None:
    """
    Custom Logging Notification Level for Pushover Logging

    Between logging.ERROR and logging.CRITICAL (45)

    Parameters
    ----------
    self: logging.Logger
    message: str
        Message String
    args
    kwargs
    Returns
    -------
    None
    """
    notification_level = logging.INFO + 1
    logging.addLevelName(level=notification_level, levelName="CAMPLY")
    if self.isEnabledFor(level=notification_level):
        self._log(level=notification_level, msg=message, args=args, **kwargs)
