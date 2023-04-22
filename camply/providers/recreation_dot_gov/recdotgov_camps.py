"""
Campsite Searching: Recreation.gov
"""

import json
import logging
from datetime import datetime, timedelta
from itertools import chain
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
import requests

from camply.config import RecreationBookingConfig, RIDBConfig
from camply.containers import AvailableCampsite
from camply.containers.api_responses import (
    CampsiteAvailabilityResponse,
    CampsiteResponse,
    RecDotGovCampsite,
    RecDotGovCampsiteResponse,
)
from camply.providers.recreation_dot_gov.recdotgov_provider import RecreationDotGovBase
from camply.utils import api_utils

logger = logging.getLogger(__name__)


class RecreationDotGov(RecreationDotGovBase):
    """
    Recreation.gov: Campsite Searcher
    """

    facility_type = RIDBConfig.CAMPGROUND_FACILITY_FIELD_QUALIFIER
    resource_api_path = RIDBConfig.CAMPSITE_API_PATH
    activity_name = "CAMPING"
    api_response_class = CampsiteResponse
    api_base_path = RecreationBookingConfig.API_BASE_PATH
    api_search_result_class = RecDotGovCampsite
    api_search_result_key = "campsite_id"

    def paginate_recdotgov_campsites(
        self, facility_id: int, equipment: Optional[List[str]] = None
    ) -> List[RecDotGovCampsite]:
        """
        Paginate through the RecDotGov Campsite Metadata
        """
        results = 0
        continue_paginate = True
        endpoint_url = api_utils.generate_url(
            scheme=RecreationBookingConfig.API_SCHEME,
            netloc=RecreationBookingConfig.API_NET_LOC,
            path="api/search/campsites",
        )
        fq_list = [f"asset_id:{facility_id}"]
        if isinstance(equipment, list) and len(equipment) > 0:
            for item in equipment:
                fq_list.append(f"campsite_equipment_name:{item}")
        params = {
            "start": 0,
            "size": 1000,
            "fq": fq_list,
            "include_non_site_specific_campsites": True,
        }
        campsites: List[RecDotGovCampsite] = []
        while continue_paginate is True:
            response = self.make_recdotgov_request_retry(
                method="GET",
                url=endpoint_url,
                params=params,
            )
            returned_data = json.loads(response.content)
            campsite_response = RecDotGovCampsiteResponse(**returned_data)
            campsites += campsite_response.campsites
            results += campsite_response.size
            params.update(start=results)
            if results == campsite_response.total:
                continue_paginate = False
        return campsites

    def make_recdotgov_availability_request(
        self,
        campground_id: int,
        month: datetime,
    ) -> requests.Response:
        """
        Make a request to the RecreationDotGov API

        Parameters
        ----------
        campground_id
        month

        Returns
        -------
        requests.Response
        """
        api_endpoint = self._rec_availability_get_endpoint(
            path=f"{campground_id}/{RecreationBookingConfig.API_MONTH_PATH}"
        )
        formatted_month = month.strftime("%Y-%m-01T00:00:00.000Z")
        query_params = {"start_date": formatted_month}
        return self.make_recdotgov_request(
            method="GET",
            url=api_endpoint,
            params=query_params,
        )

    @classmethod
    def _items_to_unique_dicts(
        cls, item: Union[List[Dict[str, Any]], pd.Series]
    ) -> List[Dict[str, Any]]:
        """
        Ensure the proper items are parsed for equipment and attributes
        """
        if isinstance(item, pd.Series):
            list_of_dicts = list(chain.from_iterable(item.tolist()))
            unique_list_of_dicts = [
                dict(s) for s in {frozenset(d.items()) for d in list_of_dicts}
            ]
            return unique_list_of_dicts
        else:
            return item

    @classmethod
    def _get_equipment_and_attributes(
        cls,
        campsite_id: int,
        campsite_metadata: pd.DataFrame,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Index a DataFrame in a Complicated Way
        """
        try:
            equipment = campsite_metadata.at[campsite_id, "permitted_equipment"]
        except LookupError:
            equipment = None
        try:
            attributes = campsite_metadata.at[campsite_id, "attributes"]
        except LookupError:
            attributes = None
        equipment = cls._items_to_unique_dicts(item=equipment)
        attributes = cls._items_to_unique_dicts(item=attributes)
        return equipment, attributes

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
        availability: Dict[str, Any]
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
        total_campsite_availability: List[Optional[AvailableCampsite]] = []
        campsite_data = CampsiteAvailabilityResponse(**availability)
        for campsite_id, site_related_data in campsite_data.campsites.items():
            for (
                matching_date,
                availability_status,
            ) in site_related_data.availabilities.items():
                if (
                    availability_status
                    not in RecreationBookingConfig.CAMPSITE_UNAVAILABLE_STRINGS
                ):
                    booking_url = (
                        f"{RecreationBookingConfig.CAMPSITE_BOOKING_URL}/{campsite_id}"
                    )
                    equipment, attributes = cls._get_equipment_and_attributes(
                        campsite_id=campsite_id, campsite_metadata=campsite_metadata
                    )
                    available_campsite = AvailableCampsite(
                        campsite_id=campsite_id,
                        booking_date=matching_date,
                        booking_end_date=matching_date + timedelta(days=1),
                        booking_nights=1,
                        campsite_site_name=site_related_data.site,
                        campsite_loop_name=site_related_data.loop,
                        campsite_type=site_related_data.campsite_type,
                        campsite_occupancy=(
                            site_related_data.min_num_people,
                            site_related_data.max_num_people,
                        ),
                        campsite_use_type=site_related_data.type_of_use,
                        availability_status=availability_status,
                        recreation_area=recreation_area,
                        recreation_area_id=recreation_area_id,
                        facility_name=facility_name,
                        facility_id=facility_id,
                        booking_url=booking_url,
                        permitted_equipment=equipment,
                        campsite_attributes=attributes,
                    )
                    total_campsite_availability.append(available_campsite)
        return total_campsite_availability
