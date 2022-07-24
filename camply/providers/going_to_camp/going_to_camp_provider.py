"""
Going to Camp Web Searching Utilities
"""

import json
import logging
import re
from base64 import b64decode
from datetime import datetime, timedelta
from enum import Enum
from json import loads
from random import choice
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib import parse

import pandas as pd
import requests
import tenacity
from pydantic import ValidationError

from camply.config import STANDARD_HEADERS, USER_AGENTS
from camply.containers import AvailableCampsite, CampgroundFacility, RecreationArea
from camply.containers.gtc_api_responses import ResourceLocation
from camply.providers.base_provider import BaseProvider, ProviderSearchError
from camply.utils import api_utils, logging_utils
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)

# TODO add remaining areas supported by going to camp
# Map going to camp subdomains to RecreationAreas
RECREATION_AREAS = {
    "washington.goingtocamp.com": RecreationArea(
        recreation_area="Washington State Parks",
        recreation_area_id=1,
        recreation_area_location="Washington, USA",
    ),
    "wisconsin.goingtocamp.com": RecreationArea(
        recreation_area="Wisconsin State Parks",
        recreation_area_id=2,
        recreation_area_location="Wisconsin, USA",
    ),
}

ENDPOINTS = {
    "CAMP_DETAILS": "https://{}/api/resourcelocation",
    "DAILY_AVAILABILITY": "https://{}/api/availability/resourcedailyavailability",
    "LIST_CAMPGROUNDS": "https://{}/api/resourcelocation/rootmaps",
    "LIST_EQUIPMENT": "https://{}/api/equipment",
    "LIST_RESOURCE_CATEGORY": "https://{}/api/resourcecategory",
    "LIST_RESOURCE_STATUS": "https://{}/api/availability/resourcestatus",
    "MAPDATA": "https://{}/api/availability/map",
    "SITE_DETAILS": "https://{}/api/resource/details",
    "ATTRIBUTE_DETAILS": "https://{}/api/attribute/filterable",
}


