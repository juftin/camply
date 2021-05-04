#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Yellowstone Variables
"""

from datetime import datetime
import logging
from os import environ
from typing import List

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
    API_BASE_PATH: str = "v1/api"
    LODGING_PATH: str = f"/{API_BASE_PATH}/availability/hotels"
    YELLOWSTONE_PARK_PATH: str = "yellowstonenationalparklodges"
    YELLOWSTONE_LODGING_PATH: str = f"{LODGING_PATH}/{YELLOWSTONE_PARK_PATH}"
    CAMPSITE_AVAILABILITY: str = f"{API_BASE_PATH}/availability/rooms"
    YELLOWSTONE_CAMPSITE_AVAILABILITY: str = f"{CAMPSITE_AVAILABILITY}/{YELLOWSTONE_PARK_PATH}"
    YELLOWSTONE_PROPERTY_INFO: str = f"{API_BASE_PATH}/property/rooms/{YELLOWSTONE_PARK_PATH}"
    API_REFERRERS: dict = {
        "Host": "webapi.xanterra.net",
        "Origin": "https://secure.yellowstonenationalparklodges.com",
        "Referer": "https://secure.yellowstonenationalparklodges.com/"
    }

    LODGING_CAMPGROUND_QUALIFIER: str = ":RV"

    # JSON FILTERING
    BOOKING_AVAILABILITY: str = "availability"

    # DATAFRAME FILTERING
    FACILITY_ID: str = "facility_id"
    FACILITY_STATUS: str = "status"
    FACILITY_STATUS_QUALIFIER: str = "OPEN"
    FACILITY_ROOMS: str = "rooms"
    FACILITY_AVAILABLE_QUALIFIER: str = "available"
    FACILITY_HOTEL_CODE: str = "hotelCode"
    FACILITY_ROOM_CODE: str = "roomCode"
    FACILITY_PRICE: str = "price"
    FACILITY_TYPE: str = "type"

    CAMPSITE_DATA_COLUMNS: List[str] = ["facility_id", "facility_name", "booking_url"]

    RATE_CODE: str = "INTERNET"
    LODGING_RATES: str = "rates"
    LODGING_TITLE: str = "title"
    LODGING_BASE_PRICES: str = "mins"

    MINIMUM_POLLING_INTERVAL: int = 45

    WEBUI_BASE_ENDPOINT: str = "secure.yellowstonenationalparklodges.com"
    WEBUI_BOOKING_PATH: str = "booking/lodging-select"

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
