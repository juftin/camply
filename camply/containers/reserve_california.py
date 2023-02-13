"""
ReserveCalifornia API Responses
"""

import datetime
from typing import Any, Dict, List, Optional

from camply.containers import CamplyModel


class ReserveCaliforniaRestrictions(CamplyModel):
    """
    ReserveCalifornia: Campsite Restrictions
    """

    FutureBookingStarts: datetime.datetime
    FutureBookingEnds: datetime.datetime
    MinimumStay: int
    MaximumStay: int
    IsRestrictionValid: bool
    Time: str


class ReserveCaliforniaUnitType(CamplyModel):
    """
    ReserveCalifornia: Unit Types
    """

    UnitTypeId: int
    UseType: int
    Name: str
    Available: bool
    AvailableFiltered: bool
    UnitCategoryId: int
    UnitTypeGroupId: int
    MaxVehicleLength: int
    HasAda: bool
    Restrictions: Optional[Any]
    AvailableCount: int


class ReserveCaliforniaAvailabilitySlice(CamplyModel):
    """
    Slice of Availability per Date
    """

    Date: datetime.date
    IsFree: bool
    IsBlocked: bool
    IsWalkin: bool
    ReservationId: int
    Lock: Any
    MinStay: int
    IsReservationDraw: bool


class ReserveCaliforniaAvailabilityUnit(CamplyModel):
    """
    UNit of Availability in Availability Request
    """

    UnitId: Optional[int]
    Name: Optional[str]
    ShortName: Optional[str]
    RecentPopups: Optional[int]
    IsAda: Optional[bool]
    AllowWebBooking: Optional[bool]
    MapInfo: Dict[str, Any] = {}
    IsWebViewable: Optional[bool]
    IsFiltered: Optional[bool]
    UnitCategoryId: Optional[int]
    SleepingUnitIds: Optional[List[int]]
    UnitTypeGroupId: Optional[int]
    UnitTypeId: Optional[int]
    UseType: Optional[int]
    VehicleLength: Optional[int]
    OrderBy: Optional[int]
    OrderByRaw: Optional[int]
    SliceCount: Optional[int]
    AvailableCount: Optional[int]
    Slices: Dict[datetime.datetime, ReserveCaliforniaAvailabilitySlice] = {}
    StartTime: Any
    EndTime: Any


class ReserveCaliforniaFacility(CamplyModel):
    """
    Campground Representation for ReserveCalifornia
    """

    FacilityId: int
    Name: str
    Description: str
    RateMessage: Optional[str]
    FacilityType: Optional[int]
    FacilityTypeNew: Optional[int]
    InSeason: Optional[bool]
    Available: Optional[bool]
    AvailableFiltered: Optional[bool]
    Restrictions: ReserveCaliforniaRestrictions
    Latitude: float
    Longitude: float
    Category: Optional[str]
    EnableCheckOccupancy: Optional[bool]
    AvailableOccupancy: Any
    FacilityAllowWebBooking: Optional[bool]
    UnitTypes: Dict[int, ReserveCaliforniaUnitType] = {}
    IsAvailableForGroup: Optional[bool]
    IsAvailableForPatron: Optional[bool]
    IsAvailableForEducationalGroup: Optional[bool]
    IsAvailableForCto: Optional[bool]
    FacilityBehaviourType: Optional[int]


class ReserveCaliforniaPlace(CamplyModel):
    """
    ReserveCalifornia: Place Object
    """

    PlaceId: int
    Name: str
    Description: str
    HasAlerts: bool
    IsFavourite: bool
    Allhighlights: str
    Url: str
    ImageUrl: str
    BannerUrl: str
    ParkSize: str
    Latitude: float
    Longitude: float
    TimeZone: str
    TimeStamp: datetime.datetime
    MilesFromSelected: int
    Available: bool
    AvailableFiltered: bool
    ParkCategoryId: int
    ParkActivity: int
    ParkPopularity: int
    AvailableUnitCount: int
    Restrictions: ReserveCaliforniaRestrictions
    Facilities: Dict[int, ReserveCaliforniaFacility]
    IsAvailableForGreatwalk: bool
    FacilityDefaultZoom: int


class ReserveCaliforniaDetailedPlace(CamplyModel):
    """
    https://calirdr.usedirect.com/RDR/rdr/fd/places
    """

    PlaceId: int
    Name: str
    Description: Optional[str]
    ParkSize: Optional[str]
    Latitude: float
    Longitude: float
    ParkCategoryId: Optional[int]
    ParkActivity: int
    ParkPopularity: int
    IsAvailableForGreatwalk: bool
    FacilityDefaultZoom: int
    RegionId: int
    ShortName: str
    OrderBy: int
    AllowWebBooking: bool
    InventoryLocking: bool
    InventoryLockDuration: int
    UsePrepend: bool
    PrependCode: str
    Address1: str
    Address2: Optional[str]
    City: str
    State: str
    Zip: str
    VoicePhone: str
    UDate: datetime.datetime
    UserId: int
    RowGuid: str
    IsWebViewable: bool
    WeekdayCheckdays: int
    WeekendCheckdays: int


