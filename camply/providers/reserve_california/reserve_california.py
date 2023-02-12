"""
ReserveCalifornia Provider
"""

from __future__ import annotations

import json
import logging
import pathlib
import sys
from datetime import date, datetime, timedelta
from typing import Any, Optional
from urllib import parse

import ratelimit
from rich import traceback

from camply.config import FileConfig
from camply.config.api_config import ReserveCaliforniaConfig
from camply.containers import AvailableCampsite, CampgroundFacility, RecreationArea
from camply.containers.reserve_california import (
    ReserveCaliforniaAvailabilityResponse,
    ReserveCaliforniaAvailabilitySlice,
    ReserveCaliforniaAvailabilityUnit,
    ReserveCaliforniaCityPark,
    ReserveCaliforniaDetailedPlace,
    ReserveCaliforniaFacilityMetadata,
    ReserveCaliforniaFacilityParent,
    ReserveCaliforniaMetadata,
    ReserveCaliforniaPlaceResult,
)
from camply.exceptions import CamplyError
from camply.providers.base_provider import BaseProvider
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)
traceback.install(show_locals=True)


class ReserveCalifornia(BaseProvider):
    """
    Camply Provider for Reserve California
    """

    reserve_california_city_parks: dict[int, ReserveCaliforniaCityPark] = {}
    reserve_california_rec_areas: dict[int, RecreationArea] = {}
    reserve_california_campgrounds: dict[int, CampgroundFacility] = {}
    reserve_california_unit_categories: dict[int, str] = {}
    reserve_california_unit_type_groups: dict[int, str] = {}
    metadata_refreshed: bool = False
    active_search: bool = False

    def search_recareas_api(self, query: str) -> list[RecreationArea]:
        """
        Retrieve Recreation Areas via the API

        Parameters
        ----------
        query: str

        Returns
        -------
        list[RecreationArea]
        """
        url = (
            f"{ReserveCaliforniaConfig.BASE_URL}/{ReserveCaliforniaConfig.SEARCH_ENDPOINT}/"
            f"{parse.quote(query)}"
        )
        response = self.session.get(url=url)
        response.raise_for_status()
        rec_areas = []
        for item in response.json():
            rc_facility = ReserveCaliforniaFacilityParent(**item)
            if rc_facility.IsActive is True:
                rec_area = RecreationArea(
                    recreation_area=rc_facility.Name,
                    recreation_area_id=rc_facility.PlaceId,
                    recreation_area_location="California",
                )
                rec_areas.append(rec_area)
                if (
                    rec_area.recreation_area_id
                    not in self.reserve_california_rec_areas.keys()
                ):
                    self.reserve_california_rec_areas[
                        rec_area.recreation_area_id
                    ] = rec_area
        return rec_areas

    def search_for_recreation_areas(
        self, query: Optional[str] = None, state: str = "CA", verbose: bool = True
    ) -> list[RecreationArea]:
        """
        Retrieve Recreation Areas

        Parameters
        ----------
        state: str
        query: str

        Returns
        -------
        list[RecreationArea]
        """
        if state.upper() != "CA":
            raise CamplyError("ReserveCalifornia doesn't support states outside CA")
        if query is None:
            logger.error(
                "You must provide a search string to search `ReserveCalifornia` Recreation Areas"
            )
            sys.exit(1)
        self.refresh_metadata()
        found_recareas = [
            rec_area
            for rec_area in self.reserve_california_rec_areas.values()
            if query.lower() in rec_area.recreation_area.lower()
            or query.lower() in rec_area.recreation_area_location.lower()
            or query.lower() in str(rec_area.description).lower()
        ]
        return found_recareas

    def find_campgrounds(
        self,
        search_string: Optional[str] = None,
        rec_area_id: Optional[list[int]] = None,
        state: str = "CA",
        verbose: bool = True,
        campground_id: Optional[list[int]] = None,
        **kwargs,
    ) -> list[CampgroundFacility]:
        """
        Search A Facility via Offline Metadata

        Parameters
        ----------
        rec_area_id: Optional[int]
        state: str = "CA"
        search_string: Optional[str]
        campground_id: Optional[list[int]]

        Returns
        -------
        list[CampgroundFacility]
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
        self.refresh_metadata()
        found_campgrounds: list[CampgroundFacility] = []
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
                if search_string.lower() in campground.recreation_area.lower()
                or search_string.lower() in campground.facility_name.lower()
            ]
        if verbose is True:
            logger.info(f"{len(found_campgrounds)} Matching Campgrounds Found")
            log_sorted_response(found_campgrounds)
        self.active_search = False
        return found_campgrounds

    def _search_for_campgrounds_api(
        self,
        place_id: int,
        start_date: Optional[date] = None,
    ) -> ReserveCaliforniaPlaceResult:
        """
        Search A Facility

        Parameters
        ----------
        place_id: int
        start_date: Optional[datetime.date]

        Returns
        -------
        ReserveCaliforniaPlaceResult
        """
        if start_date is None:
            start_date = datetime.today()
        url = f"{ReserveCaliforniaConfig.BASE_URL}/{ReserveCaliforniaConfig.PLACE_ENDPOINT}"
        data = {
            "PlaceId": place_id,
            "StartDate": start_date.strftime("%m-%d-%Y"),
        }
        resp = self.session.post(
            url=url, headers=self.json_headers, data=json.dumps(data)
        )
        resp.raise_for_status()
        results = ReserveCaliforniaPlaceResult(**resp.json())
        return results

    def get_campgrounds_api(
        self,
        rec_area_id: int,
    ) -> list[CampgroundFacility]:
        """
        Retrieve Facility IDs

        Parameters
        ----------
        rec_area_id: int

        Returns
        -------
        list[CampgroundFacility]
        """
        response: ReserveCaliforniaPlaceResult = self._search_for_campgrounds_api(
            place_id=rec_area_id, start_date=None
        )
        if response.SelectedPlace is None:
            raise ValueError(
                f"Could not find facilities in {rec_area_id} - try searching a different Rec Area."
            )
        campgrounds: list[CampgroundFacility] = []
        for _facility_id, facility in response.SelectedPlace.Facilities.items():
            if (
                response.SelectedPlace.PlaceId
                not in self.reserve_california_rec_areas.keys()
            ):
                self.reserve_california_rec_areas[
                    response.SelectedPlace.PlaceId
                ] = RecreationArea(
                    recreation_area_id=response.SelectedPlace.PlaceId,
                    recreation_area=response.SelectedPlace.Name,
                    recreation_area_location="California",
                )
            camp = CampgroundFacility(
                facility_id=facility.FacilityId,
                facility_name=facility.Name,
                recreation_area_id=response.SelectedPlace.PlaceId,
                recreation_area=response.SelectedPlace.Name,
                coordinates=(facility.Latitude, facility.Longitude),
            )
            campgrounds.append(camp)
        return campgrounds

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
        recreation_area_id = 678  # TODO: Lookup Rec Area
        booking_url = (
            f"{ReserveCaliforniaConfig.CAMPGROUND_URL}/Web/Default.aspx#!park/"
            f"{recreation_area_id}/{facility_id}"
        )
        facility = self.reserve_california_campgrounds[facility_id]
        recreation_area = self.reserve_california_rec_areas[facility.recreation_area_id]
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

    @ratelimit.sleep_and_retry
    @ratelimit.limits(calls=1, period=1)
    def get_campsites(
        self, campground_id: int, start_date: date, end_date: date
    ) -> list[AvailableCampsite]:
        """
        Get All Campsites

        Parameters
        ----------
        campground_id: int
        start_date: date
        end_date: date

        Returns
        -------
        list[AvailableCampsite]
        """
        if self.metadata_refreshed is False:
            self.refresh_metadata()
        data = {
            "FacilityId": campground_id,
            "StartDate": start_date.strftime(ReserveCaliforniaConfig.DATE_FORMAT),
            "EndDate": end_date.strftime(ReserveCaliforniaConfig.DATE_FORMAT),
        }
        url = f"{ReserveCaliforniaConfig.BASE_URL}/{ReserveCaliforniaConfig.AVAILABILITY_ENDPOINT}"
        response = self.session.post(
            url=url, data=json.dumps(data), headers=self.json_headers
        )
        response.raise_for_status()
        availability_response = ReserveCaliforniaAvailabilityResponse(**response.json())
        campsites: list[AvailableCampsite] = []
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

    def refresh_metadata(self) -> None:
        """
        Refresh All the Campground Metadata

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

    def _fetch_metadata_from_disk(
        self, file_path: pathlib.Path
    ) -> Optional[dict[Any, Any] | list[dict[Any, Any]]]:
        """
        Cache Metadata Locally and Invalidate after a day

        Parameters
        ----------
        file_path: pathlib.Path

        Returns
        -------
        Optional[dict[Any, Any]]
        """
        if file_path.exists() is False:
            return None
        else:
            modified_time = datetime.utcfromtimestamp(file_path.stat().st_mtime)
            current_time = datetime.utcnow()
            if (
                current_time - modified_time > timedelta(days=1)
                and self.active_search is False
            ):
                return None
            else:
                json_body: dict[Any, Any] = json.loads(
                    file_path.read_text(encoding="utf-8")
                )
                return json_body

    def _get_campground_metadata(self) -> ReserveCaliforniaMetadata:
        """
        Return Metadata for Campgrounds

        Returns
        -------
        ReserveCaliforniaMetadata
        """
        campground_metadata = self._fetch_metadata_from_disk(
            file_path=FileConfig.RESERVE_CALIFORNIA_FILTERS
        )
        if campground_metadata is None:
            url = f"{ReserveCaliforniaConfig.BASE_URL}/{ReserveCaliforniaConfig.METADATA_PREFIX}"
            resp = self.session.get(url=url)
            resp.raise_for_status()
            campground_metadata = resp.json()
            FileConfig.RESERVE_CALIFORNIA_FILTERS.write_text(
                json.dumps(campground_metadata, indent=2)
            )
        data = ReserveCaliforniaMetadata(**campground_metadata)
        self.reserve_california_unit_categories = {
            item.UnitCategoryId: item.UnitCategoryName for item in data.UnitCategories
        }
        self.reserve_california_unit_type_groups = {
            item.UnitTypesGroupId: item.UnitTypesGroupName
            for item in data.UnitTypesGroups
        }
        return data

    def _get_city_parks(self) -> dict[int, ReserveCaliforniaCityPark]:
        """
        Fetch Metadata On Every CityPark

        Returns
        -------
        dict[int, ReserveCaliforniaCityPark]
        """
        city_park_data = self._fetch_metadata_from_disk(
            file_path=FileConfig.RESERVE_CALIFORNIA_CITYPARKS
        )
        if city_park_data is None:
            url = f"{ReserveCaliforniaConfig.BASE_URL}/{ReserveCaliforniaConfig.CITYPARK_ENDPOINT}"
            resp = self.session.get(url=url)
            resp.raise_for_status()
            city_park_data: dict[str, dict[str, Any]] = resp.json()
            FileConfig.RESERVE_CALIFORNIA_CITYPARKS.write_text(
                json.dumps(city_park_data, indent=2)
            )
        self.reserve_california_city_parks: dict[int, ReserveCaliforniaCityPark] = {
            int(city_park_id): ReserveCaliforniaCityPark(**city_park_json)
            for city_park_id, city_park_json in city_park_data.items()
        }
        return self.reserve_california_city_parks

    def _get_places(self) -> dict[int, ReserveCaliforniaDetailedPlace]:
        """
        Fetch Metadata On Every Place

        Returns
        -------
        dict[int, ReserveCaliforniaDetailedPlace]
        """
        places_data = self._fetch_metadata_from_disk(
            file_path=FileConfig.RESERVE_CALIFORNIA_PLACES
        )
        if places_data is None:
            url = (
                f"{ReserveCaliforniaConfig.BASE_URL}/"
                f"{ReserveCaliforniaConfig.LIST_PLACES_ENDPOINT}"
            )
            resp = self.session.get(url=url)
            resp.raise_for_status()
            places_data: list[dict[str, Any]] = resp.json()
            FileConfig.RESERVE_CALIFORNIA_PLACES.write_text(
                json.dumps(places_data, indent=2)
            )
        places_validated = [
            ReserveCaliforniaDetailedPlace(**place_json) for place_json in places_data
        ]
        places_data_validated: dict[int, ReserveCaliforniaDetailedPlace] = {
            item.PlaceId: item for item in places_validated
        }
        self.reserve_california_rec_areas: dict[int, RecreationArea] = {
            place.PlaceId: RecreationArea(
                recreation_area=place.Name,
                recreation_area_id=place.PlaceId,
                recreation_area_location=f"{place.City.title()}, {place.State}",
                description=place.Description,
            )
            for place in places_data_validated.values()
        }
        return places_data_validated

    def _get_facilities(self) -> dict[int, ReserveCaliforniaFacilityMetadata]:
        """
        Fetch Metadata On Every Facility

        Returns
        -------
        dict[int, ReserveCaliforniaFacilityMetadata]
        """
        facilities_data = self._fetch_metadata_from_disk(
            file_path=FileConfig.RESERVE_CALIFORNIA_FACILITIES
        )
        if facilities_data is None:
            url = (
                f"{ReserveCaliforniaConfig.BASE_URL}/"
                f"{ReserveCaliforniaConfig.LIST_FACILITIES_ENDPOINT}"
            )
            resp = self.session.get(url=url)
            resp.raise_for_status()
            facilities_data: list[dict[str, Any]] = resp.json()
            FileConfig.RESERVE_CALIFORNIA_FACILITIES.write_text(
                json.dumps(facilities_data, indent=2)
            )
        if not isinstance(facilities_data, list):
            raise CamplyError("Unexpected data from facilities.json")
        facilities_validated = [
            ReserveCaliforniaFacilityMetadata(**facility_json)
            for facility_json in facilities_data
        ]
        facilities_data_validated: dict[int, ReserveCaliforniaFacilityMetadata] = {
            item.FacilityId: item for item in facilities_validated
        }
        self.reserve_california_campgrounds: dict[int, CampgroundFacility] = {}
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


if __name__ == "__main__":
    _this_file = pathlib.Path(__file__).resolve()
    city_park_file = _this_file.with_name("citypark.json")
    prov = ReserveCalifornia()
    prov.refresh_metadata()
