#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Logging Utilities for Pushover Variables
"""

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
