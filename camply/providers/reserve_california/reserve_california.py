"""
ReserveCalifornia Provider
"""

import json
import logging
import pathlib
import sys
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import ratelimit

from camply.config import FileConfig
from camply.config.api_config import ReserveCaliforniaConfig
from camply.containers import (
    AvailableCampsite,
    CampgroundFacility,
    CamplyModel,
    RecreationArea,
)
from camply.containers.reserve_california import (
    ReserveCaliforniaAvailabilityResponse,
    ReserveCaliforniaAvailabilitySlice,
    ReserveCaliforniaAvailabilityUnit,
    ReserveCaliforniaCityPark,
    ReserveCaliforniaDetailedPlace,
    ReserveCaliforniaFacilityMetadata,
    ReserveCaliforniaMetadata,
)
from camply.exceptions import CamplyError
from camply.providers.base_provider import BaseProvider
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)


class ReserveCalifornia(BaseProvider):
    """
    Camply Provider for Reserve California
    """

    reserve_california_city_parks: Dict[int, ReserveCaliforniaCityPark] = {}
    reserve_california_rec_areas: Dict[int, RecreationArea] = {}
    reserve_california_campgrounds: Dict[int, CampgroundFacility] = {}
    reserve_california_unit_categories: Dict[int, str] = {}
    reserve_california_unit_type_groups: Dict[int, str] = {}
    metadata_refreshed: bool = False
    active_search: bool = False
    offline_cache_dir = FileConfig.RESERVE_CALIFORNIA_PROVIDER

    def refresh_metadata(self) -> None:
        """
        Refresh All the Campground Metadata

        This is the way that this provider caches all of its metadata
        offline. It makes a number of GET requests and saves the entire output
        as JSON alongside the provider code itself (calirdr.usedirect.com):

        - /rdr/rdr/search/filters
        - /rdr/rdr/search/citypark
        - /rdr/rdr/search/places
        - /rdr/rdr/search/facilities

        Returns
        -------
        None
        """
        if self.metadata_refreshed is False:
            self._get_campground_metadata()
            self._get_city_parks()
            self._get_places()
            self._get_facilities()
        self.metadata_refreshed = True

    def search_for_recreation_areas(
        self,
        query: Optional[str] = None,
        state: str = "CA",
    ) -> List[RecreationArea]:
        """
        Retrieve Recreation Areas

        Parameters
        ----------
        state: str
        query: str

        Returns
        -------
        List[RecreationArea]
        """
        if state.upper() != "CA":
            raise CamplyError("ReserveCalifornia doesn't support states outside CA")
        if query is None:
            logger.error(
                "You must provide a search string to search `ReserveCalifornia` Recreation Areas"
            )
            sys.exit(1)
        logger.info(f'Searching for Recreation Areas: "{query}"')
        self.refresh_metadata()
        found_recareas = [
            rec_area
            for rec_area in self.reserve_california_rec_areas.values()
            if self._search_camply_model(query=query, model=rec_area) is True
        ]
        return found_recareas

    def find_campgrounds(
        self,
        search_string: Optional[str] = None,
        rec_area_id: Optional[List[int]] = None,
        state: str = "CA",
        verbose: bool = True,
        campground_id: Optional[List[int]] = None,
        **kwargs,
    ) -> List[CampgroundFacility]:
        """
        Search A Facility via Offline Metadata

        Parameters
        ----------
        rec_area_id: Optional[int]
        state: str = "CA"
        search_string: Optional[str]
        campground_id: Optional[List[int]]

        Returns
        -------
        List[CampgroundFacility]
        """
        self.active_search = True
        if state.upper() != "CA":
            raise CamplyError("ReserveCalifornia doesn't support states outside CA")
        if campground_id is None:
            campground_id = []
        if rec_area_id is None:
            rec_area_id = []
        if all([rec_area_id == [], search_string is None, campground_id == []]):
            logger.error(
                "You must provide a search string, campground ID, or recreation area ID "
                "to search on ReserveCalifornia"
            )
            sys.exit(1)
        if search_string is not None:
            logger.info(f'Searching for Campgrounds: "{search_string}"')
        self.refresh_metadata()
        found_campgrounds = self._search_for_campgrounds(
            campground_id=campground_id,
            rec_area_id=rec_area_id,
            search_string=search_string,
        )
        if verbose is True:
            logger.info(f"{len(found_campgrounds)} Matching Campgrounds Found")
            log_sorted_response(found_campgrounds)
        self.active_search = False
        return found_campgrounds

    def _search_for_campgrounds(
        self,
        campground_id: Optional[List[int]],
        rec_area_id: Optional[List[int]],
        search_string: Optional[str],
    ) -> List[CampgroundFacility]:
        """
        Filter a campground array

        Parameters
        ----------
        campground_id: Optional[List[int]]
        rec_area_id: Optional[List[int]]
        search_string: Optional[str]

        Returns
        -------
        List[CampgroundFacility]
        """
        found_campgrounds: List[CampgroundFacility] = []
        if len(campground_id) >= 1:
            for camp_id in campground_id:
                found_campgrounds += [
                    campground
                    for campground in self.reserve_california_campgrounds.values()
                    if campground.facility_id == int(camp_id)
                ]
        elif len(rec_area_id) >= 1:
            for rec_area in rec_area_id:
                found_campgrounds += [
                    campground
                    for campground in self.reserve_california_campgrounds.values()
                    if campground.recreation_area_id == int(rec_area)
                ]
        else:
            assert isinstance(search_string, str)
            found_campgrounds = [
                campground
                for campground in self.reserve_california_campgrounds.values()
                if self._search_camply_model(query=search_string, model=campground)
                is True
            ]
        return found_campgrounds

    @ratelimit.sleep_and_retry
    @ratelimit.limits(calls=1, period=1)
    def get_campsites(
        self,
        campground_id: int,
        start_date: Union[datetime, date],
        end_date: Union[datetime, date],
        is_ada: Optional[bool] = None,
        min_vehicle_length: Optional[int] = None,
        unit_category_id: Optional[int] = None,
        web_only: Optional[bool] = True,
        unit_type_group_ids: Optional[List[int]] = None,
        sleeping_unit_id: Optional[int] = None,
        unit_sort: Optional[str] = "orderby",
        in_season_only: Optional[bool] = True,
    ) -> List[AvailableCampsite]:
        """
        Get Campsites from ReserveCalifornia

        Parameters
        ----------
        campground_id: int
            Facility ID of the campground
        start_date: Union[datetime, date]
            Search Start Date
        end_date: Union[datetime, date]
            Search End Date
        is_ada: Optional[bool]
            Search for ADA sites
        min_vehicle_length: Optional[int]
            Minimum Vehicle Length - defaults to 0 which doesn't filter
        unit_category_id: Optional[int]
            Unit Category ID (typically 0)
        web_only: Optional[bool]
            Search for sights bookable online
        unit_type_group_ids: Optional[List[int]]
            UnitTypeGroupIds - Search Param
        sleeping_unit_id: Optional[int]
            SleepingUnitId - search param
        unit_sort: Optional[str]
            Sort Order
        in_season_only: Optional[bool]
            Searching for in-season only campgrounds

        Returns
        -------
        List[AvailableCampsite]
        """
        self.refresh_metadata()
        data = {
            "IsADA": is_ada,
            "MinVehicleLength": min_vehicle_length,
            "UnitCategoryId": unit_category_id,
            "StartDate": start_date.strftime(ReserveCaliforniaConfig.DATE_FORMAT),
            "WebOnly": web_only,
            "UnitTypesGroupIds": []
            if unit_type_group_ids is None
            else unit_type_group_ids,
            "SleepingUnitId": sleeping_unit_id,
            "EndDate": end_date.strftime(ReserveCaliforniaConfig.DATE_FORMAT),
            "UnitSort": unit_sort,
            "InSeasonOnly": in_season_only,
            "FacilityId": campground_id,
        }
        non_null_data = {
            key: value for key, value in data.items() if value not in [None, [], ""]
        }
        url = f"{ReserveCaliforniaConfig.BASE_URL}/{ReserveCaliforniaConfig.AVAILABILITY_ENDPOINT}"
        response = self.session.post(
            url=url, data=json.dumps(non_null_data), headers=self.json_headers
        )
        response.raise_for_status()
        availability_response = ReserveCaliforniaAvailabilityResponse(**response.json())
        campsites: List[AvailableCampsite] = []
        if availability_response.Facility.Units is None:
            return campsites
        for _campground_unit_id, unit in availability_response.Facility.Units.items():
            for _slice_date, availability_slice in unit.Slices.items():
                campsite = self._get_available_campsite(
                    availability_slice=availability_slice,
                    availability_response=availability_response,
                    unit=unit,
                )
                if campsite.availability_status == "Available":
                    campsites.append(campsite)
        return campsites

    def _get_available_campsite(
        self,
        availability_slice: ReserveCaliforniaAvailabilitySlice,
        availability_response: ReserveCaliforniaAvailabilityResponse,
        unit: ReserveCaliforniaAvailabilityUnit,
    ) -> AvailableCampsite:
        """
        Create an AvailableCampsite Object from the Availability Grid Response

        Parameters
        ----------
        availability_slice: ReserveCaliforniaAvailabilitySlice
        availability_response: ReserveCaliforniaAvailabilityResponse
        unit: ReserveCaliforniaAvailabilityUnit

        Returns
        -------
        AvailableCampsite
        """
        start_date = datetime.fromordinal(availability_slice.Date.toordinal())
        facility_id = availability_response.Facility.FacilityId
        facility = self.reserve_california_campgrounds[facility_id]
        recreation_area = self.reserve_california_rec_areas[facility.recreation_area_id]
        booking_url = (
            f"{ReserveCaliforniaConfig.CAMPGROUND_URL}/Web/Default.aspx#!park/"
            f"{recreation_area.recreation_area_id}/{facility_id}"
        )
        if unit.UnitCategoryId is None:
            unit.UnitCategoryId = -1
        if unit.UnitTypeGroupId is None:
            unit.UnitTypeGroupId = -1
        campsite_type = self.reserve_california_unit_categories.get(
            unit.UnitCategoryId, None
        )
        campsite_use_type = self.reserve_california_unit_type_groups.get(
            unit.UnitTypeGroupId, None
        )
        campsite = AvailableCampsite(
            campsite_id=unit.UnitId,
            booking_date=start_date,
            booking_end_date=start_date + timedelta(days=1),
            booking_nights=1,
            campsite_site_name=unit.Name,
            availability_status=(
                "Available" if availability_slice.IsFree is True else "Unavailable"
            ),
            recreation_area=recreation_area.recreation_area,
            recreation_area_id=facility.recreation_area_id,
            facility_name=facility.facility_name,
            facility_id=facility.facility_id,
            booking_url=booking_url,
            campsite_occupancy=(0, 1),
            campsite_type=campsite_type,
            campsite_use_type=campsite_use_type,
        )
        return campsite

    def _fetch_metadata_from_disk(
        self, file_path: pathlib.Path
    ) -> Optional[Union[Dict[Any, Any], List[Dict[Any, Any]]]]:
        """
        Cache Metadata Locally and Invalidate after a day

        Parameters
        ----------
        file_path: pathlib.Path

        Returns
        -------
        Optional[Dict[Any, Any]]
        """
        if file_path.exists() is False:
            data = None
        else:
            modified_time = datetime.utcfromtimestamp(file_path.stat().st_mtime)
            current_time = datetime.utcnow()
            if (
                current_time - modified_time > timedelta(days=1)
                and self.active_search is False
            ):
                data = None
            else:
                json_body: Dict[Any, Any] = json.loads(
                    file_path.read_text(encoding="utf-8")
                )
                data = json_body
        if data is None:
            logger.debug("Refreshing ReserveCalifornia Metadata: %s", file_path.name)
        return data

    def _get_campground_metadata(self) -> ReserveCaliforniaMetadata:
        """
        Return Metadata for Campgrounds

        Returns
        -------
        ReserveCaliforniaMetadata
        """
        metadata_file = self.offline_cache_dir.joinpath("filters.json")
        campground_metadata = self._fetch_metadata_from_disk(file_path=metadata_file)
        if campground_metadata is None:
            url = f"{ReserveCaliforniaConfig.BASE_URL}/{ReserveCaliforniaConfig.METADATA_PREFIX}"
            resp = self.session.get(url=url)
            resp.raise_for_status()
            campground_metadata = resp.json()
            metadata_file.write_text(json.dumps(campground_metadata, indent=2))
        data = ReserveCaliforniaMetadata(**campground_metadata)
        self.reserve_california_unit_categories = {
            item.UnitCategoryId: item.UnitCategoryName for item in data.UnitCategories
        }
        self.reserve_california_unit_type_groups = {
            item.UnitTypesGroupId: item.UnitTypesGroupName
            for item in data.UnitTypesGroups
        }
        return data

    def _get_city_parks(self) -> Dict[int, ReserveCaliforniaCityPark]:
        """
        Fetch Metadata On Every CityPark

        Returns
        -------
        Dict[int, ReserveCaliforniaCityPark]
        """
        metadata_file = self.offline_cache_dir.joinpath("cityparks.json")
        city_park_data = self._fetch_metadata_from_disk(file_path=metadata_file)
        if city_park_data is None:
            url = f"{ReserveCaliforniaConfig.BASE_URL}/{ReserveCaliforniaConfig.CITYPARK_ENDPOINT}"
            resp = self.session.get(url=url)
            resp.raise_for_status()
            city_park_data: Dict[str, Dict[str, Any]] = resp.json()
            metadata_file.write_text(json.dumps(city_park_data, indent=2))
        self.reserve_california_city_parks: Dict[int, ReserveCaliforniaCityPark] = {
            int(city_park_id): ReserveCaliforniaCityPark(**city_park_json)
            for city_park_id, city_park_json in city_park_data.items()
        }
        return self.reserve_california_city_parks

    def _get_places(self) -> Dict[int, ReserveCaliforniaDetailedPlace]:
        """
        Fetch Metadata On Every Place

        Returns
        -------
        Dict[int, ReserveCaliforniaDetailedPlace]
        """
        metadata_file = self.offline_cache_dir.joinpath("places.json")
        places_data = self._fetch_metadata_from_disk(file_path=metadata_file)
        if places_data is None:
            url = (
                f"{ReserveCaliforniaConfig.BASE_URL}/"
                f"{ReserveCaliforniaConfig.LIST_PLACES_ENDPOINT}"
            )
            resp = self.session.get(url=url)
            resp.raise_for_status()
            places_data: List[Dict[str, Any]] = resp.json()
            metadata_file.write_text(json.dumps(places_data, indent=2))
        places_validated = [
            ReserveCaliforniaDetailedPlace(**place_json) for place_json in places_data
        ]
        places_data_validated: Dict[int, ReserveCaliforniaDetailedPlace] = {
            item.PlaceId: item for item in places_validated
        }
        self.reserve_california_rec_areas: Dict[int, RecreationArea] = {
            place.PlaceId: RecreationArea(
                recreation_area=place.Name,
                recreation_area_id=place.PlaceId,
                recreation_area_location=f"{place.City.title()}, {place.State}",
                description=place.Description,
            )
            for place in places_data_validated.values()
        }
        return places_data_validated

    def _get_facilities(self) -> Dict[int, ReserveCaliforniaFacilityMetadata]:
        """
        Fetch Metadata On Every Facility

        Returns
        -------
        Dict[int, ReserveCaliforniaFacilityMetadata]
        """
        metadata_file = self.offline_cache_dir.joinpath("facilities.json")
        facilities_data = self._fetch_metadata_from_disk(file_path=metadata_file)
        if facilities_data is None:
            url = (
                f"{ReserveCaliforniaConfig.BASE_URL}/"
                f"{ReserveCaliforniaConfig.LIST_FACILITIES_ENDPOINT}"
            )
            resp = self.session.get(url=url)
            resp.raise_for_status()
            facilities_data: List[Dict[str, Any]] = resp.json()
            metadata_file.write_text(json.dumps(facilities_data, indent=2))
        if not isinstance(facilities_data, list):
            raise CamplyError("Unexpected data from %s", metadata_file)
        facilities_validated = [
            ReserveCaliforniaFacilityMetadata(**facility_json)
            for facility_json in facilities_data
        ]
        facilities_data_validated: Dict[int, ReserveCaliforniaFacilityMetadata] = {
            item.FacilityId: item for item in facilities_validated
        }
        self.reserve_california_campgrounds: Dict[int, CampgroundFacility] = {}
        for facility in facilities_data_validated.values():
            rec_area = self.reserve_california_rec_areas.get(facility.PlaceId, None)
            if rec_area is not None:
                self.reserve_california_campgrounds[
                    facility.FacilityId
                ] = CampgroundFacility(
                    facility_name=facility.Name,
                    facility_id=facility.FacilityId,
                    recreation_area_id=facility.PlaceId,
                    recreation_area=rec_area.recreation_area,
                )
        return facilities_data_validated

    @classmethod
    def _search_camply_model(cls, query: str, model: CamplyModel) -> bool:
        """
        Search a Camply Model

        Parameters
        ----------
        query: str
        model: CamplyModel

        Returns
        -------
        bool
        """
        return any(
            [query.lower() in str(value).lower() for value in model.dict().values()]
        )
