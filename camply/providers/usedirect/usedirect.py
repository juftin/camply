"""
UseDirect Provider
"""

import json
import logging
import pathlib
import sys
from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Union

import ratelimit
from pydantic import ValidationError

from camply.config import FileConfig
from camply.config.api_config import UseDirectConfig
from camply.containers import (
    AvailableCampsite,
    CampgroundFacility,
    CamplyModel,
    RecreationArea,
)
from camply.containers.usedirect import (
    UseDirectAvailabilityResponse,
    UseDirectAvailabilitySlice,
    UseDirectAvailabilityUnit,
    UseDirectCityPark,
    UseDirectDetailedPlace,
    UseDirectFacilityMetadata,
    UseDirectMetadata,
)
from camply.exceptions import CamplyError
from camply.providers.base_provider import BaseProvider
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)


class UseDirectError(CamplyError):
    """
    UseDirect Provider Error
    """


class UseDirectProvider(BaseProvider, ABC):
    """
    Camply Provider for UseDirect RDR Campgrounds
    """

    usedirect_city_parks: Dict[int, UseDirectCityPark] = {}
    usedirect_rec_areas: Dict[int, RecreationArea] = {}
    usedirect_campgrounds: Dict[int, CampgroundFacility] = {}
    usedirect_unit_categories: Dict[int, str] = {}
    usedirect_unit_type_groups: Dict[int, str] = {}
    usedirect_campsites: Dict[int, UseDirectAvailabilityUnit] = {}
    campsite_ids: List[int] = []
    metadata_refreshed: bool = False
    active_search: bool = False

    __offline_cache_dir__: Optional[pathlib.Path] = None

    rdr_path: str = "rdr"

    booking_path_params: bool = True
    booking_path: str = "Web/Default.aspx"

    @property
    @abstractmethod
    def base_url(self) -> str:
        """
        Base URL for the Provider
        """
        pass

    @property
    @abstractmethod
    def campground_url(self) -> str:
        """
        Campground URL for the Provider
        """
        pass

    @property
    @abstractmethod
    def state_code(self) -> str:
        """
        State Code for the Provider
        """
        pass

    @property
    def offline_cache_dir(self) -> pathlib.Path:
        """
        Offline Cache Directory
        """
        if self.__offline_cache_dir__ is None:
            return FileConfig.USEDIRECT_PROVIDER / self.__class__.__name__
        else:
            return self.__offline_cache_dir__

    def refresh_metadata(self) -> None:
        """
        Refresh All the Campground Metadata

        This is the way that this provider caches all of its metadata
        offline. It makes a number of GET requests and saves the entire output
        as JSON alongside the provider code itself (<subdomain>.usedirect.com):

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
        state: Optional[str] = None,
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
        if state is not None and state.upper() != self.state_code.upper():
            raise CamplyError(
                f"{self.__class__.__name__} doesn't support states outside {self.state_code}"
            )
        if query is None:
            logger.error(
                "You must provide a search string to search `UseDirect` Recreation Areas"
            )
            sys.exit(1)
        logger.info(f'Searching for Recreation Areas: "{query}"')
        self.refresh_metadata()
        found_recareas = [
            rec_area
            for rec_area in self.usedirect_rec_areas.values()
            if self._search_camply_model(query=query, model=rec_area) is True
        ]
        return found_recareas

    def find_campgrounds(
        self,
        search_string: Optional[str] = None,
        rec_area_id: Optional[List[int]] = None,
        state: Optional[str] = None,
        verbose: bool = True,
        campground_id: Optional[List[int]] = None,
        **kwargs: Any,
    ) -> List[CampgroundFacility]:
        """
        Search A Facility via Offline Metadata

        Parameters
        ----------
        rec_area_id: Optional[int]
        state: Optional[str]
        search_string: Optional[str]
        campground_id: Optional[List[int]]

        Returns
        -------
        List[CampgroundFacility]
        """
        self.active_search = True
        if state is not None and state.upper() != self.state_code:
            raise CamplyError(
                f"{self.__class__.__name__} doesn't support states outside {self.state_code}"
            )
        if campground_id is None:
            campground_id = []
        if rec_area_id is None:
            rec_area_id = []
        if all([rec_area_id == [], search_string is None, campground_id == []]):
            logger.error(
                "You must provide a search string, campground ID, or recreation area ID "
                "to search on UseDirect"
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
        campground_id: List[int],
        rec_area_id: List[int],
        search_string: Optional[str],
    ) -> List[CampgroundFacility]:
        """
        Filter a campground array

        Parameters
        ----------
        campground_id: List[int]
        rec_area_id: List[int]
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
                    for campground in self.usedirect_campgrounds.values()
                    if campground.facility_id == int(camp_id)
                ]
        elif len(rec_area_id) >= 1:
            for rec_area in rec_area_id:
                found_campgrounds += [
                    campground
                    for campground in self.usedirect_campgrounds.values()
                    if campground.recreation_area_id == int(rec_area)
                ]
        else:
            assert isinstance(search_string, str)
            found_campgrounds = [
                campground
                for campground in self.usedirect_campgrounds.values()
                if self._search_camply_model(query=search_string, model=campground)
                is True
            ]
        return found_campgrounds

    @ratelimit.sleep_and_retry
    @ratelimit.limits(calls=1, period=1)
    def get_campsites_response(
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
    ) -> UseDirectAvailabilityResponse:
        """
        Get Campsites from UseDirect

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
        UseDirectAvailabilityResponse
        """
        data = {
            "IsADA": is_ada,
            "MinVehicleLength": min_vehicle_length,
            "UnitCategoryId": unit_category_id,
            "StartDate": start_date.strftime(UseDirectConfig.DATE_FORMAT),
            "WebOnly": web_only,
            "UnitTypesGroupIds": []
            if unit_type_group_ids is None
            else unit_type_group_ids,
            "SleepingUnitId": sleeping_unit_id,
            "EndDate": end_date.strftime(UseDirectConfig.DATE_FORMAT),
            "UnitSort": unit_sort,
            "InSeasonOnly": in_season_only,
            "FacilityId": campground_id,
        }
        non_null_data = {
            key: value for key, value in data.items() if value not in [None, [], ""]
        }
        url = f"{self.base_url}/{self.rdr_path}/{UseDirectConfig.AVAILABILITY_ENDPOINT}"
        response = self.make_http_request_retry(
            url=url,
            method="POST",
            data=json.dumps(non_null_data),
            headers=self.json_headers,
        )
        response_json = response.json()
        try:
            return UseDirectAvailabilityResponse(**response_json)
        except ValidationError as e:
            raise
            error_message = (
                "Error Parsing UseDirect Availability Response "
                f"- Facility ID # {campground_id}."
            )
            if "Message" in response_json:
                error_message += " " + response_json["Message"]
            raise UseDirectError(error_message) from e

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
        Get Campsites from UseDirect

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
        availability_response = self.get_campsites_response(
            campground_id=campground_id,
            start_date=start_date,
            end_date=end_date,
            is_ada=is_ada,
            min_vehicle_length=min_vehicle_length,
            unit_category_id=unit_category_id,
            web_only=web_only,
            unit_type_group_ids=unit_type_group_ids,
            sleeping_unit_id=sleeping_unit_id,
            unit_sort=unit_sort,
            in_season_only=in_season_only,
        )
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
                campsite_available = campsite.availability_status == "Available"
                if campsite_available is True:
                    if (
                        len(self.campsite_ids) == 0
                        or campsite.campsite_id in self.campsite_ids
                    ):
                        campsites.append(campsite)
        return campsites

    def _get_available_campsite(
        self,
        availability_slice: UseDirectAvailabilitySlice,
        availability_response: UseDirectAvailabilityResponse,
        unit: UseDirectAvailabilityUnit,
    ) -> AvailableCampsite:
        """
        Create an AvailableCampsite Object from the Availability Grid Response

        Parameters
        ----------
        availability_slice: UseDirectAvailabilitySlice
        availability_response: UseDirectAvailabilityResponse
        unit: UseDirectAvailabilityUnit

        Returns
        -------
        AvailableCampsite
        """
        start_date = datetime.fromordinal(availability_slice.Date.toordinal())
        facility_id = availability_response.Facility.FacilityId
        facility = self.usedirect_campgrounds[facility_id]
        recreation_area = self.usedirect_rec_areas[facility.recreation_area_id]
        booking_url = f"{self.campground_url}/{self.booking_path}"
        if self.booking_path_params is True:
            booking_url = f"{booking_url}#!park/{recreation_area.recreation_area_id}/{facility_id}"
        if unit.UnitCategoryId is None:
            unit.UnitCategoryId = -1
        if unit.UnitTypeGroupId is None:
            unit.UnitTypeGroupId = -1
        campsite_type = self.usedirect_unit_categories.get(unit.UnitCategoryId, None)
        campsite_use_type = self.usedirect_unit_type_groups.get(
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
            logger.debug("Refreshing UseDirect Metadata: %s", file_path.name)
        return data

    def _get_campground_metadata(self) -> UseDirectMetadata:
        """
        Return Metadata for Campgrounds

        Returns
        -------
        UseDirectMetadata
        """
        metadata_file = self.offline_cache_dir.joinpath("filters.json")
        campground_metadata = self._fetch_metadata_from_disk(file_path=metadata_file)
        if campground_metadata is None:
            self.offline_cache_dir.mkdir(parents=True, exist_ok=True)
            url = f"{self.base_url}/{self.rdr_path}/{UseDirectConfig.METADATA_PREFIX}"
            resp = self.make_http_request_retry(url=url)
            resp.raise_for_status()
            campground_metadata = resp.json()
            metadata_file.write_text(json.dumps(campground_metadata, indent=2))
        data = UseDirectMetadata(**campground_metadata)
        self.usedirect_unit_categories = {
            item.UnitCategoryId: item.UnitCategoryName for item in data.UnitCategories
        }
        self.usedirect_unit_type_groups = {
            item.UnitTypesGroupId: item.UnitTypesGroupName
            for item in data.UnitTypesGroups
        }
        return data

    def _get_city_parks(self) -> Dict[int, UseDirectCityPark]:
        """
        Fetch Metadata On Every CityPark

        Returns
        -------
        Dict[int, UseDirectCityPark]
        """
        metadata_file = self.offline_cache_dir.joinpath("cityparks.json")
        city_park_data = self._fetch_metadata_from_disk(file_path=metadata_file)
        if city_park_data is None:
            url = f"{self.base_url}/{self.rdr_path}/{UseDirectConfig.CITYPARK_ENDPOINT}"
            resp = self.make_http_request_retry(url=url)
            resp.raise_for_status()
            city_park_data: Dict[str, Dict[str, Any]] = resp.json()
            metadata_file.write_text(json.dumps(city_park_data, indent=2))
        self.usedirect_city_parks: Dict[int, UseDirectCityPark] = {
            int(city_park_id): UseDirectCityPark(**city_park_json)
            for city_park_id, city_park_json in city_park_data.items()
            if city_park_json["Name"] is not None
        }
        return self.usedirect_city_parks

    def _get_places(self) -> Dict[int, UseDirectDetailedPlace]:
        """
        Fetch Metadata On Every Place

        Returns
        -------
        Dict[int, UseDirectDetailedPlace]
        """
        metadata_file = self.offline_cache_dir.joinpath("places.json")
        places_data = self._fetch_metadata_from_disk(file_path=metadata_file)
        if places_data is None:
            url = f"{self.base_url}/{self.rdr_path}/{UseDirectConfig.LIST_PLACES_ENDPOINT}"
            resp = self.make_http_request_retry(url=url)
            resp.raise_for_status()
            places_data: List[Dict[str, Any]] = resp.json()
            metadata_file.write_text(json.dumps(places_data, indent=2))
        places_validated = [
            UseDirectDetailedPlace(**place_json) for place_json in places_data
        ]
        places_data_validated: Dict[int, UseDirectDetailedPlace] = {
            item.PlaceId: item for item in places_validated
        }
        self.usedirect_rec_areas: Dict[int, RecreationArea] = {
            place.PlaceId: RecreationArea(
                recreation_area=place.Name,
                recreation_area_id=place.PlaceId,
                recreation_area_location=f"{place.City.title()}, {place.State}",
                description=place.Description,
            )
            for place in places_data_validated.values()
        }
        return places_data_validated

    def _get_facilities(self) -> Dict[int, UseDirectFacilityMetadata]:
        """
        Fetch Metadata On Every Facility

        Returns
        -------
        Dict[int, UseDirectFacilityMetadata]
        """
        metadata_file = self.offline_cache_dir.joinpath("facilities.json")
        facilities_data = self._fetch_metadata_from_disk(file_path=metadata_file)
        if facilities_data is None:
            url = f"{self.base_url}/{self.rdr_path}/{UseDirectConfig.LIST_FACILITIES_ENDPOINT}"
            resp = self.make_http_request_retry(url=url)
            resp.raise_for_status()
            facilities_data: List[Dict[str, Any]] = resp.json()
            metadata_file.write_text(json.dumps(facilities_data, indent=2))
        if not isinstance(facilities_data, list):
            raise CamplyError("Unexpected data from %s", metadata_file)
        facilities_validated = [
            UseDirectFacilityMetadata(**facility_json)
            for facility_json in facilities_data
        ]
        facilities_data_validated: Dict[int, UseDirectFacilityMetadata] = {
            item.FacilityId: item for item in facilities_validated
        }
        self.usedirect_campgrounds: Dict[int, CampgroundFacility] = {}
        for facility in facilities_data_validated.values():
            rec_area = self.usedirect_rec_areas.get(facility.PlaceId, None)
            if rec_area is not None:
                self.usedirect_campgrounds[facility.FacilityId] = CampgroundFacility(
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
            query.lower() in str(value).lower() for value in model.dict().values()
        )

    def get_campsites_per_facility(
        self, facility_id: int
    ) -> List[UseDirectAvailabilityUnit]:
        """
        Get Campsites Per Facility

        Parameters
        ----------
        facility_id: int

        Returns
        -------
        List[UseDirectAvailabilityUnit]
        """
        resp = self.get_campsites_response(
            campground_id=facility_id, start_date=date.today(), end_date=date.today()
        )
        campsites: List[UseDirectAvailabilityUnit] = list(resp.Facility.Units.values())
        for campsite in campsites:
            campsite.FacilityId = facility_id
        return campsites

    def get_campsite_metadata(
        self, facility_ids: List[int]
    ) -> Dict[int, UseDirectAvailabilityUnit]:
        """
        Get the Campsite Metadata

        Parameters
        ----------
        facility_ids: List[int]
            List of facility ids to fetch metadata for

        Returns
        -------
        Dict[int, UseDirectAvailabilityUnit]
        """
        campsites: Dict[int, UseDirectAvailabilityUnit] = {}
        for facility_id in facility_ids:
            found_campsites = self.get_campsites_per_facility(facility_id=facility_id)
            campsite_dict = {item.UnitId: item for item in found_campsites}
            campsites.update(campsite_dict)
        self.usedirect_campsites.update(campsites)
        return campsites

    def _prepare_facility_ids(
        self,
        recreation_area_ids: Optional[List[int]] = None,
        campground_ids: Optional[List[int]] = None,
    ) -> List[int]:
        """
        Prepare Facility Ids

        Parameters
        ----------
        recreation_area_ids: Optional[List[int]]
        campground_ids: Optional[List[int]]

        Returns
        -------
        List[int]
        """
        if not self.usedirect_campgrounds:
            self.refresh_metadata()
        recreation_area_ids = recreation_area_ids or []
        campground_ids = campground_ids or []
        facility_ids = []
        if len(recreation_area_ids) == 0 and len(campground_ids) == 0:
            raise CamplyError("Must specify either a recreation area or campground id")
        elif len(recreation_area_ids) > 0:
            logger.info(
                "Searching %s Recreation Areas for campgrounds",
                len(recreation_area_ids),
            )
            for recreation_area_id in recreation_area_ids:
                facility_ids += [
                    facility_id
                    for facility_id, facility in self.usedirect_campgrounds.items()
                    if facility.recreation_area_id == int(recreation_area_id)
                ]
        else:
            facility_ids = campground_ids
        facility_ids = [int(x) for x in facility_ids]
        return facility_ids

    def validate_campsites(self, campsites: List[int], facility_ids: List[int]) -> None:
        """
        Validate Campsites

        Parameters
        ----------
        campsites: List[int]

        Returns
        -------
        None
        """
        self.get_campsite_metadata(facility_ids=facility_ids)
        for campsite_id in campsites:
            if campsite_id not in self.usedirect_campsites:
                raise CamplyError(f"Campsite {campsite_id} not found")
            else:
                campsite = self.usedirect_campsites[campsite_id]
                logger.info("Searching Specific campsite: %s", campsite.Name)
        self.campsite_ids = list(campsites)
