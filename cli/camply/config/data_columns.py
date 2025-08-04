"""
Project Configuration for Data Variable Labels
"""


class DataColumns:
    """
    Variable Storage Class
    """

    CAMPSITE_ID_COLUMN: str = "campsite_code"
    BOOKING_DATE_COLUMN: str = "booking_date"
    BOOKING_END_DATE_COLUMN: str = "booking_end_date"
    BOOKING_NIGHTS_COLUMN: str = "booking_nights"
    CAMPSITE_SITE_NAME_COLUMN: str = "campsite_title"
    CAMPSITE_TYPE_COLUMN: str = "campsite_type"
    CAMPSITE_OCCUPANCY_COLUMN: str = "capacity"
    CAMPSITE_USE_TYPE_COLUMN: str = "campsite_type"
    AVAILABILITY_STATUS_COLUMN: str = "Available"
    RECREATION_AREA_COLUMN: str = "recreation_area"
    FACILITY_NAME_COLUMN: str = "facility_name"
    FACILITY_ID_COLUMN: str = "facility_id"
    BOOKING_URL_COLUMN: str = "booking_url"


class CampsiteContainerFields:
    """
    String Variable Storage Class
    """

    CAMPSITE_ID: str = "campsite_id"
    CAMPGROUND_ID: str = "facility_id"
    BOOKING_DATE: str = "booking_date"
    CAMPSITE_GROUP: str = "campsite_group"
    BOOKING_END_DATE: str = "booking_end_date"
    BOOKING_URL: str = "booking_url"
    LOCATION: str = "location"

    PERMITTED_EQUIPMENT: str = "permitted_equipment"
    CAMPSITE_ATTRIBUTES: str = "campsite_attributes"
