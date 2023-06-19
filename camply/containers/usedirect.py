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

    FutureBookingStarts: Optional[datetime.datetime]
    FutureBookingEnds: Optional[datetime.datetime]
    MinimumStay: Optional[int]
    MaximumStay: Optional[int]
    IsRestrictionValid: Optional[bool]
    Time: Optional[str]


class UseDirectUnitType(CamplyModel):
    """
    UseDirect: Unit Types
    """

    UnitTypeId: int
    UseType: int
    Name: str
    Available: bool
    AvailableFiltered: Optional[bool]
    UnitCategoryId: Optional[int]
    UnitTypeGroupId: Optional[int]
    MaxVehicleLength: Optional[int]
    HasAda: Optional[bool]
    Restrictions: Optional[Any]
    AvailableCount: Optional[int]


class UseDirectAvailabilitySlice(CamplyModel):
    """
    Slice of Availability per Date
    """

    Date: datetime.date
    IsFree: bool
    IsBlocked: Optional[bool]
    IsWalkin: Optional[bool]
    ReservationId: Optional[int]
    Lock: Any
    MinStay: Optional[int]
    IsReservationDraw: Optional[bool]


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
    MapInfo: Optional[Dict[str, Any]] = {}
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
    Slices: Optional[Dict[datetime.datetime, UseDirectAvailabilitySlice]] = {}
    StartTime: Any
    EndTime: Any
    FacilityId: Optional[int]


class UseDirectFacility(CamplyModel):
    """
    Campground Representation for UseDirect
    """

    FacilityId: int
    Name: Optional[str]
    Description: Optional[str]
    RateMessage: Optional[str]
    FacilityType: Optional[int]
    FacilityTypeNew: Optional[int]
    InSeason: Optional[bool]
    Available: Optional[bool]
    AvailableFiltered: Optional[bool]
    Restrictions: Optional[UseDirectRestrictions]
    Latitude: Optional[float]
    Longitude: Optional[float]
    Category: Optional[str]
    EnableCheckOccupancy: Optional[bool]
    AvailableOccupancy: Any
    FacilityAllowWebBooking: Optional[bool]
    UnitTypes: Optional[Dict[int, UseDirectUnitType]] = {}
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
    Description: Optional[str]
    HasAlerts: Optional[bool]
    IsFavourite: Optional[bool]
    Allhighlights: Optional[str]
    Url: Optional[str]
    ImageUrl: Optional[str]
    BannerUrl: Optional[str]
    ParkSize: Optional[str]
    Latitude: Optional[float]
    Longitude: Optional[float]
    TimeZone: Optional[str]
    TimeStamp: Optional[datetime.datetime]
    MilesFromSelected: Optional[int]
    Available: bool
    AvailableFiltered: Optional[bool]
    ParkCategoryId: Optional[int]
    ParkActivity: Optional[int]
    ParkPopularity: Optional[int]
    AvailableUnitCount: Optional[int]
    Restrictions: Optional[UseDirectRestrictions]
    Facilities: Optional[Dict[int, UseDirectFacility]] = {}
    IsAvailableForGreatwalk: Optional[bool]
    FacilityDefaultZoom: Optional[int]


class UseDirectDetailedPlace(CamplyModel):
    """
    https://calirdr.usedirect.com/RDR/rdr/fd/places
    """

    PlaceId: int
    Name: str
    Description: Optional[str]
    ParkSize: Optional[str]
    Latitude: Optional[float]
    Longitude: Optional[float]
    ParkCategoryId: Optional[int]
    ParkActivity: Optional[int]
    ParkPopularity: Optional[int]
    IsAvailableForGreatwalk: Optional[bool]
    FacilityDefaultZoom: Optional[int]
    RegionId: Optional[int]
    ShortName: Optional[str]
    OrderBy: Optional[int]
    AllowWebBooking: Optional[bool]
    InventoryLocking: Optional[bool]
    InventoryLockDuration: Optional[int]
    UsePrepend: Optional[bool]
    PrependCode: Optional[str]
    Address1: Optional[str]
    Address2: Optional[str]
    City: Optional[str]
    State: Optional[str]
    Zip: Optional[str]
    VoicePhone: Optional[str]
    UDate: datetime.datetime
    UserId: Optional[int]
    RowGuid: Optional[str]
    IsWebViewable: Optional[bool]
    WeekdayCheckdays: Optional[int]
    WeekendCheckdays: Optional[int]


