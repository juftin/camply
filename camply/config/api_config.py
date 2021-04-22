#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Configuration
"""

API_HEADERS: list = [
    {"User-Agent": ("Mozilla/5.0 (X11; Linux x86_64; rv:10.0) "
                    "Gecko/20100101 Firefox/10.0")},
    {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36")},
    {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 "
                    "(KHTML, like Gecko) Version/14.0.3 Safari/605.1.15")},
    {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")},
    {"User-Agent": ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) "
                    "Gecko/20100101 Firefox/87.0")},
    {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36")}
]


class RIDBConfig(object):
    """
    RIDB API Configuration

    https://ridb.recreation.gov/docs
    """
    API_KEY: str = "842d8997-353f-4680-b340-f512610f20a9"

    RIDB_SCHEME: str = "https"
    RIDB_NET_LOC: str = "ridb.recreation.gov"
    RIDB_BASE_PATH: str = "api/v1/"

    # FACILITIES_API_PATH FIELDS

    FACILITIES_API_PATH: str = "facilities"
    FACILITY_DATA: str = "RECDATA"
    FACILITY_METADATA: str = "METADATA"
    FACILITY_METADATA_RESULTS: str = "RESULTS"

    PAGINATE_RESULT_COUNT: str = "CURRENT_COUNT"
    PAGINATE_TOTAL_COUNT: str = "TOTAL_COUNT"

    CAMPGROUND_FACILITY_FIELD: str = "FacilityTypeDescription"
    CAMPGROUND_FACILITY_FIELD_QUALIFIER: str = "Campground"
    CAMPGROUND_FACILITY_RESERVABLE_FIELD: str = "Reservable"
    CAMPGROUND_FACILITY_ENABLED_FIELD: str = "Enabled"
    FACILITY_ID: str = "FacilityID"
    FACILITY_NAME: str = "FacilityName"
    CAMPGROUND_RECREATION_AREA: str = "RECAREA"
    RECREATION_AREA_NAME: str = "RecAreaName"
    FACILITY_ADDRESS: str = "FACILITYADDRESS"
    FACILITY_LOCATION_STATE: str = "AddressStateCode"

    # RECREATION AREA FIELDS
    REC_AREA_API_PATH: str = "recareas"
    REC_AREA_ID: str = "RecAreaID"
    REC_AREA_NAME: str = "RecAreaName"
    REC_AREA_ADDRESS: str = "RECAREAADDRESS"
    REC_AREA_STATE: str = "AddressStateCode"


class RecreationBookingConfig(object):
    """
    Variable Storage Class for Recreation.gov Booking API
    """
    API_SCHEME: str = "https"
    API_NET_LOC = "recreation.gov"
    API_BASE_PATH: str = "api/camps/availability/campground/"
    API_MONTH_PATH: str = "month"

    CAMPSITE_UNAVAILABLE_STRINGS: list = [
        "Reserved",
        "Not Available",
        "Not Reservable",
        "Not Reservable Management"
    ]

    CAMPSITE_BASE: str = "campsites"
    CAMPSITE_AVAILABILITIES_BASE: str = "availabilities"

    CAMPSITE_LOCATION_LOOP: str = "loop"
    CAMPSITE_LOCATION_LOOP_DEFAULT: str = "Default Loop"

    CAMPSITE_LOCATION_SITE: str = "site"
    CAMPSITE_LOCATION_SITE_DEFAULT: str = "Default Site"

    CAMPSITE_INFO_TYPE: str = "campsite_type"
    CAMPSITE_INFO_MAX_PEOPLE: str = "max_num_people"
    CAMPSITE_INFO_MIN_PEOPLE: str = "min_num_people"
    CAMPSITE_INFO_TYPE_OF_USE: str = "type_of_use"

    CAMPSITE_BOOKING_URL: str = "https://www.recreation.gov/camping/campsites"