class ReserveCaliforniaAvailabilityFacility(ReserveCaliforniaFacility):
    """
    ReserveCalifornia: Facility w/ Availability
    """

    FacilityMapSize: Optional[bool]
    FacilityImage: Optional[str]
    FacilityImageVBT: Optional[str]
    DatesInSeason: Optional[int]
    DatesOutOfSeason: Optional[int]
    SeasonDates: Dict[datetime.datetime, bool]
    TrafficStatuses: Dict[str, Any]
    UnitCount: int
    AvailableUnitCount: int
    SliceCount: int
    AvailableSliceCount: int
    TimebaseMaxHours: int
    TimebaseMinHours: int
    TimebaseDuration: float
    IsReservationDraw: bool
    DrawBookingStartDate: datetime.datetime
    DrawBookingEndDate: datetime.datetime
    Units: Optional[Dict[str, ReserveCaliforniaAvailabilityUnit]]


class ReserveCaliforniaAvailabilityResponse(CamplyModel):
    """
    API Response from /rdr/rdr/search/grid
    """

    Message: str
    Filters: Dict[str, Any]
    UnitTypeId: int
    StartDate: datetime.date
    EndDate: datetime.date
    NightsRequested: int
    NightsActual: int
    TodayDate: datetime.date
    TimeZone: str
    TimeStamp: datetime.datetime
    MinDate: datetime.date
    MaxDate: datetime.date
    AvailableUnitsOnly: bool
    UnitSort: str
    TimeGrid: bool
    ForUnit: bool
    UnitId: int
    TimeBetween: str
    TimeBetweenEval: str
    Facility: ReserveCaliforniaAvailabilityFacility


class ReserveCaliforniaUnitCategory(CamplyModel):
    """
    ReserveCalifornia: Unit Categories
    """

    UnitCategoryId: int
    UnitCategoryName: str
    HasEquipment: bool
    Icon: str


class ReserveCaliforniaNightlySleepingUnit(CamplyModel):
    """
    ReserveCalifornia: Nightly Sleeping Units
    """

    UnitCategoryId: int
    SleepingUnitId: int
    SleepingUnitName: str
    IsWheeled: bool
    Icon: str


class ReserveCaliforniaMinVehicleLength(CamplyModel):
    """
    ReserveCalifornia: Vehicle Length
    """

    SleepingUnitId: int
    MinVehicleLength: int
    MinVehicleName: str
    Icon: str


class ReserveCaliforniaUnitTypeGroup(CamplyModel):
    """
    ReserveCalifornia: Unit Type Groups
    """

    UnitCategoryId: int
    UnitTypesGroupId: int
    UnitTypesGroupName: str
    Icon: str


class ReserveCaliforniaAmenity(CamplyModel):
    """
    ReserveCalifornia: Amenities
    """

    AmenityId: int
    Name: str
    ShortName: str
    AmenityType: int
    IsSearchable: bool
    Description: str
    OrderBy: int
    IDate: datetime.datetime
    UDate: datetime.datetime
    ImagePath: Optional[str]
    UCashierName: Optional[str]
    UStoreId: Optional[int]
    IsADA: Optional[bool]
    Value: Optional[Any]


class ReserveCaliforniaMetadata(CamplyModel):
    """
    Campground Metadata Responses
    """

    Message: str
    UnitCategories: List[ReserveCaliforniaUnitCategory]
    NightlySleepingUnits: List[ReserveCaliforniaNightlySleepingUnit]
    MinVehicleLengths: List[ReserveCaliforniaMinVehicleLength]
    UnitTypesGroups: List[ReserveCaliforniaUnitTypeGroup]
    PlaceHighlights: List[Any]
    AllAmenity: List[ReserveCaliforniaAmenity]


class ReserveCaliforniaCityPark(CamplyModel):
    """
    ReserveCalifornia: City Parks
    """

    CityParkId: int
    Name: str
    Latitude: float
    Longitude: float
    IsActive: bool
    EntityType: Optional[str]
    EnterpriseId: Optional[int]
    ParkSize: str
    PlaceId: int


class ReserveCaliforniaFacilityMetadata(CamplyModel):
    """
    ReserveCalifornia: Facility Metadata
    """

    FacilityId: int
    RegionId: int
    PlaceId: int
    Name: str
    ShortName: str
    Description: Optional[str]
    OrderBy: int
    FacilityType: int
    UsePrepend: bool
    PrependCode: str
    AllowWebBooking: bool
    AutoOpenInventory: bool
    UDate: datetime.datetime
    RowGuid: str
    FacilityTypeNew: Optional[int]
    MaxPersonOccupancy: int
    IsAvailableForGroup: bool
    IsAvailableForEducationalGroup: Optional[bool]
    IsAvailableForCto: Optional[bool]
    IsCaptcha: bool
    FacilityBehaviourType: int
    EnableCheckOccupancy: bool
    IsTrail: Optional[bool]
    TimebaseMaxHours: int
    TimebaseMinHours: int
    TimebaseDuration: int
