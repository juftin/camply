#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Yellowstone Variables
"""

from datetime import datetime
import logging
from os import environ

logger = logging.getLogger(__name__)


class YellowstoneConfig(object):
    """
    Variable Storage Class
    """

    BOOKING_START: datetime = datetime.strptime(environ["BOOKING_DATE_START"], "%Y-%m-%d")
    NUMBER_OF_GUESTS = environ["NUMBER_OF_GUESTS"]
    NUMBER_OF_NIGHTS = environ["NUMBER_OF_NIGHTS"]
    POLLING_INTERVAL = int(environ["POLLING_INTERVAL"])

    API_SCHEME: str = "https"
    API_BASE_ENDPOINT: str = "webapi.xanterra.net"
    LODGING_PATH: str = "/v1/api/availability/hotels"
    YELLOWSTONE_LODGING_PATH: str = f"{LODGING_PATH}/yellowstonenationalparklodges"
    API_HEADERS: dict = {"Content-Type": "application/json"}

    LODGING_CAMPGROUND_QUALIFIER: str = ":RV"

    # JSON FILTERING
    BOOKING_AVAILABILITY: str = "availability"

    RATE_CODE: str = "INTERNET"
    LODGING_RATES: str = "rates"
    LODGING_TITLE: str = "title"
    LODGING_BASE_PRICES: str = "mins"

    MINIMUM_POLLING_INTERVAL: int = 45

    WEBUI_BASE_ENDPOINT: str = "secure.yellowstonenationalparklodges.com"
    WEBUI_BOOKING_PATH: str = "booking/lodging-search"

    @staticmethod
    def get_polling_interval(interval: int) -> int:
        """
        Ensure the Polling Interval never exceeds the minimum set

        Returns
        -------
        int
        """
        if interval < YellowstoneConfig.MINIMUM_POLLING_INTERVAL:
            logger.warning("Polling interval is too short, setting "
                           f"to {YellowstoneConfig.MINIMUM_POLLING_INTERVAL} seconds")
            return YellowstoneConfig.MINIMUM_POLLING_INTERVAL
        else:
            return interval
