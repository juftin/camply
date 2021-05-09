#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Yellowstone Variables
"""

import logging
from typing import List, Tuple

from .data_columns import DataColumns

logger = logging.getLogger(__name__)


class YellowstoneConfig(DataColumns):
    """
    Variable Storage Class
    """

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
    LODGING_OCCUPANCY_BASE: str = "occupancyBase"
    LODGING_OCCUPANCY_MAX: str = "occupancyMax"
    LODGING_ERROR_MESSAGE: str = "message"

    MINIMUM_POLLING_INTERVAL: int = 45

    WEBUI_ALIAS_ENDPOINT: str = "yellowstonenationalparklodges.com"
    WEBUI_BASE_ENDPOINT: str = "secure.yellowstonenationalparklodges.com"
    WEBUI_BOOKING_PATH: str = "booking/lodging-select"

    CAMPSITE_ID_COLUMN: str = "campsite_code"
    BOOKING_DATE_COLUMN: str = "booking_date"
    CAMPSITE_SITE_NAME_COLUMN: str = "campsite_title"
    CAMPSITE_TYPE_COLUMN: str = "campsite_type"
    CAMPSITE_OCCUPANCY_COLUMN: str = "capacity"
    CAMPSITE_USE_TYPE_COLUMN: str = "campsite_type"
    AVAILABILITY_STATUS_COLUMN: str = "Available"
    RECREATION_AREA_COLUMN: str = "recreation_area"
    FACILITY_NAME_COLUMN: str = "facility_name"
    FACILITY_ID_COLUMN: str = "facility_id"
    BOOKING_URL_COLUMN: str = "booking_url"

    YELLOWSTONE_RECREATION_AREA_ID: int = 1
    YELLOWSTONE_RECREATION_AREA_NAME: str = "Yellowstone"
    YELLOWSTONE_LOOP_NAME: str = "N/A"
    CAMPSITE_AVAILABILITY_STATUS: str = "Available"
    YELLOWSTONE_CAMPGROUND_NAME_REPLACE: Tuple[str, str] = ("CG Internet Rate", "Campground")

    YELLOWSTONE_TIMEZONE: str = "America/Denver"

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
                           f"to {YellowstoneConfig.MINIMUM_POLLING_INTERVAL} minutes")
            return YellowstoneConfig.MINIMUM_POLLING_INTERVAL
        else:
            return interval
