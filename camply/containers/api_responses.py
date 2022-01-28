"""
API Response Objects

These are JSON Responses from APIs
"""

import datetime
from typing import Any, Dict, Iterator, List, Optional, Union

from camply.config.api_config import RecreationBookingConfig
from camply.containers.base_container import CamplyModel


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


class FacilityResponse(CamplyModel):
    """
    /api/v1/facilities/<Facility ID>
    """

    FacilityID: int
    FacilityName: str
    FacilityTypeDescription: str
    Enabled: bool
    Reservable: bool
    FACILITYADDRESS: Optional[List[_FacilityAddress]]
    RECAREA: Optional[List[_FacilityRecArea]]


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
