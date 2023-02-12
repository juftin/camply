"""
Recreation.gov Web Searching Utilities
"""

import json
import logging
from abc import ABC, abstractmethod
from base64 import b64decode
from datetime import datetime
from json import loads
from typing import Any, Dict, List, Optional, Tuple, Type, Union
from urllib import parse

import pandas as pd
import ratelimit
import requests
import tenacity
from fake_useragent import UserAgent
from pydantic import ValidationError

from camply.config import STANDARD_HEADERS, RecreationBookingConfig, RIDBConfig
from camply.containers import CampgroundFacility, RecreationArea
from camply.containers.api_responses import (
    CampsiteResponse,
    CoreRecDotGovResponse,
    FacilityResponse,
    GenericResponse,
    RecDotGovCampsite,
    RecreationAreaResponse,
    TourResponse,
)
from camply.containers.base_container import CamplyModel
from camply.providers.base_provider import BaseProvider, ProviderSearchError
from camply.utils import api_utils
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)


class RecreationDotGovBase(BaseProvider, ABC):
    """
    Python Class for Working with Recreation.gov API / NPS APIs
    """

    def __init__(self, api_key: str = None):
        """
        Initialize with Search Dates
        """
        super().__init__()
        if api_key is None:
            _api_key = RIDBConfig.API_KEY
            if isinstance(_api_key, bytes):
                _api_key: str = b64decode(RIDBConfig.API_KEY).decode("utf-8")
        else:
            _api_key: str = api_key
        self._ridb_api_headers: dict = {
            "accept": "application/json",
            "apikey": _api_key,
        }
        _user_agent = UserAgent(use_external_data=False, browsers=["chrome"]).chrome
        self._user_agent = {"User-Agent": _user_agent}

    @property
    @abstractmethod
    def api_search_result_key(self) -> str:
        """
        Entity ID: Related to Searches
        """
        pass

    @property
    @abstractmethod
    def activity_name(self) -> str:
        """
        Activity Name Used In API Query Params
        """
        pass

    @property
    @abstractmethod
    def api_search_result_class(self) -> Type[CamplyModel]:
        """
        Pydantic Object for the Search Results API Response
        """
        pass

    @property
    @abstractmethod
    def facility_type(self) -> str:
        """
        Facility Type: Used for Filtering Campgrounds
        """
        pass

    @property
    @abstractmethod
    def resource_api_path(self) -> str:
        """
        API Endpoint Path
        """
        pass

    @property
    @abstractmethod
    def api_base_path(self) -> str:
        """
        API Base Path - Used in Downstream API Calls.
        """
        pass

    @property
    @abstractmethod
    def api_response_class(self) -> Type[CoreRecDotGovResponse]:
        """
        Pydantic Object Representing the API Response.
        """
        pass

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
        except AssertionError as ae:
            raise RuntimeError(
                "You must provide a search query or state(s) "
                "to find Recreation Areas"
            ) from ae
        if search_string is not None:
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
        logging_messages = []
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
            facilities = []
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
            if self.activity_name:
                kwargs["activity"] = self.activity_name
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
        campgrounds = []
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
        campgrounds = []
        for campground_identifier in campground_id:
            facility_data = self.get_ridb_data(
                path=f"{RIDBConfig.FACILITIES_API_PATH}/{campground_identifier}",
                params={"full": True},
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
            params=dict(query=search, full="true", **kwargs),
        )
        filtered_responses = self._filter_facilities_responses(
            responses=facilities_response
        )
        logger.info(f"{len(filtered_responses)} Matching Campgrounds Found")
        campgrounds = []
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
        headers = self.headers.copy()
        headers.update(self._ridb_api_headers)
        response = self.session.get(
            url=api_endpoint, headers=headers, params=params, timeout=30
        )
        if response.ok is False:
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
        paginated_response = []

        data_incomplete = True
        offset: int = 0
        max_offset: int = 500
        historical_results = 0

        while data_incomplete is True:
            params.update(offset=offset)
            data_response = self.get_ridb_data(path=path, params=params)
            response_object = GenericResponse(**data_response)
            paginated_response += response_object.RECDATA
            result_count = response_object.METADATA.RESULTS.CURRENT_COUNT
            historical_results += result_count
            total_count = response_object.METADATA.RESULTS.TOTAL_COUNT
            if offset >= max_offset:
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
        filtered_responses = []
        for possible_match in responses:
            try:
                facility = FacilityResponse(**possible_match)
            except ValidationError as e:
                logger.error("That doesn't look like a valid Campground Facility")
                logger.error(json.dumps(possible_match))
                logger.exception(e)
                raise ProviderSearchError("Invalid Campground Facility Returned") from e
            if all(
                [
                    facility.FacilityTypeDescription == cls.facility_type,
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
            path=cls.api_base_path,
        )
        endpoint_url = parse.urljoin(base_url, path)
        return endpoint_url

    @classmethod
    @ratelimit.sleep_and_retry
    @ratelimit.limits(calls=3, period=1)
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
        user_agent = {
            "User-Agent": UserAgent(use_external_data=False, browsers=["chrome"]).chrome
        }
        headers = STANDARD_HEADERS.copy()
        headers.update(user_agent)
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
        response = self.make_recdotgov_availability_request(campground_id, month)
        if response.ok is True:
            return response
        else:
            response_error = response.text
            error_message = "Bad Data Returned from the RecreationDotGov API"
            logger.debug(f"{error_message}, will continue to retry")
            logger.debug(f"Error Details: {response_error}")
            raise ConnectionError(f"{error_message}: {response_error}")

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
        except tenacity.RetryError as re:
            raise RuntimeError(
                "Something went wrong in fetching data from the "
                "RecreationDotGov API."
            ) from re
        return loads(response.content)

    def get_campsite_by_id(
        self, campsite_id: int
    ) -> Union[CampsiteResponse, TourResponse]:
        """
        Get a Campsite's Details

        Parameters
        ----------
        campsite_id: int

        Returns
        -------
        CamplyModel
        """
        data = self.get_ridb_data(path=f"{self.resource_api_path}/{campsite_id}")
        try:
            response = self.api_response_class(**data[0])
        except IndexError as ie:
            raise ProviderSearchError(
                f"Campsite with ID #{campsite_id} not found."
            ) from ie
        return response

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
        campground_ids = []
        campgrounds = []
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
        facilities = []
        for campsite in campsites:
            facility = self._find_facilities_from_campgrounds(
                campground_id=[campsite.FacilityID]
            )[0]
            facilities.append(facility)
            # TODO(@juftin): Why did we change this?
            logger.info(
                "Searching Specific Campsite: ⛺️ "
                f"{campsite} - {facility.facility_name}, {facility.recreation_area}"
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
            columns=self.api_search_result_class.__fields__,
        )
        all_campsite_df.set_index(self.api_search_result_key, inplace=True)
        return all_campsite_df
