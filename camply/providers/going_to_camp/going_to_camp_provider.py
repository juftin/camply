"""
Going to Camp Web Searching Utilities
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

import requests
from fake_useragent import UserAgent
from pydantic import ValidationError

from camply.containers import AvailableResource, CampgroundFacility, RecreationArea
from camply.containers.base_container import GoingToCampEquipment
from camply.containers.gtc_api_responses import ResourceLocation
from camply.providers.base_provider import BaseProvider, ProviderSearchError
from camply.utils import make_list
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)

# Map going to camp subdomains to RecreationAreas
RECREATION_AREAS = {
    "longpoint.goingtocamp.com": RecreationArea(
        recreation_area="Long Point Region",
        recreation_area_id=1,
        recreation_area_location="Ontario, CA",
    ),
    "stclair.goingtocamp.com": RecreationArea(
        recreation_area="St. Clair Region",
        recreation_area_id=2,
        recreation_area_location="Ontario, CA",
    ),
    "washington.goingtocamp.com": RecreationArea(
        recreation_area="Washington State Parks",
        recreation_area_id=3,
        recreation_area_location="Washington, USA",
    ),
    "yukon.goingtocamp.com": RecreationArea(
        recreation_area="Yukon (Backcountry)",
        recreation_area_id=4,
        recreation_area_location="Yukon, CA",
    ),
    "hamilton.goingtocamp.com": RecreationArea(
        recreation_area="Hamilton",
        recreation_area_id=5,
        recreation_area_location="Ontario, CA",
    ),
    "maitlandvalley.goingtocamp.com": RecreationArea(
        recreation_area="Maitland Valley",
        recreation_area_id=6,
        recreation_area_location="Ontario, CA",
    ),
    "orovillepark.goingtocamp.com": RecreationArea(
        recreation_area="Oroville Park",
        recreation_area_id=7,
        recreation_area_location="Washington, USA",
    ),
    "saugeen.goingtocamp.com": RecreationArea(
        recreation_area="Saugeen Valley",
        recreation_area_id=8,
        recreation_area_location="Ontario, CA",
    ),
    "tacomapower.goingtocamp.com": RecreationArea(
        recreation_area="Tacoma Power Parks",
        recreation_area_id=9,
        recreation_area_location="Washington, USA",
    ),
    "wisconsin.goingtocamp.com": RecreationArea(
        recreation_area="Wisconsin State Parks",
        recreation_area_id=10,
        recreation_area_location="Wisconsin, USA",
    ),
    "ahtrails.ca": RecreationArea(
        recreation_area="Algonquin Highlands",
        recreation_area_id=11,
        recreation_area_location="Ontario, CA",
    ),
    "parkreservations.maryland.gov": RecreationArea(
        recreation_area="Maryland State Parks",
        recreation_area_id=12,
        recreation_area_location="Maryland, USA",
    ),
    "reservations.ncc-ccn.gc.ca": RecreationArea(
        recreation_area="Gatineau Park",
        recreation_area_id=13,
        recreation_area_location="Ottawa-Gatineau, Ontario-Quebec, CA",
    ),
    "www.nlcamping.ca": RecreationArea(
        recreation_area="Newfoundland & Labrador Provincial Parks",
        recreation_area_id=14,
        recreation_area_location="Newfoundland and Labrador, CA",
    ),
    "camping.bcparks.ca": RecreationArea(
        recreation_area="BC Parks",
        recreation_area_id=15,
        recreation_area_location="British Columbia, CA",
    ),
}

NON_GROUP_EQUIPMENT = -32768

CAMP_SITE = -2147483648
OVERFLOW_SITE = -2147483647
GROUP_SITE = -2147483643

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

    @classmethod
    def find_recreation_areas(
        cls, search_string: Optional[str] = None, **kwargs
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
        if search_string is not None:
            logger.info(f'Searching for Recreation Areas matching: "{search_string}"')

        if not search_string or search_string == "":
            rec_areas = RECREATION_AREAS.values()
            log_sorted_response(rec_areas)
            return rec_areas

        rec_areas = []
        for _, rec_area in RECREATION_AREAS.items():
            if (
                search_string.lower() in rec_area.recreation_area.lower()
                or search_string.lower() in rec_area.recreation_area_location.lower()
            ):
                rec_areas.append(rec_area)

        log_sorted_response(rec_areas)

        return rec_areas

    def rec_area_lookup(self, rec_area_id: int) -> Tuple[str, RecreationArea]:
        """
        Lookup a recreation area by ID

        Parameters
        ----------
        rec_area_id: int
            The recreation area ID to lookup

        Returns
        -------
        domain_name, rec_ara: Tuple[str, RecreationArea]
            The rec area's domain name and the recreation area object
        """
        for domain_name, rec_area in RECREATION_AREAS.items():
            if str(rec_area.recreation_area_id) == str(rec_area_id):
                return domain_name, rec_area

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

        Returns
        -------
        facilities: List[CampgroundFacility]
            Array of Matching Campgrounds
        """
        if rec_area_id in (None, [], ()):
            logger.error(
                "This provider requires --rec-area to be specified when seaching for campsites"
            )
            sys.exit(1)

        return self.find_facilities_per_recreation_area(
            rec_area_id=rec_area_id,
            campground_id=campground_id,
            searching_string=search_string,
        )

    def _get_attr_val(self, attribute, attribute_detail) -> any:
        for attr_value in attribute.get("values", []):
            for attribute_enum_detail in attribute_detail.get("values"):
                if attribute_enum_detail["enumValue"] == attr_value:
                    return _fetch_nested_key(
                        attribute_enum_detail, "localizedValues", 0, "displayName"
                    )

    def get_site_details(self, rec_area_id: int, resource_id: int):
        """
        Get the details about a site in a recreation area

        Parameters
        ----------
        rec_area_id: int
            Recreation Area ID by which to filter
        resource_id: int

        Returns
        -------
        details: Dict[str, str]
            The details about the site
        """
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
            attribute_name = _fetch_nested_key(
                attribute_detail, "localizedValues", 0, "displayName"
            )
            attribute_value = attribute.get("value")
            attribute_values = []
            # Attribute a multi-value enum
            if not attribute_value:
                attr_value = self._get_attr_val(attribute, attribute_detail)
                if not attr_value:
                    continue
                attribute_values.append(attr_value)
            else:
                attribute_values.append(f"{attribute_value}")

            site_attributes[attribute_name] = ",".join(attribute_values)
        site_details["site_attributes"] = site_attributes

        return site_details

    def get_reservation_link(
        self,
        rec_area_domain_name,
        resource_location_id,
        map_id,
        equipment_id,
        sub_equipment_id,
        party_size,
        start_date,
        end_date,
    ):
        """
        Generate a URL which a site can be booked

        Returns
        -------
        url: str
            The reservation link URL

        """
        if not sub_equipment_id:
            sub_equipment_id = ""

        return (
            "https://%s/create-booking/results?mapId=%s"
            "&bookingCategoryId=0"
            "&startDate=%s"
            "&endDate=%s"
            "&isReserving=true"
            "&equipmentId=%s"
            "&subEquipmentId=%s"
            "&partySize=%s"
            "&resourceLocationId=%s"
            % (
                rec_area_domain_name,
                map_id,
                start_date.isoformat(),
                end_date.isoformat(),
                equipment_id,
                sub_equipment_id,
                party_size,
                resource_location_id,
            )
        )

    def find_facilities_per_recreation_area(
        self,
        rec_area_id: Union[List[int], int] = None,
        campground_id: int = None,
        search_string: str = None,
        **kwargs,
    ) -> List[CampgroundFacility]:
        """
        Find Matching Campsites by Recreation Area

        Parameters
        ----------
        rec_area_id: int
            Recreation Area ID

        campground_id: Optional[List[int]]
            Campground IDs

        search_string: Optional[str]
            A string to search for in the facility name

        Returns
        -------
        campgrounds: List[CampgroundFacility]
            Array of Matching Campsites
        """
        rec_area_id = make_list(rec_area_id, coerce=int)[0]
        logger.info(
            f"Retrieving Facility Information for Recreation Area ID: `{rec_area_id}`."
        )

        rec_area = None
        for _, ra in RECREATION_AREAS.items():
            if str(ra.recreation_area_id) == str(rec_area_id):
                rec_area = ra
        if not rec_area:
            logger.error(f"Recreation area '{rec_area_id}' does not exist.")
            sys.exit(1)

        self.campground_details = {}
        api_response = self._api_request(rec_area_id, "LIST_CAMPGROUNDS")

        filtered_facilities = self._filter_facilities_responses(
            rec_area_id, facilities=api_response
        )

        campgrounds = []
        # Fetch campgrounds details for all facilities
        for camp_details in self._api_request(rec_area_id, "CAMP_DETAILS"):
            self.campground_details[camp_details["resourceLocationId"]] = camp_details

        # If a search string is provided, make sure every facility name contains
        # the search string
        if search_string and search_string not in [[], (), ""]:
            filtered_facilities = [
                f
                for f in filtered_facilities
                if search_string.lower() in f.resource_location_name.lower()
            ]

        for facility in filtered_facilities:
            _, campground_facility = self._process_facilities_responses(
                rec_area, facility=facility
            )
            if not campground_facility:
                continue
            if not campground_id:
                campgrounds.append(campground_facility)
            if campground_id and str(campground_facility.facility_id) in campground_id:
                campgrounds.append(campground_facility)

        logger.info(f"{len(campgrounds)} Matching Campgrounds Found")
        log_sorted_response(response_array=campgrounds)
        return campgrounds

    def _hostname_for(self, recreation_area_id: int) -> str:
        for hostname, recreation_area in RECREATION_AREAS.items():
            if str(recreation_area.recreation_area_id) == str(recreation_area_id):
                return hostname
        return None

    def _api_request(
        self,
        rec_area_id: int,
        endpoint_name: str,
        params: Optional[Dict[str, str]] = None,
    ) -> str:
        if params is None:
            params = {}

        hostname = self._hostname_for(rec_area_id)
        endpoint = ENDPOINTS.get(endpoint_name)
        url = None
        if endpoint:
            url = endpoint.format(hostname)
        user_agent = {
            "User-Agent": UserAgent(use_external_data=False, browsers=["chrome"]).chrome
        }
        response = requests.get(url=url, headers=user_agent, params=params, timeout=30)
        if response.ok is False:
            error_message = "Receiving bad data from GoingToCamp API: status_code: "
            f"{response.status_code}: {response.text}"
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
        filtered_facilities = []
        for facil in facilities:
            try:
                location_name = _fetch_nested_key(
                    facil, "resourceLocationLocalizedValues", "en-US"
                )
                if not location_name:
                    location_name = _fetch_nested_key(
                        facil, "resourceLocationLocalizedValues", "en-CA"
                    )

                park_alerts = _fetch_nested_key(
                    facil, "park_alerts", "en-US", 0, "messageTitle"
                )
                if not park_alerts:
                    _fetch_nested_key(facil, "park_alerts", "en-CA", 0, "messageTitle")

                facility = ResourceLocation(
                    id=facil.get("mapId"),
                    park_alerts=park_alerts,
                    rec_area_id=rec_area_id,
                    resource_categories=facil.get("resourceCategoryIds"),
                    resource_location_id=facil.get("resourceLocationId"),
                    resource_location_name=location_name,
                )
            except ValidationError as ve:
                logger.error("That doesn't look like a valid Campground Facility")
                logger.error(facil)
                raise ProviderSearchError(
                    "Invalid Campground Facility Returned"
                ) from ve

            if not facility.resource_categories:
                continue

            # Resource categories from: /api/resourcecategory
            if any(
                [
                    CAMP_SITE in facility.resource_categories,
                    GROUP_SITE in facility.resource_categories,
                    OVERFLOW_SITE in facility.resource_categories,
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
        details = self.campground_details[facility.resource_location_id]
        region = _fetch_nested_key(details, "region")
        facility_name = _fetch_nested_key(details, "localizedValues", 0, "fullName")
        if region:
            formatted_recreation_area = f"{rec_area.recreation_area}, {region}"
        else:
            formatted_recreation_area = f"{rec_area.recreation_area}"

        campground_facility = CampgroundFacility(
            facility_name=facility_name,
            recreation_area=formatted_recreation_area,
            facility_id=facility.resource_location_id,
            recreation_area_id=facility.rec_area_id,
            map_id=facility.id,
        )
        return facility, campground_facility

    def _find_matching_resources(self, rec_area_id: int, search_filter: Dict[str, any]):
        results = self._api_request(rec_area_id, "MAPDATA", search_filter)

        availability_details = {
            search_filter["mapId"]: results["resourceAvailabilities"]
        }

        return availability_details, list(results["mapLinkAvailabilities"].keys())

    def list_equipment_types(self, rec_area_id: int) -> Dict[str, int]:
        """
        List equipment types available for a recreation area

        Params
        ------
        rec_area_id: int
            The ID of the recreation area

        Returns
        -------
        types: List[GoingToCampEquipment]
            A list of equipment types available to this rec area
        """
        results = self._api_request(rec_area_id, "LIST_EQUIPMENT")

        equipment_types = []
        # Only allow equipment from non-group equipment category (the 0th
        # element in results)
        for sub_category in results[0]["subEquipmentCategories"]:
            equipment_name = _fetch_nested_key(
                sub_category, "localizedValues", 0, "name"
            )
            equipment_id = sub_category["subEquipmentCategoryId"]
            equipment_types.append(
                GoingToCampEquipment(
                    equipment_name=equipment_name, equipment_type_id=equipment_id
                )
            )

        log_sorted_response(response_array=equipment_types)
        return equipment_types

    def list_site_availability(
        self,
        campground: CampgroundFacility,
        start_date: datetime.date,
        end_date: datetime.date,
        equipment_type_id: Optional[str],
    ) -> List[AvailableResource]:
        """
        Retrieve the Availability for all Sites in a Camp Area

        Sites are filtered on the provided date range and compatible
        equipment.

        Returns
        -------
        available_sites: List[AvailableResource]
            The list of available sites
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
            "equipmentCategoryId": NON_GROUP_EQUIPMENT,
            "filterData": [],
        }
        if equipment_type_id:
            search_filter["subEquipmentCategoryId"] = equipment_type_id

        resources, additional_resources = self._find_matching_resources(
            campground.recreation_area_id, search_filter
        )

        # Resources are often deeply nested; fetch nested resources
        for map_id in additional_resources:
            search_filter["mapId"] = map_id
            avail, _ = self._find_matching_resources(
                campground.recreation_area_id, search_filter
            )
            resources.update(avail)

        availabilities = []
        for map_id, resource_details in resources.items():
            for resource_id, availability_details in resource_details.items():
                if availability_details[0]["availability"] == 0:
                    ar = AvailableResource(resource_id=resource_id, map_id=map_id)
                    availabilities.append(ar)

        return availabilities


def _fetch_nested_key(obj: Union[dict, list, object], *keys: str) -> Any:
    """
    Fetch nested keys from dictionaries/lists if the keys exist

    Example
    -------
        mydict = {
            'foo': {
                'bar': 'baz'
            }
        }
        val = _fetch_nested_key(mydict, 'foo', 'bar')
        print(f"Value: {val}")
        Prints: Value: baz
    """
    if (
        not isinstance(obj, dict)
        and not isinstance(obj, list)
        and not isinstance(obj, object)
    ):
        raise AttributeError(
            "`obj` must be of type `dict`, `list`, or `object`, but is not"
        )
    if len(keys) == 0:
        raise AttributeError(
            "At least one key must be specified in `keys:`. None were provided"
        )

    _element = obj
    for key in keys:
        try:
            _element = _element[key]
            if not _element:
                _element = getattr(_element, key)
        except (KeyError, TypeError, AttributeError):
            return None

    return _element
