"""
API Searching Configuration
"""

from os import getenv
from typing import Any, Dict, List, Tuple, Union

from dotenv import load_dotenv

from camply.config.data_columns import DataColumns
from camply.config.file_config import FileConfig
from camply.containers import CampgroundFacility

load_dotenv(FileConfig.DOT_CAMPLY_FILE, override=False)

STANDARD_HEADERS: Dict[str, str] = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,la;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


class APIConfig:
    """
    Base API Configuration
    """

    RETRY_API_MULTIPLIER: int = 3  # Exponential Backoff Multiplier
    RETRY_MAX_API_ATTEMPTS: int = 10  # Max Number of Retries
    RETRY_MAX_API_TIMEOUT: int = (
        6000  # Max Timeout in Seconds of Retrying (100 Minutes)
    )


class RIDBConfig(APIConfig):
    """
    RIDB API Configuration

    https://ridb.recreation.gov/docs
    """

    _camply_ridb_service_account_api_token: bytes = (
        b"YTc0MTY0NzEtMWI1ZC00YTY0LWFkM2QtYTIzM2U3Y2I1YzQ0"
    )
    _api_key: Union[str, bytes] = getenv(
        "RIDB_API_KEY", _camply_ridb_service_account_api_token
    )
    API_KEY = _camply_ridb_service_account_api_token if _api_key == "" else _api_key

    RIDB_SCHEME: str = "https"
    RIDB_NET_LOC: str = "ridb.recreation.gov"
    RIDB_BASE_PATH: str = "api/v1/"

    # FACILITIES_API_PATH FIELDS
    FACILITIES_API_PATH: str = "facilities"
    CAMPGROUND_FACILITY_FIELD_QUALIFIER: str = "Campground"
    TICKET_FACILITY_FIELD_QUALIFIER: str = "Ticket Facility"
    TIMED_ENTRY_FACILITY_FIELD_QUALIFIER: str = "Timed Entry"
    # RECREATION AREA FIELDS
    REC_AREA_API_PATH: str = "recareas"
    # CAMPSITE DETAILS
    CAMPSITE_API_PATH: str = "campsites"
    # TOUR DETAILS
    TOUR_API_PATH: str = "tours"


class RecreationBookingConfig(APIConfig):
    """
    Variable Storage Class for Recreation.gov Booking API
    """

    API_SCHEME: str = "https"
    API_NET_LOC = "www.recreation.gov"
    API_BASE_PATH: str = "api/camps/availability/campground/"
    API_MONTH_PATH: str = "month"
    API_REFERRERS: Dict[str, Any] = {"Referer": "https://www.recreation.gov/"}

    CAMPSITE_UNAVAILABLE_STRINGS: list = [
        "Reserved",
        "Not Available",
        "Not Reservable",
        "Not Reservable Management",
        "Not Available Cutoff",
        "Lottery",
        "Open",
        "NYR",
        "Closed",
    ]

    CAMPSITE_LOCATION_LOOP_DEFAULT: str = "Default Loop"
    CAMPSITE_LOCATION_SITE_DEFAULT: str = "Default Site"

    CAMPSITE_BOOKING_URL: str = "https://www.recreation.gov/camping/campsites"

    RATE_LIMITING = (1.01, 1.51)


class UseDirectConfig(APIConfig):
    """
    Reserve California API Configuration
    """

    RDR_PREFIX = "rdr"
    SEARCH_PREFIX = "search"
    CITYPARK_ENDPOINT = f"{RDR_PREFIX}/fd/citypark"
    LIST_PLACES_ENDPOINT = f"{RDR_PREFIX}/fd/places"
    LIST_FACILITIES_ENDPOINT = f"{RDR_PREFIX}/fd/facilities"
    SEARCH_ENDPOINT = f"{CITYPARK_ENDPOINT}/namecontains"
    METADATA_PREFIX = f"{RDR_PREFIX}/{SEARCH_PREFIX}/filters"
    PLACE_ENDPOINT = f"{RDR_PREFIX}/{SEARCH_PREFIX}/place"
    AVAILABILITY_ENDPOINT = f"{RDR_PREFIX}/{SEARCH_PREFIX}/grid"
    DATE_FORMAT = "%m-%d-%Y"


class YellowstoneConfig(DataColumns, APIConfig):
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
    YELLOWSTONE_CAMPSITE_AVAILABILITY: str = (
        f"{CAMPSITE_AVAILABILITY}/{YELLOWSTONE_PARK_PATH}"
    )
    YELLOWSTONE_PROPERTY_INFO: str = (
        f"{API_BASE_PATH}/property/rooms/{YELLOWSTONE_PARK_PATH}"
    )
    API_REFERRERS: dict = {
        "Host": "webapi.xanterra.net",
        "Origin": "https://secure.yellowstonenationalparklodges.com",
        "Referer": "https://secure.yellowstonenationalparklodges.com/",
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

    YELLOWSTONE_RECREATION_AREA_ID: int = 1
    YELLOWSTONE_RECREATION_AREA_NAME: str = "Yellowstone"
    YELLOWSTONE_RECREATION_AREA_FULL_NAME: str = "Yellowstone National Park"
    YELLOWSTONE_RECREATION_AREA_FORMAL_NAME: str = "Yellowstone National Park, USA"
    YELLOWSTONE_LOOP_NAME: str = "N/A"
    CAMPSITE_AVAILABILITY_STATUS: str = "Available"
    YELLOWSTONE_CAMPGROUND_NAME_REPLACE: Tuple[str, str] = (
        "CG Internet Rate",
        "Campground",
    )

    YELLOWSTONE_TIMEZONE: str = "America/Denver"

    # LODGES:  https://webapi.xanterra.net/v1/api/property/hotels/yellowstonenationalparklodges
    YELLOWSTONE_CAMPGROUNDS: Dict[str, str] = {
        "YLYC:RV": "Canyon Campground",
        "YLYB:RV": "Bridge Bay Campground",
        "YLYG:RV": "Grant Campground",
        "YLYM:RV": "Madison Campground",
        "YLYF:RV": "Fishing Bridge RV Park",
    }

    YELLOWSTONE_CAMPGROUND_OBJECTS: List[CampgroundFacility] = []
    for key, value in YELLOWSTONE_CAMPGROUNDS.items():
        YELLOWSTONE_CAMPGROUND_OBJECTS.append(
            CampgroundFacility(
                recreation_area_id=YELLOWSTONE_RECREATION_AREA_ID,
                recreation_area=YELLOWSTONE_RECREATION_AREA_FORMAL_NAME,
                facility_name=value,
                facility_id=str(key),
            )
        )