class UseDirectAvailabilityFacility(UseDirectFacility):
    """
    UseDirect: Facility w/ Availability
    """

    FacilityMapSize: Optional[bool]
    FacilityImage: Optional[str]
    FacilityImageVBT: Optional[str]
    DatesInSeason: Optional[int]
    DatesOutOfSeason: Optional[int]
    SeasonDates: Optional[Dict[datetime.datetime, bool]] = {}
    TrafficStatuses: Optional[Dict[str, Any]] = {}
    UnitCount: Optional[int]
    AvailableUnitCount: Optional[int]
    SliceCount: Optional[int]
    AvailableSliceCount: Optional[int]
    TimebaseMaxHours: Optional[int]
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
    Filters: Optional[Dict[str, Any]] = {}
    UnitTypeId: int
    StartDate: Optional[datetime.date]
    EndDate: Optional[datetime.date]
    NightsRequested: Optional[int]
    NightsActual: Optional[int]
    TodayDate: Optional[datetime.date]
    TimeZone: Optional[str]
    TimeStamp: Optional[datetime.datetime]
    MinDate: Optional[datetime.date]
    MaxDate: Optional[datetime.date]
    AvailableUnitsOnly: Optional[bool]
    UnitSort: Optional[str]
    TimeGrid: Optional[bool]
    ForUnit: Optional[bool]
    UnitId: Optional[int]
    TimeBetween: Optional[str]
    TimeBetweenEval: Optional[str]
    Facility: Optional[UseDirectAvailabilityFacility]


class UseDirectUnitCategory(CamplyModel):
    """
    UseDirect: Unit Categories
    """

    UnitCategoryId: int
    UnitCategoryName: str
    HasEquipment: Optional[bool]
    Icon: Optional[str]


class UseDirectNightlySleepingUnit(CamplyModel):
    """
    UseDirect: Nightly Sleeping Units
    """

    UnitCategoryId: int
    SleepingUnitId: int
    SleepingUnitName: str
    IsWheeled: Optional[bool]
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
    AmenityType: Optional[str]
    IsSearchable: Optional[bool]
    Description: Optional[str]
    OrderBy: Optional[int]
    IDate: Optional[datetime.datetime]
    UDate: Optional[datetime.datetime]
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
    UnitCategories: Optional[List[UseDirectUnitCategory]] = []
    NightlySleepingUnits: Optional[List[UseDirectNightlySleepingUnit]] = []
    MinVehicleLengths: Optional[List[UseDirectMinVehicleLength]] = []
    UnitTypesGroups: Optional[List[UseDirectUnitTypeGroup]] = []
    PlaceHighlights: Optional[List[Any]] = []
    AllAmenity: Optional[List[UseDirectAmenity]] = []


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
    ParkSize: Optional[str]
    PlaceId: int


class UseDirectFacilityMetadata(CamplyModel):
    """
    UseDirect: Facility Metadata
    """

    FacilityId: int
    RegionId: Optional[int]
    PlaceId: int
    Name: str
    ShortName: Optional[str]
    Description: Optional[str]
    OrderBy: Optional[int]
    FacilityType: Optional[int]
    UsePrepend: Optional[bool]
    PrependCode: Optional[str]
    AllowWebBooking: Optional[bool]
    AutoOpenInventory: Optional[bool]
    UDate: Optional[datetime.datetime]
    RowGuid: Optional[str]
    FacilityTypeNew: Optional[int]
    MaxPersonOccupancy: Optional[int]
    IsAvailableForGroup: Optional[bool]
    IsAvailableForEducationalGroup: Optional[bool]
    IsAvailableForCto: Optional[bool]
    IsCaptcha: Optional[bool]
    FacilityBehaviourType: Optional[int]
    EnableCheckOccupancy: Optional[bool]
    IsTrail: Optional[bool]
    TimebaseMaxHours: Optional[int]
    TimebaseMinHours: Optional[int]
    TimebaseDuration: Optional[int]