class GoingToCampProvider(BaseProvider):
    """
    Going To Camp API provider
    """

    def __repr__(self):
        """
        String Representation

        Returns
        -------
        str
        """
        return "<GoingToCampProvider>"

    def find_recreation_areas(
        self, search_string: Optional[str] = None, **kwargs
    ) -> List[RecreationArea]:
        """
        Find Matching Recreation Areas based on search string

        Parameters
        ----------
        search_string: Optional[str]
            Search Keyword(s)

        Returns
        -------
        filtered_responses: List[RecreationArea]
            Array of Matching Recreation Areas
        """
        logger.info(f'Searching for Recreation Areas matching: "{search_string}"')

        if not search_string or search_string == "":
            rec_areas = RECREATION_AREAS.values()
            log_sorted_response(rec_areas)
            return rec_areas

        rec_areas = []
        for key, rec_area in RECREATION_AREAS.items():
            if (
                search_string in rec_area.recreation_area.lower()
                or search_string in rec_area.recreation_area_location.lower()
            ):
                rec_areas.append(rec_area)

        log_sorted_response(rec_areas)

        return rec_areas

    def rec_area_lookup(self, rec_area_id: int) -> RecreationArea:
        for _, rec_area in RECREATION_AREAS.items():
            if str(rec_area.recreation_area_id) == str(rec_area_id):
                return rec_area

    def find_campgrounds(
        self,
        search_string: str = None,
        rec_area_id: Optional[List[int]] = None,
        campground_id: Optional[List[int]] = None,
        campsite_id: Optional[List[int]] = None,
        **kwargs,
    ) -> List[CampgroundFacility]:
        """
        Find Campgrounds Given a Set of Search Criteria

        Parameters
        ----------
        search_string: str
            Search Keyword(s)
        rec_area_id: Optional[List[int]]
            Recreation Area ID by which to filter
        campground_id: Optional[List[int]]
            ID of the Campground
        campsite_id: Optional[List[int]]
            ID of the Campsite

        Returns
        -------
        facilities: List[CampgroundFacility]
            Array of Matching Campgrounds
        """
        if rec_area_id not in (None, [], ()):
            facilities = list()
            for recreation_area in rec_area_id:
                facilities += self.find_facilities_per_recreation_area(
                    rec_area_id=recreation_area
                )
        # TODO Finish other search methods

        return facilities

    def get_site_details(self, rec_area_id: int, resource_id: int):
        if not hasattr(self, "_attribute_details"):
            self._attribute_details = self._api_request(
                rec_area_id, "ATTRIBUTE_DETAILS"
            )
        attribute_details = self._attribute_details

        site_details = self._api_request(
            rec_area_id, "SITE_DETAILS", {"resourceId": resource_id}
        )
        site_attributes = {}

        for attribute in site_details["definedAttributes"]:
            attribute_detail = attribute_details[
                f"{attribute['attributeDefinitionId']}"
            ]
            attribute_name = fetch_nested_key(
                attribute_detail, "localizedValues", 0, "displayName"
            )
            attribute_value = attribute.get("value")
            attribute_values = []

            # Attribute a multi-value enum
            if not attribute_value:
                for attr_value in attribute.get("values"):
                    for attribute_enum_detail in attribute_detail.get("values"):
                        if attribute_enum_detail["enumValue"] == attr_value:
                            attribute_values.append(
                                fetch_nested_key(
                                    attribute_enum_detail,
                                    "localizedValues",
                                    0,
                                    "displayName",
                                )
                            )
            else:
                attribute_values.append(f"{attribute_value}")

            site_attributes[attribute_name] = ",".join(attribute_values)
        site_details["site_attributes"] = site_attributes

        return site_details

    def get_reservation_link(
        self,
        party_size,
        start_date,
        end_date,
        camp_area,
        resource_location_id,
        equipment_id,
        sub_equipment_id,
    ):
        """
        Web link at which a reservation could be made for the specified search
        :param party_size:
        :param start_date:
        :param end_date:
        :param camp_area:
        :param resource_location_id:
        :param equipment_id:
        :param sub_equipment_id:
        :return:
        """
        return (
            "https://washington.goingtocamp.com/create-booking/results?mapId=%s&bookingCategoryId=0&startDate=%s&endDate=%s&isReserving=true&equipmentId=%s&subEquipmentId=%s&partySize=%s&resourceLocationId=%s"
            % (
                camp_area.map_id,
                start_date.isoformat(),
                end_date.isoformat(),
                equipment_id,
                sub_equipment_id,
                party_size,
                resource_location_id,
            )
        )

    def find_facilities_per_recreation_area(
        self, rec_area_id: int = None, **kwargs
    ) -> List[CampgroundFacility]:
        """
        Find Matching Campsites by Recreation Area

        Parameters
        ----------
        rec_area_id: int
            Recreation Area ID

        Returns
        -------
        campgrounds: List[CampgroundFacility]
            Array of Matching Campsites
        """
        logger.info(
            f"Retrieving Facility Information for Recreation Area ID: `{rec_area_id}`."
        )

        rec_area = None
        for key, ra in RECREATION_AREAS.items():
            if str(ra.recreation_area_id) == str(rec_area_id):
                rec_area = ra
        if not rec_area:
            logger.error(f"Recreation area '{rec_area_id}' does not exist.")
            exit(1)

        self.campground_details = {}
        api_response = self._api_request(rec_area_id, "LIST_CAMPGROUNDS")

        filtered_facilities = self._filter_facilities_responses(
            rec_area_id, facilities=api_response
        )
        campgrounds = list()
        logger.info(f"{len(filtered_facilities)} Matching Campgrounds Found")

        # Fetch campgrounds details for all facilities
        for camp_details in self._api_request(rec_area_id, "CAMP_DETAILS"):
            self.campground_details[camp_details["resourceLocationId"]] = camp_details

        for facility in filtered_facilities:
            _, campground_facility = self._process_facilities_responses(
                rec_area, facility=facility
            )
            if campground_facility is not None:
                campgrounds.append(campground_facility)
        log_sorted_response(response_array=campgrounds)
        return campgrounds

    def _hostname_for(self, recreation_area_id: int) -> str:
        for hostname, recreation_area in RECREATION_AREAS.items():
            if str(recreation_area.recreation_area_id) == str(recreation_area_id):
                return hostname
        return None

    def _api_request(
        self, rec_area_id: int, endpoint_name: str, params: dict[str, str] = {}
    ) -> str:
        hostname = self._hostname_for(rec_area_id)
        endpoint = ENDPOINTS.get(endpoint_name)
        url = None
        if endpoint:
            url = endpoint.format(hostname)

        headers = {}
        response = requests.get(url=url, headers=headers, params=params, timeout=30)
        try:
            assert response.status_code == 200
        except AssertionError:
            error_message = f"Receiving bad data from GoingToCamp API: status_code: {response.status_code}: {response.text}"
            logger.error(error_message)
            raise ConnectionError(error_message)

        return json.loads(response.content)

    def _filter_facilities_responses(
        self, rec_area_id: int, facilities=List[dict]
    ) -> List[ResourceLocation]:
        """
        Filter Facilities to Actual Reservable Campsites

        Parameters
        ----------
        responses

        Returns
        -------
        List[dict]
        """
        filtered_facilities = list()
        for facil in facilities:
            try:
                facility = ResourceLocation(
                    ID=facil.get("mapId"),
                    ParkAlerts=facil.get("parkAlerts"),
                    RecAreaID=rec_area_id,
                    ResourceCategories=facil.get("resourceCategoryIds"),
                    ResourceLocationID=facil.get("resourceLocationId"),
                    ResourceLocationName=fetch_nested_key(
                        facil, "resourceLocationLocalizedValues", "en-US"
                    ),
                )
            except ValidationError as e:
                logger.error("That doesn't look like a valid Campground Facility")
                logger.error(facil)
                logger.exception(e)
                raise ProviderSearchError("Invalid Campground Facility Returned")

            if not facility.ResourceCategories:
                continue

            # Resource categories from: /api/resourcecategory
            # TODO: Don't hardcode
            if any(
                [
                    -2147483648 in facility.ResourceCategories,  # Campsite
                    -2147483643 in facility.ResourceCategories,  # Group camp
                ]
            ):
                filtered_facilities.append(facility)

        return filtered_facilities

    def _process_facilities_responses(
        self, rec_area: RecreationArea, facility: ResourceLocation
    ) -> Tuple[dict, Optional[CampgroundFacility]]:
        """
        Process Facilities Responses to be More Usable

        Parameters
        ----------
        facility: dict

        Returns
        -------
        Tuple[dict, CampgroundFacility]
        """
        details = self.campground_details[facility.ResourceLocationID]
        facility_name = fetch_nested_key(details, "localizedValues", 0, "fullName")
        facility_state = fetch_nested_key(details, "region")
        recreation_area_id = facility.RecAreaID
        formatted_recreation_area = f"{rec_area.recreation_area}, {facility_state}"
        campground_facility = CampgroundFacility(
            facility_name=facility_name,
            recreation_area=formatted_recreation_area,
            facility_id=facility.ResourceLocationID,
            recreation_area_id=facility.RecAreaID,
            map_id=facility.ID,
        )
        return facility, campground_facility

    def _find_matching_resources(self, rec_area_id: int, search_filter: dict[str, any]):
        results = self._api_request(rec_area_id, "MAPDATA", search_filter)
        availabilities = results["resourceAvailabilities"]

        for mapId in results["mapLinkAvailabilities"].keys():
            search_filter["mapId"] = mapId
            availabilities.update(
                self._find_matching_resources(rec_area_id, search_filter)
            )

        return availabilities

    def list_equipment_categories(self, rec_area_id: int) -> dict[str, int]:
        """
        List equipment categories available for a recreation area

        returns
        -------
        categories: dict[str, int]
            A dictionary with keys corresponding to category names and values corresponding with the rec area's category
            IDs
        """
        results = self._api_request(rec_area_id, "LIST_EQUIPMENT")

        sub_categories = {}
        # TODO: Only focusing on the "primary" equipment category for now.
        # The other category is, the "group" camp category, which is the 1th element in `results`
        for sub_category in results[0]["subEquipmentCategories"]:
            category_name = fetch_nested_key(
                sub_category, "localizedValues", 0, "name"
            ).lower()
            max_size = 0
            if "tent" in category_name:
                # e.g. 1 Tent
                max_size = int(category_name.split(" ")[0])
            if "rv/trailer up to" in category_name:
                # e.g. RV/Trailers up to 20'
                max_size = int(re.findall(r"\d+", category_name)[0])
            if "rv/trailer over" in category_name:
                # e.g. RV/Trailers over 40'
                max_size = 1000

            category_id = sub_category["subEquipmentCategoryId"]
            sub_categories[category_name] = {"id": category_id, "max_size": max_size}

        return sub_categories

    def list_site_availability(
        self,
        campground: CampgroundFacility,
        start_date: datetime.date,
        end_date: datetime.date,
        equipment_category: any,
    ):
        """
        Retrieve the Availability for all Sites in a Camp Area which can host the selected Equipment within a date range
        :return:
        """
        search_filter = {
            "mapId": campground.map_id,
            "resourceLocationId": campground.facility_id,
            "bookingCategoryId": 0,
            "startDate": start_date.isoformat(),
            "endDate": end_date.isoformat(),
            "isReserving": True,
            "getDailyAvailability": False,
            "partySize": 1,
            "equipmentCategoryId": -32768,  # TODO: Confirm what this means. Possibly all camping equipment
            "subEquipmentCategoryId": equipment_category,
            "filterData": [],
        }

        resources = self._find_matching_resources(
            campground.recreation_area_id, search_filter
        )
        availabilities = []
        for resource_id, availability_details in resources.items():
            if availability_details[0]["availability"] == 0:
                availabilities.append(resource_id)

        return availabilities


def fetch_nested_key(obj: dict | list, *keys: str) -> Any:
    """
    Fetch nested keys from dictionaries/lists if the keys exist
    Example:
        mydict = {
            'foo': {
                'bar': 'baz'
            }
        }
        val = fetch_nested_key(mydict, 'foo', 'bar')
        print(f"Value: {val}")
        Prints: Value: baz
    """
    if not isinstance(obj, dict) and not isinstance(obj, list):
        raise AttributeError("`obj` must be of type `dict`, but is not")
    if len(keys) == 0:
        raise AttributeError(
            "At least one key must be specified in `keys:`. None were provided"
        )

    _element = obj
    for key in keys:
        try:
            _element = _element[key]
        except (KeyError, TypeError):
            return None

    return _element
