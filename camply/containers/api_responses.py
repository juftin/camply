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


class CampsiteResponse(CamplyModel):
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


class _RecAreaAddress(CamplyModel):
    """
    Recreation Area Address Field
    """

    AddressStateCode: str


class RecreationAreaResponse(CamplyModel):
    """
    https://ridb.recreation.gov/api/v1/campsites/<CAMPSITE ID>
    """

    RecAreaID: int
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

    RecAreaID: int
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
    ParentRecAreaID: Optional[int]

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
