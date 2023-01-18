"""
API Response Objects

These are JSON Responses from APIs
"""

import datetime
from typing import Any, Dict, Iterator, List, Optional, Union

from pydantic import validator

from camply.config.api_config import RecreationBookingConfig
from camply.containers.base_container import (
    CamplyModel,
    RecDotGovAttribute,
    RecDotGovEquipment,
)


class _CampsiteEquipment(CamplyModel):
    EquipmentName: str
    MaxLength: float


class _CampsiteAttribute(CamplyModel):
    AttributeName: str
    AttributeValue: str


class CoreRecDotGovResponse(CamplyModel):
    """
    Core Response from Recreation.gov
    """


class CampsiteResponse(CoreRecDotGovResponse):
    """
    https://ridb.recreation.gov/api/v1/campsites/<CAMPSITE ID>
    """

    CampsiteID: int
    FacilityID: int
    CampsiteName: str
    CampsiteType: str
    TypeOfUse: str
    Loop: str
    CampsiteAccessible: bool
    CampsiteReservable: bool
    CampsiteLongitude: float
    CampsiteLatitude: float
    CreatedDate: datetime.date
    LastUpdatedDate: datetime.date
    PERMITTEDEQUIPMENT: List[_CampsiteEquipment]
    ATTRIBUTES: List[_CampsiteAttribute]

    def __str__(self) -> str:
        """
        String Representation
        """
        return f"{self.CampsiteName} (#{self.CampsiteID})"


class TourResponse(CoreRecDotGovResponse):
    """
    https://ridb.recreation.gov/api/v1/tours/<TOUR ID>
    """

    TourID: int
    FacilityID: int
    TourName: str
    TourType: str
    TourDuration: int
    TourDescription: str
    TourAccessible: bool
    CreatedDate: datetime.date
    LastUpdatedDate: datetime.date
    ATTRIBUTES: List[_CampsiteAttribute]

    def __str__(self) -> str:
        """
        String Representation
        """
        return f"{self.TourName} (#{self.TourID})"


class Date(datetime.date):
    """
    Date Parsing
    """

    @classmethod
    def __get_validators__(cls) -> Iterator:
        """
        Generate Validators
        """
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, datetime.date]) -> datetime.date:
        """
        Validate Date Strings Into

        Parameters
        ----------
        v: Union[str, datetime.date]

        Returns
        -------
        datetime.date
        """
        if isinstance(v, str):
            return datetime.datetime.strptime(v, "%Y-%m-%d").date()
        elif isinstance(v, datetime.date):
            return v
        else:
            raise ValueError("You Must Provide a Parsable Date String or Object")


class UnawareDatetime(datetime.datetime):
    """
    Datetime Unaware Timestamp Parsing
    """

    @classmethod
    def __get_validators__(cls) -> Iterator:
        """
        Generate Validators
        """
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, datetime.datetime]) -> datetime.datetime:
        """
        Validate Date Strings Into

        Parameters
        ----------
        v: Union[str, datetime.datetime]

        Returns
        -------
        datetime.datetime
        """
        if isinstance(v, str):
            return datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
        elif isinstance(v, datetime.datetime):
            return v.replace(tzinfo=None)
        else:
            raise ValueError("You Must Provide a Parsable Datetime String or Object")


class AwareDatetime(datetime.datetime):
    """
    Datetime Aware Timestamp Parsing
    """

    @classmethod
    def __get_validators__(cls) -> Iterator:
        """
        Generate Validators
        """
        yield cls.validate

    @classmethod
    def validate(cls, v: Union[str, datetime.datetime]) -> datetime.datetime:
        """
        Validate Date Strings Into

        Parameters
        ----------
        v: Union[str, datetime.datetime]

        Returns
        -------
        datetime.datetime
        """
        if isinstance(v, str):
            return datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%S%z")
        elif isinstance(v, datetime.datetime):
            if v.tzinfo is None:
                raise ValueError(
                    "You Must Provide a Parsable Datetime Object with tzinfo"
                )
            return v
        else:
            raise ValueError("You Must Provide a Parsable Datetime String or Object")


