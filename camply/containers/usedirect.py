"""
UseDirect API Responses
"""

import datetime
from typing import Any, Dict, List, Optional

from camply.containers import CamplyModel


class UseDirectRestrictions(CamplyModel):
    """
    UseDirect: Campsite Restrictions
    """

    FutureBookingStarts: datetime.datetime
    FutureBookingEnds: datetime.datetime
    MinimumStay: int
    MaximumStay: int
    IsRestrictionValid: bool
    Time: str


class UseDirectUnitType(CamplyModel):
    """
    UseDirect: Unit Types
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


class UseDirectAvailabilitySlice(CamplyModel):
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


class UseDirectAvailabilityUnit(CamplyModel):
    """
    Unit of Availability in Availability Request
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
    Slices: Dict[datetime.datetime, UseDirectAvailabilitySlice] = {}
    StartTime: Any
    EndTime: Any
    FacilityId: Optional[int]


class UseDirectFacility(CamplyModel):
    """
    Campground Representation for UseDirect
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
    Restrictions: UseDirectRestrictions
    Latitude: float
    Longitude: float
    Category: Optional[str]
    EnableCheckOccupancy: Optional[bool]
    AvailableOccupancy: Any
    FacilityAllowWebBooking: Optional[bool]
    UnitTypes: Dict[int, UseDirectUnitType] = {}
    IsAvailableForGroup: Optional[bool]
    IsAvailableForPatron: Optional[bool]
    IsAvailableForEducationalGroup: Optional[bool]
    IsAvailableForCto: Optional[bool]
    FacilityBehaviourType: Optional[int]


class UseDirectPlace(CamplyModel):
    """
    UseDirect: Place Object
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
    Restrictions: UseDirectRestrictions
    Facilities: Dict[int, UseDirectFacility]
    IsAvailableForGreatwalk: bool
    FacilityDefaultZoom: Optional[int]


class UseDirectDetailedPlace(CamplyModel):
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
    FacilityDefaultZoom: Optional[int]
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
    VoicePhone: Optional[str]
    UDate: datetime.datetime
    UserId: int
    RowGuid: str
    IsWebViewable: bool
    WeekdayCheckdays: int
    WeekendCheckdays: int


class UseDirectAvailabilityFacility(UseDirectFacility):
    """
    UseDirect: Facility w/ Availability
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
    TimebaseMinHours: Optional[int]
    TimebaseDuration: Optional[float]
    IsReservationDraw: Optional[bool]
    DrawBookingStartDate: Optional[datetime.datetime]
    DrawBookingEndDate: Optional[datetime.datetime]
    Units: Optional[Dict[str, UseDirectAvailabilityUnit]]


class UseDirectAvailabilityResponse(CamplyModel):
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
    Facility: UseDirectAvailabilityFacility


class UseDirectUnitCategory(CamplyModel):
    """
    UseDirect: Unit Categories
    """

    UnitCategoryId: int
    UnitCategoryName: str
    HasEquipment: bool
    Icon: Optional[str]


class UseDirectNightlySleepingUnit(CamplyModel):
    """
    UseDirect: Nightly Sleeping Units
    """

    UnitCategoryId: int
    SleepingUnitId: int
    SleepingUnitName: str
    IsWheeled: bool
    Icon: Optional[str]


class UseDirectMinVehicleLength(CamplyModel):
    """
    UseDirect: Vehicle Length
    """

    SleepingUnitId: int
    MinVehicleLength: int
    MinVehicleName: str
    Icon: Optional[str]


class UseDirectUnitTypeGroup(CamplyModel):
    """
    UseDirect: Unit Type Groups
    """

    UnitCategoryId: int
    UnitTypesGroupId: int
    UnitTypesGroupName: str
    Icon: Optional[str]


class UseDirectAmenity(CamplyModel):
    """
    UseDirect: Amenities
    """

    AmenityId: int
    Name: str
    ShortName: str
    AmenityType: int
    IsSearchable: bool
    Description: Optional[str]
    OrderBy: int
    IDate: datetime.datetime
    UDate: datetime.datetime
    ImagePath: Optional[str]
    UCashierName: Optional[str]
    UStoreId: Optional[int]
    IsADA: Optional[bool]
    Value: Optional[Any]


class UseDirectMetadata(CamplyModel):
    """
    Campground Metadata Responses
    """

    Message: str
    UnitCategories: List[UseDirectUnitCategory]
    NightlySleepingUnits: List[UseDirectNightlySleepingUnit]
    MinVehicleLengths: List[UseDirectMinVehicleLength]
    UnitTypesGroups: List[UseDirectUnitTypeGroup]
    PlaceHighlights: List[Any]
    AllAmenity: List[UseDirectAmenity]


class UseDirectCityPark(CamplyModel):
    """
    UseDirect: City Parks
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


class UseDirectFacilityMetadata(CamplyModel):
    """
    UseDirect: Facility Metadata
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
    FacilityBehaviourType: Optional[int]
    EnableCheckOccupancy: Optional[bool]
    IsTrail: Optional[bool]
    TimebaseMaxHours: Optional[int]
    TimebaseMinHours: Optional[int]
    TimebaseDuration: Optional[int]
