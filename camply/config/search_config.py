#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Yellowstone Variables
"""


class SearchConfig:
    """
    File Path Storage Class
    """

    POLLING_INTERVAL_MINIMUM: int = 5  # 5 MINUTES
    RECOMMENDED_POLLING_INTERVAL: int = 10  # 10 MINUTES
    ERROR_MESSAGE: str = "No search days configured. Exiting"
    MINIMUM_CAMPSITES_FIRST_NOTIFY: int = 5