class _CampsiteAvailabilityCampsiteResponse(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/campsites/<CAMPSITE ID>
    """

    availabilities: Dict[UnawareDatetime, str] = {}
    loop: str = RecreationBookingConfig.CAMPSITE_LOCATION_LOOP_DEFAULT
    campsite_type: Optional[str]
    max_num_people: int = 1
    min_num_people: int = 1
    type_of_use: Optional[str]
    site: str = RecreationBookingConfig.CAMPSITE_LOCATION_SITE_DEFAULT


class CampsiteAvailabilityResponse(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/campsites/<CAMPSITE ID>
    """

    campsites: Dict[int, _CampsiteAvailabilityCampsiteResponse]


class _TourMonthlyAvailabilityTourResponse(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/tours/<CAMPSITE ID>
    """

    facility_id: int
    tour_id: int
    local_date: Date
    availability_level: str
    not_yet_released: int
    reservable: int
    reserved_count: int
    scheduled_count: int
    walk_up: int


class _TourMonthlyAvailabilityDateResponse(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/tours/<CAMPSITE ID>
    """

    tour_availability_summary_view_by_tour_id: Dict[
        int, _TourMonthlyAvailabilityTourResponse
    ]


class TourMonthlyAvailabilityResponse(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/tours/<CAMPSITE ID>
    """

    facility_availability_summary_view_by_local_date: Dict[
        Date, _TourMonthlyAvailabilityDateResponse
    ]


class TourDailyAvailabilityBookingWindow(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/tours/<CAMPSITE ID>
    """

    open_timestamp: AwareDatetime
    close_timestamp: AwareDatetime


class TourDailyAvailabilityBookingWindows(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/tours/<CAMPSITE ID>
    """

    PRIMARY: Optional[TourDailyAvailabilityBookingWindow]
    SECONDARY: Optional[TourDailyAvailabilityBookingWindow]


class TourDailyAvailabilityResponse(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/tours/<CAMPSITE ID>
    """

    facility_id: int
    booking_windows: TourDailyAvailabilityBookingWindows
    inventory_count: Dict[str, int]
    reservation_count: Dict[str, int]
    status: str
    tour_date: Date
    tour_id: int
    tour_time: str


class _RecAreaAddress(CamplyModel):
    """
    Recreation Area Address Field
    """

    AddressStateCode: str


class RecreationAreaResponse(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/campsites/<CAMPSITE ID>
    """

    RecAreaID: Union[int, str]
    RecAreaName: str
    RECAREAADDRESS: List[_RecAreaAddress]


class _FacilityAddress(_RecAreaAddress):
    """
    Facility Address aka RecArea Address
    """


class _FacilityRecArea(CamplyModel):
    """
    Recreation Area inside of Facility
    """

    RecAreaID: Union[int, str]
    RecAreaName: str


class _FacilityOrganization(CamplyModel):
    """
    Organization inside of Facility
    """

    OrgName: str
    OrgID: int


class FacilityResponse(CamplyModel):
    """
    /api/v1/facilities/<Facility ID>
    """

    FacilityID: Union[int, str]
    FacilityName: str
    FacilityTypeDescription: str
    Enabled: bool
    Reservable: bool
    FACILITYADDRESS: Optional[List[_FacilityAddress]]
    RECAREA: Optional[List[_FacilityRecArea]]
    ORGANIZATION: Optional[List[_FacilityOrganization]]
    ParentRecAreaID: Optional[Union[int, str]]

    @validator("ParentRecAreaID", pre=True, always=False)
    def validate_parentrecid(cls, val: Any) -> Optional[int]:
        """
        Validate Empty Strings as Null
        """
        if val == "":
            return None
        return val


class _PaginationCountResponse(CamplyModel):
    """
    Pagination Counters
    """

    CURRENT_COUNT: int
    TOTAL_COUNT: int


class _PaginationMetadataResponse(CamplyModel):
    """
    Pagination Metadata
    """

    RESULTS: _PaginationCountResponse


class GenericResponse(CamplyModel):
    """
    Generic Response to Be Paginated
    """

    RECDATA: Any
    METADATA: _PaginationMetadataResponse


class XantPerGuest(CamplyModel):
    """
    PerGuest Objects
    """

    a2: Optional[Union[int, str]]
    b: Optional[Union[int, str]]
    b2: Optional[Union[int, str]]
    m: Optional[Union[int, str]]
    m2: Optional[Union[int, str]]
    r: Optional[Union[int, str]]
    r2: Optional[Union[int, str]]
    s: Optional[Union[int, str]]


class XantRates(CamplyModel):
    """
    Yellowstone Rates Object
    """

    code: str
    title: str
    description: str
    category: str
    minstay: int
    start: datetime.date
    available: Dict[int, int]
    mins: Dict[int, int]
    min: int

    @validator("start", pre=True)
    def parse_datetime(cls, value):
        """
        Parse Poorly Formatted Date Strings
        """
        return datetime.datetime.strptime(value, "%m/%d/%Y").date()


class XantCampgroundDetails(CamplyModel):
    """
    Yellowstone Campground Details OBject
    """

    hotelCode: str
    status: str
    message: str
    min: str
    max: str
    perGuests: Dict[int, XantPerGuest]
    rates: Dict[str, XantRates]
    rates2: Optional[Dict[str, XantRates]]


class XantResortData(CamplyModel):
    """
    Main Yellowstone API Response Wrapper
    """

    availability: Dict[datetime.date, Dict[str, XantCampgroundDetails]]

    @validator("availability", pre=True)
    def parse_datetime(cls, value):
        """
        Parse Poorly Formatted Date Strings
        """
        return {
            datetime.datetime.strptime(x, "%m/%d/%Y").date(): y
            for x, y in value.items()
        }


class RecDotGovCampsite(CamplyModel):
    """
    Recreation.gov Campsite Object
    """

    accessible: bool
    asset_id: int
    asset_type = str
    attributes: List[RecDotGovAttribute]
    average_rating: Optional[int]
    campsite_id: int
    campsite_reserve_type: str
    city: Optional[str]
    country_code: Optional[str]
    fee_templates: Dict[str, Any]
    latitude: Optional[float]
    longitude: Optional[float]
    loop: str
    name: str
    number_of_ratings = int
    org_id: int
    org_name: str
    parent_asset_id: int
    parent_asset_name: str
    parent_asset_type: str
    permitted_equipment: List[RecDotGovEquipment]
    preview_image_url: Optional[str]
    reservable: bool
    state_code: Optional[str]
    type: str
    type_of_use: str


class RecDotGovCampsiteResponse(CamplyModel):
    """
    Parent Response from Campsite Metadata
    """

    campsites: List[RecDotGovCampsite]
    size: int
    spelling_autocorrected: Any
    start: int
    total: int


class RecDotGovSearchResult(CamplyModel):
    """
    Recreation.gov Search Result Object
    """

    average_rating: Optional[int]
    description: str
    entity_id: int
    entity_type: str
    latitude: Optional[float]
    longitude: Optional[float]
    name: str
    number_of_ratings = int
    org_id: int
    parent_id: int
    parent_name: str
    parent_type: str
    preview_image_url: Optional[str]
    reservable: bool
    time_zone: str
    type: str


class RecDotGovSearchResponse(CamplyModel):
    """
    Parent Response from Search Results
    """

    results: List[RecDotGovSearchResult]
    size: int
    spelling_autocorrected: Any
    start: int
    total: int
