#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Scraping Utilities
"""

from datetime import datetime
from json import loads
import logging
from random import choice
from typing import List, Optional, Tuple, Union
from urllib import parse

import requests
import tenacity

from camply.config import RecreationBookingConfig, RIDBConfig, STANDARD_HEADERS, USER_AGENTS
from camply.containers import AvailableCampsite, CampgroundFacility, RecreationArea
from camply.providers.base_provider import BaseProvider
from camply.utils import api_utils, logging_utils

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
            self.api_key: str = RIDBConfig.API_KEY
        else:
            self.api_key: str = api_key
        if self.api_key is None:
            raise EnvironmentError("Set the RIDB_API_KEY environment variable "
                                   "or provide it manually")
        self._ridb_api_headers: dict = dict(accept="application/json", apikey=self.api_key)
        self._recreation_gov_headers: List[dict] = USER_AGENTS

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
            assert any([kwargs.get("state", None) is not None,
                        search_string is not None and search_string != ""])
        except AssertionError:
            raise RuntimeError("You must provide a search query or state(s) "
                               "to find Recreation Areas")
        logger.info(f'Searching for Recreation Areas: "{search_string}"')
        params = dict(query=search_string, sort="Name", full="true", **kwargs)
        if search_string is None:
            params.pop("query")
        api_response = self._ridb_get_paginate(path=RIDBConfig.REC_AREA_API_PATH,
                                               params=params)
        logger.info(f"{len(api_response)} recreation areas found.")
        logging_messages = list()
        for recreation_area_object in api_response:
            _, recreation_area = self._process_rec_area_response(
                recreation_area=recreation_area_object)
            if recreation_area is not None:
                logging_messages.append(recreation_area)
        self.log_sorted_response(response_array=logging_messages)
        return api_response

    def find_campgrounds(self, search_string: str = None,
                         rec_area_id: Optional[List[int]] = None,
                         campground_id: Optional[List[int]] = None, **kwargs) -> List[dict]:
        """
        Find Matching Campsites Based on Search String

        Parameters
        ----------
        search_string: str
            Search Keyword(s)
        rec_area_id: Optional[List[int]]
            Recreation Area ID to filter with
        campground_id: Optional[List[int]]
            ID of the Campsite

        Returns
        -------
        filtered_responses: List[dict]
            Array of Matching Campsites
        """
        if campground_id not in [None, list()]:
            return self._ridb_get_data(path=f"{RIDBConfig.FACILITIES_API_PATH}/{campground_id}",
                                       params=dict(full=True))
        if rec_area_id is not None:
            facilities = list()
            for recreation_area in rec_area_id:
                facilities += self.find_facilities_per_recreation_area(rec_area_id=recreation_area)
            return facilities
        else:
            if search_string in ["", None] and kwargs.get("state", None) is None:
                raise RuntimeError("You must provide a search query or state to find campsites")
            facilities_response = self._ridb_get_paginate(path=RIDBConfig.FACILITIES_API_PATH,
                                                          params=dict(query=search_string,
                                                                      activity="CAMPING",
                                                                      full="true",
                                                                      **kwargs))
            filtered_responses = self._filter_facilities_responses(responses=facilities_response)
            logger.info(f"{len(filtered_responses)} Matching Campgrounds Found")

            logging_messages = list()
            for facility in filtered_responses:
                _, campground_facility = self.process_facilities_responses(facility=facility)
                if campground_facility is not None:
                    logging_messages.append(campground_facility)
            self.log_sorted_response(response_array=logging_messages)
            return filtered_responses

    def find_facilities_per_recreation_area(self, rec_area_id: int = None, **kwargs) -> List[dict]:
        """
        Find Matching Campsites Based on Search String

        Parameters
        ----------
        rec_area_id: int
            Recreation Area ID

        Returns
        -------
        filtered_responses: List[dict]
            Array of Matching Campsites
        """
        logger.info(f"Retrieving Facility Information for Recreation Area ID: `{rec_area_id}`.")
        api_path = f"{RIDBConfig.REC_AREA_API_PATH}/{rec_area_id}/{RIDBConfig.FACILITIES_API_PATH}"
        api_response = self._ridb_get_paginate(path=api_path, params=dict(full="true", **kwargs))
        filtered_facilities = self._filter_facilities_responses(responses=api_response)
        logging_messages = list()
        logger.info(f"{len(filtered_facilities)} camping facilities found")
        for facility in filtered_facilities:
            _, campground_facility = self.process_facilities_responses(facility=facility)
            if campground_facility is not None:
                logging_messages.append(campground_facility)
        self.log_sorted_response(response_array=logging_messages)
        return filtered_facilities

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
        base_url = api_utils.generate_url(scheme=RIDBConfig.RIDB_SCHEME,
                                          netloc=RIDBConfig.RIDB_NET_LOC,
                                          path=RIDBConfig.RIDB_BASE_PATH)
        endpoint_url = parse.urljoin(base_url, path)
        return endpoint_url

    def _ridb_get_data(self, path: str, params: Optional[dict] = None) -> Union[dict, list]:
        """
        Find Matching Campsites Based on Search String

        Parameters
        ----------
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
        response = requests.get(url=api_endpoint, headers=self._ridb_api_headers,
                                params=params)
        assert response.status_code == 200
        return loads(response.content)

    def _ridb_get_paginate(self, path: str, params: Optional[dict] = None) -> List[dict]:
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
            data_response = self._ridb_get_data(path=path, params=params)
            actual_data = data_response[RIDBConfig.FACILITY_DATA]
            paginated_response += actual_data
            metadata = data_response[RIDBConfig.FACILITY_METADATA]
            result_count = metadata[RIDBConfig.FACILITY_METADATA_RESULTS][
                RIDBConfig.PAGINATE_RESULT_COUNT]
            historical_results += result_count
            total_count = metadata[RIDBConfig.FACILITY_METADATA_RESULTS][
                RIDBConfig.PAGINATE_TOTAL_COUNT]
            if offset >= 500:
                logger.info(f"Too Many Results returned ({total_count}), "
                            "try performing a more specific search")
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

        """
        filtered_responses = list()
        for possible_match in responses:
            facility_type = possible_match[RIDBConfig.CAMPGROUND_FACILITY_FIELD]
            if all([
                facility_type == RIDBConfig.CAMPGROUND_FACILITY_FIELD_QUALIFIER,
                possible_match[RIDBConfig.CAMPGROUND_FACILITY_ENABLED_FIELD] is True,
                possible_match[RIDBConfig.CAMPGROUND_FACILITY_RESERVABLE_FIELD] is True
            ]):
                filtered_responses.append(possible_match)
        return filtered_responses

    @classmethod
    def process_facilities_responses(cls, facility: dict) -> \
            Tuple[dict, Optional[CampgroundFacility]]:
        """
        Process Facilities Responses to be More Usable

        Parameters
        ----------
        facility: dict

        Returns
        -------
        Tuple[dict, CampgroundFacility]
        """
        facility_id = facility[RIDBConfig.FACILITY_ID]
        facility_name = facility[RIDBConfig.FACILITY_NAME]
        try:
            facility_state = facility[RIDBConfig.FACILITY_ADDRESS][0][
                RIDBConfig.FACILITY_LOCATION_STATE].upper()
        except IndexError:
            facility_state = "USA"
        try:
            recreation_area = facility[RIDBConfig.CAMPGROUND_RECREATION_AREA][0][
                RIDBConfig.RECREATION_AREA_NAME]
            recreation_area_id = facility[RIDBConfig.CAMPGROUND_RECREATION_AREA][0][
                RIDBConfig.REC_AREA_ID]
            formatted_recreation_area = f"{recreation_area}, {facility_state}"
            campground_facility = CampgroundFacility(facility_name=facility_name.title(),
                                                     recreation_area=formatted_recreation_area,
                                                     facility_id=facility_id,
                                                     recreation_area_id=recreation_area_id)
            return facility, campground_facility
        except IndexError:
            return facility, None

    @classmethod
    def _process_rec_area_response(cls, recreation_area=dict) -> \
            Tuple[dict, Optional[RecreationArea]]:
        """
        Process Rec Area Responses to be More Usable

        Parameters
        ----------
        recreation_area: dict

        Returns
        -------
        Tuple[dict, RecreationArea]
        """
        recreation_area_id = recreation_area[RIDBConfig.REC_AREA_ID]
        recreation_area_name = recreation_area[RIDBConfig.RECREATION_AREA_NAME]
        try:
            recreation_area_location = recreation_area[RIDBConfig.REC_AREA_ADDRESS][0][
                RIDBConfig.REC_AREA_STATE]
            recreation_area_tuple = RecreationArea(
                recreation_area=recreation_area_name,
                recreation_area_id=recreation_area_id,
                recreation_area_location=recreation_area_location)
            return recreation_area, recreation_area_tuple
        except IndexError:
            return recreation_area, None

    @classmethod
    def _generate_response_string(cls,
                                  response: Union[CampgroundFacility, RecreationArea, str]) -> str:
        """
        Generate a formatted string for logging

        Parameters
        ----------
        response: Union[CampgroundFacility]

        Returns
        -------
        str
        """
        if isinstance(response, CampgroundFacility):
            return (f"⛰  {response.recreation_area} (#{response.recreation_area_id}) - "
                    f"🏕  {response.facility_name} (#{response.facility_id})")
        elif isinstance(response, RecreationArea):
            return (f"⛰  {response.recreation_area}, {response.recreation_area_location} "
                    f"(#{response.recreation_area_id})")
        else:
            return response

    @staticmethod
    def log_sorted_response(response_array: List[object]) -> None:
        """
        Log Some Statements in a Nice Sorted way

        Parameters
        ----------
        response_array: List[str]

        Returns
        -------
        None
        """
        log_array = [RecreationDotGov._generate_response_string(obj) for obj in response_array]
        sorted_logs = sorted(log_array)
        for log_response in sorted_logs:
            logger.info(log_response)

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
        base_url = api_utils.generate_url(scheme=RecreationBookingConfig.API_SCHEME,
                                          netloc=RecreationBookingConfig.API_NET_LOC,
                                          path=RecreationBookingConfig.API_BASE_PATH)
        endpoint_url = parse.urljoin(base_url, path)
        return endpoint_url

    @tenacity.retry(wait=tenacity.wait_random_exponential(multiplier=3, max=1800),
                    stop=tenacity.stop.stop_after_delay(6000))
    def _make_recdotgov_request(self, campground_id: int, month: datetime) -> requests.Response:
        """
        Make a request to the RecreationDotGov API - Handle Exponential Backoff
        Parameters
        ----------
        campground_id
        month

        Returns
        -------
        Returns
        """
        try:
            formatted_month = month.strftime("%Y-%m-01T00:00:00.000Z")
            api_endpoint = self._rec_availability_get_endpoint(
                path=f"{campground_id}/{RecreationBookingConfig.API_MONTH_PATH}")
            # BUILD THE HEADERS EXPECTED FROM THE API
            headers = STANDARD_HEADERS
            headers.update(choice(USER_AGENTS))
            headers.update(RecreationBookingConfig.API_REFERRERS)
            response = requests.get(url=api_endpoint, headers=headers,
                                    params=dict(start_date=formatted_month))
            assert response.status_code == 200
        except AssertionError:
            response_error = response.text
            error_message = f"Bad Data Returned from the RecreationDotGov API"
            logger.debug(f"{error_message}, will continue to retry")
            logger.debug(f"Error Details: {response_error}")
            raise ConnectionError(f"{error_message}: {response_error}")
        return response

    def get_recdotgov_data(self, campground_id: int, month: datetime) -> Union[dict, list]:
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
            response = self._make_recdotgov_request(campground_id=campground_id,
                                                    month=month)
        except tenacity.RetryError:
            raise RuntimeError("Something went wrong in fetching data from the "
                               "RecreationDotGov API.")
        return loads(response.content)

    @classmethod
    def process_campsite_availability(
            cls, availability: dict, recreation_area: str,
            recreation_area_id: int, facility_name: str,
            facility_id: int, month: datetime) -> List[Optional[AvailableCampsite]]:
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

        Returns
        -------
        total_campsite_availability: List[Optional[AvailableCampsite]]
            Any monthly availabilities
        """
        total_campsite_availability: List[Optional[AvailableCampsite]] = list()
        campsite_data = availability[RecreationBookingConfig.CAMPSITE_BASE]
        for campsite_id, site_related_data in campsite_data.items():
            campsite_availabilities = site_related_data[
                RecreationBookingConfig.CAMPSITE_AVAILABILITIES_BASE]
            campsite_loop = site_related_data.get(
                RecreationBookingConfig.CAMPSITE_LOCATION_LOOP,
                RecreationBookingConfig.CAMPSITE_LOCATION_LOOP_DEFAULT)
            campsite_type = site_related_data.get(
                RecreationBookingConfig.CAMPSITE_INFO_TYPE, None)
            campsite_max = site_related_data.get(
                RecreationBookingConfig.CAMPSITE_INFO_MAX_PEOPLE, 1)
            campsite_min = site_related_data.get(
                RecreationBookingConfig.CAMPSITE_INFO_MIN_PEOPLE, 1)
            campsite_use_type = site_related_data.get(
                RecreationBookingConfig.CAMPSITE_INFO_TYPE_OF_USE, None)
            campsite_name = site_related_data.get(
                RecreationBookingConfig.CAMPSITE_LOCATION_SITE,
                RecreationBookingConfig.CAMPSITE_LOCATION_SITE_DEFAULT)
            if campsite_availabilities is None:
                campsite_availabilities = {}
            for date_string, availability_status in campsite_availabilities.items():
                matching_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
                if availability_status not in RecreationBookingConfig.CAMPSITE_UNAVAILABLE_STRINGS:
                    booking_url = f"{RecreationBookingConfig.CAMPSITE_BOOKING_URL}/{campsite_id}"
                    available_campsite = AvailableCampsite(
                        campsite_id=campsite_id,
                        booking_date=matching_date,
                        campsite_site_name=campsite_name,
                        campsite_loop_name=campsite_loop,
                        campsite_type=campsite_type,
                        campsite_occupancy=(campsite_min, campsite_max),
                        campsite_use_type=campsite_use_type,
                        availability_status=availability_status,
                        recreation_area=recreation_area,
                        recreation_area_id=recreation_area_id,
                        facility_name=facility_name,
                        facility_id=facility_id,
                        booking_url=booking_url
                    )
                    total_campsite_availability.append(available_campsite)
        logger.info(f"\t{logging_utils.get_emoji(total_campsite_availability)}\t"
                    f"{len(total_campsite_availability)} total sites found in month of "
                    f"{month.strftime('%B')}")
        return total_campsite_availability