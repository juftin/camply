"""
Recreation.gov Implementation for Tours.
"""

import json
import logging
import functools
from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import requests

from camply.config import RecreationBookingConfig, RIDBConfig
from camply.containers import AvailableCampsite
from camply.containers.api_responses import (
    RecDotGovSearchResponse,
    RecDotGovSearchResult,
    RecDotGovPermitMapping,
    RecDotGovPermitMappingResponse,
    PermitEntranceResponse,
    PermitEntranceForFacilityResponse,
    PermitMonthlyAvailabilityResponse,
)
from camply.containers.base_container import CamplyModel, RecDotGovEquipment
from camply.providers.base_provider import ProviderSearchError
from camply.providers.recreation_dot_gov.recdotgov_provider import RecreationDotGovBase
from camply.utils import api_utils

logger = logging.getLogger(__name__)


class RecreationDotGovPermit(RecreationDotGovBase):
    """
    Recreation.gov Implementation for Permits
    """

    api_response_class = PermitEntranceResponse
    api_search_result_class = RecDotGovSearchResult
    api_search_result_key = "entity_id"
    api_search_fq = "entity_type:permit"
    api_base_path = RecreationBookingConfig.API_BASE_PATH
    facility_type = RIDBConfig.PERMIT_FACILITY_FIELD_QUALIFIER
    activity_name = None  # Activity Name Should't Be Propogated to Query Parameters
    resource_api_path = RIDBConfig.PERMIT_ENTRANCE_API_PATH
    booking_url = "https://www.recreation.gov/permits/{facility_id}/registration/detailed-availability"

    facility_permit_map = {
        # Yosemite National Park Wilderness Permits
        445859: {
            44585904: "Beehive Meadows",
            44585907: "Cathedral Lakes",
            44585914: "Glen Aulin",
            44585915: "Glen Aulin -> Cold Canyon/Waterwheel (pass through)",
            44585917: "Happy Isles -> Little Yosemite Valley (No Donohue Pass)",
            44585918: "Happy Isles -> Past LYV (Donohue Pass Eligible)",
            44585921: "Lyell Canyon (Donohue Pass Eligible)",
            44585924: "May Lake",
            44585940: "Rafferty Creek -> Vogelsang",
            44585945: "Sunrise",
            44585956: "Young Lakes via Glen Trail",
        }
    }

    @functools.lru_cache(maxsize=None)
    def _permit_mapping(self) -> RecDotGovPermitMapping:
        mapping_url = api_utils.generate_url(
            scheme=RecreationBookingConfig.API_SCHEME,
            netloc=RecreationBookingConfig.API_NET_LOC,
            path="api/permitcontent/permitmapping",
        )
        response = self.make_recdotgov_request_retry(url=mapping_url)
        data = json.loads(response.content)
        return RecDotGovPermitMappingResponse(**data).payload

    def _permit_api_path(self, permit_id: int):
        permit_mapping = self._permit_mapping()

        api_mapping = [
            (permit_mapping.day_use_permit_ids, "permitdayuse"),
            (permit_mapping.hunting_permit_ids, "huntingpermit"),
            (permit_mapping.itinerary_permit_ids, "permititinerary"),
            (permit_mapping.land_permit_ids, "permitinyo"),
            (permit_mapping.water_permit_ids, "permitwbe"),
            (permit_mapping.early_access_permit_ids, "permitissuance"),
            (permit_mapping.lottery_permit_ids, "permitissuance"),
            (permit_mapping.vehicle_permit_ids, "permitissuance"),
        ]

        permit_id = str(permit_id)
        for k, v in api_mapping:
            if permit_id in k:
                return v

        return "permits"

    def paginate_recdotgov_campsites(
        self, facility_id: int, equipment: Optional[List[str]] = None
    ) -> List[PermitEntranceResponse]:
        """
        Paginate through the RecDotGov Campsite Metadata
        """
        results = 0
        continue_paginate = True
        params = {
            "offset": 0,
            "limit": 1000,
        }
        path = f"facilities/{facility_id}/{self.resource_api_path}"

        permits: List[PermitEntranceResponse] = []
        while continue_paginate is True:
            data = self.get_ridb_data(path, params)
            response = PermitEntranceForFacilityResponse(**data)

            permits += response.RECDATA
            results += response.METADATA["RESULTS"]["CURRENT_COUNT"]
            params.update(offset=results)
            if results == response.METADATA["RESULTS"]["TOTAL_COUNT"]:
                continue_paginate = False
        
        if facility_id in self.facility_permit_map:
            permit_map = self.facility_permit_map[facility_id]
            for permit_id, name in permit_map.items():
                permits.append(PermitEntranceResponse(
                    PermitEntranceID=permit_id,
                    FacilityID=facility_id,
                    PermitEntranceName=name,
                    PermitEntranceDescription='',
                    District='',
                    Town='',
                    PermitEntranceAccessible=True,
                    Longitude=0.0,
                    Latitude=0.0,
                    CreatedDate=date.today(),
                    LastUpdatedDate=date.today(),
                    ATTRIBUTES=[],
                    ZONES=[],
                ))

        return permits

    def get_internal_campsites(
        self, facility_ids: List[int]
    ) -> List[PermitEntranceResponse]:
        """
        Retrieve all of the underlying Campsites to Search
        """
        all_campsites: List[PermitEntranceResponse] = []
        for facility_id in facility_ids:
            all_campsites += self.paginate_recdotgov_campsites(facility_id=facility_id)
        return all_campsites

    def get_internal_campsite_metadata(self, facility_ids: List[int]) -> pd.DataFrame:
        """
        Retrieve Metadata About all of the underlying Campsites to Search
        """
        all_campsites: List[PermitEntranceResponse] = self.get_internal_campsites(
            facility_ids=facility_ids
        )
        all_campsite_df = pd.DataFrame(
            [item.dict() for item in all_campsites],
            columns=PermitEntranceResponse.__fields__,
        )
        all_campsite_df.set_index("PermitEntranceID", inplace=True)

        # Special case for Mt. Whitney
        all_campsite_df[all_campsite_df["FacilityID"] == 233260]["FacilityID"] = 445860

        return all_campsite_df

    def make_recdotgov_availability_request(
        self,
        facility_id: int,
        month: datetime,
    ) -> requests.Response:
        """
        Make a request to the RecreationDotGov API

        Parameters
        ----------
        facility_id
        month

        Returns
        -------
        requests.Response
        """

        # Special case for Mt. Whitney
        if facility_id == 233260:
            facility_id = 445860

        permit_api_path = self._permit_api_path(facility_id)

        query_url = api_utils.generate_url(
            scheme=RecreationBookingConfig.API_SCHEME,
            netloc=RecreationBookingConfig.API_NET_LOC,
            path=f"api/{permit_api_path}/{facility_id}/availability",
        )
        query_params = {
            "year": month.strftime("%Y"),
            "start_date": month.strftime("%Y-%m-%d"),
            "category": "non-commercial",
        }
        response = self.make_recdotgov_request(
            method="GET",
            url=query_url,
            params=query_params,
        )
        return response

    @classmethod
    def make_campsite_availability_fields(
        cls,
        permit_entrance_id: int,
        facility_id: int,
        booking_date: datetime.date,
        campsite_metadata: pd.DataFrame,
    ) -> Dict[str, Any]:
        """
        Generate a dictionary of fields to be used in a campsite container.

        Parameters
        ----------
        permit_entrance_id: int
        booking_url_vars: Dict[str, str]
        booking_date: datetime.date
        campsite_metadata: pd.DataFrame

        Returns
        -------
        Dict[str, Any]
        """
        booking_date = datetime.combine(booking_date, time.min)
        try:
            permit_entrance_name = campsite_metadata.at[
                permit_entrance_id, "PermitEntranceName"
            ]
        except LookupError:
            permit_entrance_name = f"Permit Entrance #{permit_entrance_id}"
        try:
            loop_name = campsite_metadata.at[
                permit_entrance_id, "PermitEntranceDescription"
            ]
        except LookupError:
            loop_name = "Description not available"
        try:
            use_type = campsite_metadata.at[permit_entrance_id, "PermitEntranceType"]
        except LookupError:
            use_type = "Time zone not available"
        return {
            "booking_url": cls.booking_url.format(facility_id=facility_id),  # type: ignore
            "booking_date": booking_date,
            "booking_end_date": booking_date + timedelta(days=1),
            "booking_nights": 1,
            "campsite_id": permit_entrance_id,
            "campsite_site_name": permit_entrance_name,
            "campsite_loop_name": loop_name,
            "campsite_type": cls.facility_type,
            "campsite_use_type": use_type,
        }

    @classmethod
    def process_campsite_availability(
        cls,
        availability: Dict[str, Any],
        recreation_area: str,
        recreation_area_id: int,
        facility_name: str,
        facility_id: int,
        month: datetime,
        campsite_metadata: pd.DataFrame,
    ) -> List[Optional[AvailableCampsite]]:
        """
        Parse the JSON Response and return availabilities

        Parameters
        ----------
        availability: dict
            API Response
        recreation_area: str
            Name of Recreation Area
        recreation_area_id: int
            ID of Recreation Area
        facility_name: str
            Campground Facility Name
        facility_id: int
            Campground Facility ID
        month: datetime
            Month to Process
        campsite_metadata: pd.DataFrame
            Metadata Fetched from the Recreation.gov API about the Campsites

        Returns
        -------
        total_campsite_availability: List[Optional[AvailableCampsite]]
            Any monthly availabilities
        """
        # Special case for Mt. Whitney
        if facility_id == 233260:
            facility_id = 445860

        total_campsite_availability: List[Optional[AvailableCampsite]] = []
        permit_data = PermitMonthlyAvailabilityResponse(**availability)
        for (
            matching_date,
            date_related_data,
        ) in permit_data.payload.items():
            for (
                permit_entrance_id,
                availability_status,
            ) in date_related_data.items():
                if availability_status.remaining > 0:
                    fields = cls.make_campsite_availability_fields(
                        permit_entrance_id,
                        facility_id,
                        matching_date,
                        campsite_metadata,
                    )
                    available_campsite = AvailableCampsite(
                        campsite_occupancy=(1, availability_status.remaining),
                        availability_status=f"{availability_status.remaining}/{availability_status.total}",
                        recreation_area=recreation_area,
                        recreation_area_id=recreation_area_id,
                        facility_name=facility_name,
                        facility_id=facility_id,
                        permitted_equipment=[],
                        campsite_attributes=[],
                        **fields,
                    )
                    total_campsite_availability.append(available_campsite)
        return total_campsite_availability

    def get_campground_ids_by_campsites(
        self, campsite_ids: List[int]
    ) -> Tuple[List[int], List[CamplyModel]]:
        """
        Retrieve a list of FacilityIDs, and Facilities from a Campsite ID List

        Parameters
        ----------
        campsite_ids: List[int]
            List of Campsite IDs

        Returns
        -------
        Tuple[List[int], List[CamplyModel]]
        """
        permits = []
        unknown_ids = []
        for campsite_id in campsite_ids:
            try:
                campsite = self.get_campsite_by_id(campsite_id=campsite_id)
                permits.append(campsite)
            except ProviderSearchError as e:
                logging.warning(f"Ignoring ProviderSearchError for #{campsite_id}.")
                unknown_ids.append(campsite_id)
                continue
        
        if unknown_ids:
            for unknown_permit_id in unknown_ids:
                campsite = None
                for facility_id, map in self.facility_permit_map.items():
                    if unknown_permit_id in map:
                        name = map[unknown_permit_id]
                        campsite = PermitEntranceResponse(
                            PermitEntranceID=unknown_permit_id,
                            FacilityID=facility_id,
                            PermitEntranceName=name,
                            PermitEntranceDescription='',
                            District='',
                            Town='',
                            PermitEntranceAccessible=True,
                            Longitude=0.0,
                            Latitude=0.0,
                            CreatedDate=date.today(),
                            LastUpdatedDate=date.today(),
                            ATTRIBUTES=[],
                            ZONES=[],
                        )
                        break
                if campsite:
                    permits.append(campsite)
                else:
                    raise ProviderSearchError(
                        "No facility can be determined from specified permits."
                    )

        facility_ids = [i.FacilityID for i in permits]
        facility_ids_unique = list(set(facility_ids))
        return facility_ids_unique, list(permits)
