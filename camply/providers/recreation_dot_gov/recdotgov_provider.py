"""
Recreation.gov Web Searching Utilities
"""

import json
import logging
from base64 import b64decode
from datetime import datetime, timedelta
from itertools import chain
from json import loads
from random import choice
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib import parse

import pandas as pd
import requests
import tenacity
from pydantic import ValidationError

from camply.config import (
    STANDARD_HEADERS,
    USER_AGENTS,
    RecreationBookingConfig,
    RIDBConfig,
)
from camply.containers import AvailableCampsite, CampgroundFacility, RecreationArea
from camply.containers.api_responses import (
    CampsiteAvailabilityResponse,
    CampsiteResponse,
    FacilityResponse,
    GenericResponse,
    RecDotGovCampsite,
    RecDotGovCampsiteResponse,
    RecreationAreaResponse,
)
from camply.providers.base_provider import BaseProvider, ProviderSearchError
from camply.utils import api_utils, logging_utils
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)


class RecreationDotGov(BaseProvider):
    """
    Python Class for Working with Recreation.gov API / NPS APIs
    """

    def __init__(self, api_key: str = None):
        """
        Initialize with Search Dates
        """
        if api_key is None:
            _api_key = RIDBConfig.API_KEY
            if isinstance(_api_key, bytes):
                _api_key: str = b64decode(RIDBConfig.API_KEY).decode("utf-8")
        else:
            _api_key: str = api_key
        self._ridb_api_headers: dict = dict(accept="application/json", apikey=_api_key)

    def __repr__(self):
        """
        String Representation

        Returns
        -------
        str
        """
        return "<RecreationDotGov>"

    def find_recreation_areas(self, search_string: str = None, **kwargs) -> List[dict]:
        """
        Find Matching Campsites Based on Search String

        Parameters
        ----------
        search_string: str
            Search Keyword(s)

        Returns
        -------
        filtered_responses: List[dict]
            Array of Matching Campsites
        """
        try:
            assert any(
                [
                    kwargs.get("state", None) is not None,
                    search_string is not None and search_string != "",
                ]
            )
        except AssertionError:
            raise RuntimeError(
                "You must provide a search query or state(s) "
                "to find Recreation Areas"
            )
        logger.info(f'Searching for Recreation Areas: "{search_string}"')
        state_arg = kwargs.get("state", None)
        if state_arg is not None:
            kwargs.update({"state": state_arg.upper()})
        params = dict(query=search_string, sort="Name", full="true", **kwargs)
        if search_string is None:
            params.pop("query")
        api_response = self._ridb_get_paginate(
            path=RIDBConfig.REC_AREA_API_PATH, params=params
        )
        logger.info(f"{len(api_response)} recreation areas found.")
        logging_messages = list()
        for recreation_area_object in api_response:
            _, recreation_area = self._process_rec_area_response(
                recreation_area=recreation_area_object
            )
            if recreation_area is not None:
                logging_messages.append(recreation_area)
        log_sorted_response(response_array=logging_messages)
        return api_response

    def find_campgrounds(
        self,
        search_string: str = None,
        rec_area_id: Optional[List[int]] = None,
        campground_id: Optional[List[int]] = None,
        campsite_id: Optional[List[int]] = None,
        **kwargs,
    ) -> List[CampgroundFacility]:
        """
        Find Bookable Campgrounds Given a Set of Search Criteria

        Parameters
        ----------
        search_string: str
            Search Keyword(s)
        rec_area_id: Optional[List[int]]
            Recreation Area ID to filter with
        campground_id: Optional[List[int]]
            ID of the Campground
        campsite_id: Optional[List[int]]
            ID of the Campsite

        Returns
        -------
        facilities: List[CampgroundFacility]
            Array of Matching Campsites
        """
        if campsite_id not in (None, [], ()):
            facilities = self._process_specific_campsites_provided(
                campsite_id=campsite_id
            )
        elif campground_id not in (None, [], ()):
            facilities = self._find_facilities_from_campgrounds(
                campground_id=campground_id
            )
        elif rec_area_id not in (None, [], ()):
            facilities = list()
            for recreation_area in rec_area_id:
                facilities += self.find_facilities_per_recreation_area(
                    rec_area_id=recreation_area
                )
        else:
            state_arg = kwargs.get("state", None)
            if state_arg is not None:
                kwargs.update({"state": state_arg.upper()})
            if search_string in ["", None] and state_arg is None:
                raise RuntimeError(
                    "You must provide a search query or state to find campsites"
                )
            facilities = self._find_facilities_from_search(
                search=search_string, **kwargs
            )
        return facilities

    def find_facilities_per_recreation_area(
        self, rec_area_id: int = None, **kwargs
    ) -> List[CampgroundFacility]:
        """
        Find Matching Campsites Based from Recreation Area

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
        api_path = f"{RIDBConfig.REC_AREA_API_PATH}/{rec_area_id}/{RIDBConfig.FACILITIES_API_PATH}"
        api_response = self._ridb_get_paginate(
            path=api_path, params=dict(full="true", **kwargs)
        )
        filtered_facilities = self._filter_facilities_responses(responses=api_response)
        campgrounds = list()
        logger.info(f"{len(filtered_facilities)} Matching Campgrounds Found")
        for facility in filtered_facilities:
            _, campground_facility = self.process_facilities_responses(
                facility=facility
            )
            if campground_facility is not None:
                campgrounds.append(campground_facility)
        log_sorted_response(response_array=campgrounds)
        return campgrounds

    def _find_facilities_from_campgrounds(
        self, campground_id: Union[int, List[int]]
    ) -> List[CampgroundFacility]:
        """
        Find Matching Campsites from Campground ID

        Parameters
        ----------
        campground_id: Union[int, List[int]]
            ID of the Campsite
        Returns
        -------
        filtered_responses: List[CampgroundFacility]
            Array of Matching Campsites
        """
        campgrounds = list()
        for campground_identifier in campground_id:
            facility_data = self.get_ridb_data(
                path=f"{RIDBConfig.FACILITIES_API_PATH}/{campground_identifier}",
                params=dict(full=True),
            )
            filtered_facility = self._filter_facilities_responses(
                responses=[facility_data]
            )
            _, campground_facility = self.process_facilities_responses(
                facility=filtered_facility[0]
            )
            if campground_facility is not None:
                campgrounds.append(campground_facility)
        logger.info(f"{len(campgrounds)} Matching Campgrounds Found")
        log_sorted_response(response_array=campgrounds)
        return campgrounds

    def _find_facilities_from_search(self, search: str, **kwargs) -> List[dict]:
        """
        Find Matching Campgrounds Based on Search String

        Parameters
        ----------
        search: str
            Search String

        Returns
        -------
        campgrounds: List[dict]
            Array of Matching Campsites
        """
        facilities_response = self._ridb_get_paginate(
            path=RIDBConfig.FACILITIES_API_PATH,
            params=dict(query=search, activity="CAMPING", full="true", **kwargs),
        )
        filtered_responses = self._filter_facilities_responses(
            responses=facilities_response
        )
        logger.info(f"{len(filtered_responses)} Matching Campgrounds Found")
        campgrounds = list()
        for facility in filtered_responses:
            _, campground_facility = self.process_facilities_responses(
                facility=facility
            )
            if campground_facility is not None:
                campgrounds.append(campground_facility)
        log_sorted_response(response_array=campgrounds)
        return campgrounds

    @classmethod
    def _ridb_get_endpoint(cls, path: str) -> str:
        """
        Return an API Endpoint for the RIDP

        Parameters
        ----------
        path: str
            URL Endpoint, see https://ridb.recreation.gov/docs

        Returns
        -------
        endpoint_url: str
            URL for the API Endpoint
        """
        assert RIDBConfig.RIDB_BASE_PATH.endswith("/")
        base_url = api_utils.generate_url(
            scheme=RIDBConfig.RIDB_SCHEME,
            netloc=RIDBConfig.RIDB_NET_LOC,
            path=RIDBConfig.RIDB_BASE_PATH,
        )
        endpoint_url = parse.urljoin(base_url, path)
        return endpoint_url

    @tenacity.retry(
        wait=tenacity.wait_random_exponential(multiplier=2, max=10),
        stop=tenacity.stop.stop_after_delay(15),
    )
    def get_ridb_data(
        self, path: str, params: Optional[dict] = None
    ) -> Union[dict, list]:
        """
        Find Matching Campsites Based on Search String

        Parameters
        ----------
        path: str
            URL Endpoint, see https://ridb.recreation.gov/docs
        params: Optional[dict]
            API Call Parameters

        Returns
        -------
        Union[dict, list]
        """
        api_endpoint = self._ridb_get_endpoint(path=path)
        headers = self._ridb_api_headers.copy()
        headers.update(choice(USER_AGENTS))
        response = requests.get(
            url=api_endpoint, headers=headers, params=params, timeout=30
        )
        try:
            assert response.status_code == 200
        except AssertionError:
            error_message = (
                f"Receiving bad data from Recreation.gov API: {response.text}"
            )
            logger.error(error_message)
            raise ConnectionError(error_message)
        return loads(response.content)

    def _ridb_get_paginate(
        self,
        path: str,
        params: Optional[dict] = None,
    ) -> List[dict]:
        """
        Return the Paginated Response from the RIDP

        Parameters
        ----------
        path: str
            URL Endpoint, see https://ridb.recreation.gov/docs
        params: Optional[dict]
            API Call Parameters

        Returns
        -------
        paginated_response: list
            Concatted Response
        """
        if params is None:
            params = {}
        paginated_response = list()

        data_incomplete = True
        offset: int = 0
        historical_results = 0

        while data_incomplete is True:
            params.update(offset=offset)
            data_response = self.get_ridb_data(path=path, params=params)
            response_object = GenericResponse(**data_response)
            paginated_response += response_object.RECDATA
            result_count = response_object.METADATA.RESULTS.CURRENT_COUNT
            historical_results += result_count
            total_count = response_object.METADATA.RESULTS.TOTAL_COUNT
            if offset >= 500:
                logger.info(
                    f"Too Many Results returned ({total_count}), "
                    "try performing a more specific search"
                )
                data_incomplete = False
            elif historical_results < total_count:
                offset = historical_results
            else:
                data_incomplete = False
        return paginated_response

    @classmethod
    def _filter_facilities_responses(cls, responses=List[dict]) -> List[dict]:
        """
        Filter Facilities to Actual Reservable Campsites

        Parameters
        ----------
        responses

        Returns
        -------
        List[dict]
        """
        filtered_responses = list()
        for possible_match in responses:
            try:
                facility = FacilityResponse(**possible_match)
            except ValidationError as e:
                logger.error("That doesn't look like a valid Campground Facility")
                logger.error(json.dumps(possible_match))
                logger.exception(e)
                raise ProviderSearchError("Invalid Campground Facility Returned")
            if all(
                [
                    facility.FacilityTypeDescription
                    == RIDBConfig.CAMPGROUND_FACILITY_FIELD_QUALIFIER,
                    facility.Enabled is True,
                    facility.Reservable is True,
                ]
            ):
                filtered_responses.append(possible_match)
        return filtered_responses

    @classmethod
    def process_facilities_responses(
        cls, facility: dict
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
        facility_object = FacilityResponse(**facility)
        try:
            facility_state = facility_object.FACILITYADDRESS[0].AddressStateCode.upper()
        except (KeyError, IndexError):
            facility_state = "USA"
        try:
            if len(facility_object.RECAREA) == 0:
                recreation_area_id = facility_object.ParentRecAreaID
                formatted_recreation_area = (
                    f"{facility_object.ORGANIZATION[0].OrgName}, {facility_state}"
                )
            else:
                recreation_area = facility_object.RECAREA[0].RecAreaName
                recreation_area_id = facility_object.RECAREA[0].RecAreaID
                formatted_recreation_area = f"{recreation_area}, {facility_state}"
            campground_facility = CampgroundFacility(
                facility_name=facility_object.FacilityName.title(),
                recreation_area=formatted_recreation_area,
                facility_id=facility_object.FacilityID,
                recreation_area_id=recreation_area_id,
            )
            return facility, campground_facility
        except (KeyError, IndexError):
            return facility, None

    @classmethod
    def _process_rec_area_response(
        cls, recreation_area=dict
    ) -> Tuple[dict, Optional[RecreationArea]]:
        """
        Process Rec Area Responses to be More Usable

        Parameters
        ----------
        recreation_area: dict

        Returns
        -------
        Tuple[dict, RecreationArea]
        """
        rec_area_response = RecreationAreaResponse(**recreation_area)
        try:
            recreation_area_location = rec_area_response.RECAREAADDRESS[
                0
            ].AddressStateCode
            recreation_area_tuple = RecreationArea(
                recreation_area=rec_area_response.RecAreaName,
                recreation_area_id=rec_area_response.RecAreaID,
                recreation_area_location=recreation_area_location,
            )
            return recreation_area, recreation_area_tuple
        except IndexError:
            return recreation_area, None

    @classmethod
    def _rec_availability_get_endpoint(cls, path: str) -> str:
        """
        Return an API Endpoint for the Recreation.gov Campground Availability API

        Parameters
        ----------
        path: str
            URL Endpoint Path

        Returns
        -------
        endpoint_url: str
            URL for the API Endpoint
        """
        base_url = api_utils.generate_url(
            scheme=RecreationBookingConfig.API_SCHEME,
            netloc=RecreationBookingConfig.API_NET_LOC,
            path=RecreationBookingConfig.API_BASE_PATH,
        )
        endpoint_url = parse.urljoin(base_url, path)
        return endpoint_url

    @classmethod
    def make_recdotgov_request(
        cls,
        url: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """
        Make a Raw Request to RecreationDotGov

        Parameters
        ----------
        url: str
        method: str
        params: Optional[Dict[str, Any]]

        Returns
        -------
        requests.Response
        """
        # BUILD THE HEADERS EXPECTED FROM THE API
        headers = STANDARD_HEADERS.copy()
        headers.update(choice(USER_AGENTS))
        headers.update(RecreationBookingConfig.API_REFERRERS)
        response = requests.request(
            method=method, url=url, headers=headers, params=params, timeout=30, **kwargs
        )
        return response

    @classmethod
    @tenacity.retry(
        wait=tenacity.wait_random_exponential(multiplier=2, max=10),
        stop=tenacity.stop.stop_after_delay(15),
    )
    def make_recdotgov_request_retry(
        cls,
        url: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> requests.Response:
        """
        Make a Raw Request to RecreationDotGov - But Handle 404

        Parameters
        ----------
        url: str
        method: str
        params: Optional[Dict[str, Any]]

        Returns
        -------
        requests.Response
        """
        response = cls.make_recdotgov_request(
            url=url, method=method, params=params, **kwargs
        )
        response.raise_for_status()
        return response

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
        params = dict(
            start=0,
            size=1000,
            fq=fq_list,
            include_non_site_specific_campsites=True,
        )
        campsites = []
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

    @tenacity.retry(
        wait=tenacity.wait_random_exponential(multiplier=3, max=1800),
        stop=tenacity.stop.stop_after_delay(6000),
    )
    def _make_recdotgov_availability_request(
        self,
        campground_id: int,
        month: datetime,
    ) -> requests.Response:
        """
        Make a request to the RecreationDotGov API - Handle Exponential Backoff

        Parameters
        ----------
        campground_id
        month

        Returns
        -------
        requests.Response
        """
        try:
            api_endpoint = self._rec_availability_get_endpoint(
                path=f"{campground_id}/{RecreationBookingConfig.API_MONTH_PATH}"
            )
            formatted_month = month.strftime("%Y-%m-01T00:00:00.000Z")
            query_params = dict(start_date=formatted_month)
            response = self.make_recdotgov_request(
                method="GET",
                url=api_endpoint,
                params=query_params,
            )
            assert response.status_code == 200
        except AssertionError:
            response_error = response.text
            error_message = "Bad Data Returned from the RecreationDotGov API"
            logger.debug(f"{error_message}, will continue to retry")
            logger.debug(f"Error Details: {response_error}")
            raise ConnectionError(f"{error_message}: {response_error}")
        return response

    def get_recdotgov_data(
        self, campground_id: int, month: datetime
    ) -> Union[dict, list]:
        """
        Find Campsite Availability Data

        Parameters
        ----------
        campground_id: int
            Campground ID from the RIDB API. Can also be pulled of URLs on Recreation.gov
        month: datetime
            datetime object, results will be filtered to month

        Returns
        -------
        Union[dict, list]
        """
        try:
            response = self._make_recdotgov_availability_request(
                campground_id=campground_id, month=month
            )
        except tenacity.RetryError:
            raise RuntimeError(
                "Something went wrong in fetching data from the "
                "RecreationDotGov API."
            )
        return loads(response.content)

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
                dict(s) for s in set(frozenset(d.items()) for d in list_of_dicts)
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
        availability: dict,
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
        total_campsite_availability: List[Optional[AvailableCampsite]] = list()
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
        logger.info(
            f"\t{logging_utils.get_emoji(total_campsite_availability)}\t"
            f"{len(total_campsite_availability)} total sites found in month of "
            f"{month.strftime('%B')}"
        )
        return total_campsite_availability

    def get_campsite_by_id(self, campsite_id: int) -> CampsiteResponse:
        """
        Get a Campsite's Details

        Parameters
        ----------
        campsite_id: int

        Returns
        -------
        CampsiteResponse
        """
        data = self.get_ridb_data(path=f"{RIDBConfig.CAMPSITE_API_PATH}/{campsite_id}")
        try:
            response = CampsiteResponse(**data[0])
        except IndexError:
            raise ProviderSearchError(f"Campsite with ID #{campsite_id} not found.")
        return response

    def get_campground_ids_by_campsites(
        self, campsite_ids: List[int]
    ) -> Tuple[List[int], List[CampsiteResponse]]:
        """
        Retrieve a list of FacilityIDs, and Facilities from a Campsite ID List

        Parameters
        ----------
        campsite_ids: List[int]
            List of Campsite IDs

        Returns
        -------
        Tuple[List[int], List[CampsiteResponse]]
        """
        campground_ids = list()
        campgrounds = list()
        for campsite_id in campsite_ids:
            campsite = self.get_campsite_by_id(campsite_id=campsite_id)
            campgrounds.append(campsite)
            campground_ids.append(campsite.FacilityID)
        return list(set(campground_ids)), list(campgrounds)

    def _process_specific_campsites_provided(
        self, campsite_id: List[int] = None
    ) -> List[CampgroundFacility]:
        """
        Process Requests for Campgrounds into Facilities

        Parameters
        ----------
        campsite_id: Optional[List[int]]

        Returns
        -------
        List[CampgroundFacility]
        """
        facility_ids, campsites = self.get_campground_ids_by_campsites(
            campsite_ids=campsite_id
        )
        facilities = list()
        for campsite in campsites:
            facility = self._find_facilities_from_campgrounds(
                campground_id=[campsite.FacilityID]
            )[0]
            facilities.append(facility)
            logger.info(
                "Searching Specific Campsite: ⛺️ "
                f"{campsite.CampsiteName} (#{campsite.CampsiteID}) - "
                f"{facility.facility_name}, {facility.recreation_area}"
            )
        return facilities

    def get_internal_campsite_metadata(self, facility_ids: List[int]) -> pd.DataFrame:
        """
        Retrieve Metadata About all of the underlying Campsites to Search
        """
        all_campsites: List[RecDotGovCampsite] = []
        for facility_id in facility_ids:
            all_campsites += self.paginate_recdotgov_campsites(facility_id=facility_id)
        all_campsite_df = pd.DataFrame(
            [item.dict() for item in all_campsites],
            columns=RecDotGovCampsite.__fields__,
        )
        all_campsite_df.set_index("campsite_id", inplace=True)
        return all_campsite_df
