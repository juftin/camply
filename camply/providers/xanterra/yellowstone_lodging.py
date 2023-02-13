"""
Python Class Check Yellowstone Campground Booking API for Availability
"""

import logging
from datetime import datetime, timedelta
from json import loads
from typing import List, Optional
from urllib import parse

import requests
import tenacity
from fake_useragent import UserAgent
from pandas import DataFrame, to_datetime
from pytz import timezone

from camply.config import STANDARD_HEADERS, YellowstoneConfig
from camply.containers import AvailableCampsite, CampgroundFacility, RecreationArea
from camply.containers.api_responses import XantResortData
from camply.providers.base_provider import BaseProvider
from camply.utils import logging_utils
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)


class YellowstoneLodging(BaseProvider):
    """
    Scanner for Lodging in Yellowstone
    """

    recreation_area = RecreationArea(
        recreation_area=YellowstoneConfig.YELLOWSTONE_RECREATION_AREA_FULL_NAME,
        recreation_area_id=YellowstoneConfig.YELLOWSTONE_RECREATION_AREA_ID,
        recreation_area_location="USA",
    )

    def __repr__(self):
        """
        String Representation

        Returns
        -------
        str
        """
        return "<YellowstoneLodging>"

    def _get_monthly_availability(self, month: datetime, nights: int = None) -> dict:
        """
        Check All Lodging in Yellowstone for Campground Data

        Returns
        -------
        data_availability: dict
            Data Availability Dictionary
        """
        query_dict = {
            "date": self._ensure_current_month(month=month),
            "limit": 31,
            "rate_code": YellowstoneConfig.RATE_CODE,
        }
        if nights is not None:
            query_dict.update({"nights": nights})
        api_endpoint = self._get_api_endpoint(
            url_path=YellowstoneConfig.YELLOWSTONE_LODGING_PATH, query=None
        )
        logger.info(
            f"Searching for Yellowstone Lodging Availability: {month.strftime('%B, %Y')}"
        )
        all_resort_availability_data = self.make_yellowstone_request(
            endpoint=api_endpoint, params=query_dict
        )
        return all_resort_availability_data

    @staticmethod
    @tenacity.retry(
        wait=tenacity.wait_random_exponential(multiplier=3, max=1800),
        stop=tenacity.stop.stop_after_delay(6000),
    )
    def _try_retry_get_data(endpoint: str, params: Optional[dict] = None) -> dict:
        """
        Try and Retry Fetching Data from the Yellowstone API.

        Unfortunately this is a required method to request the data since the
        Yellowstone API doesn't always return data.

        Parameters
        ----------
        endpoint: str
            API Endpoint
        params

        Returns
        -------
        dict
        """
        yellowstone_headers = {}
        user_agent = {
            "User-Agent": UserAgent(use_external_data=False, browsers=["chrome"]).chrome
        }
        yellowstone_headers.update(user_agent)
        yellowstone_headers.update(STANDARD_HEADERS)
        yellowstone_headers.update(YellowstoneConfig.API_REFERRERS)
        response = requests.get(
            url=endpoint, headers=yellowstone_headers, params=params, timeout=30
        )
        if response.ok is True and response.text.strip() != "":
            return loads(response.content)
        else:
            error_message = (
                "Something went wrong with checking the "
                "Yellowstone Booking API. Will continue retrying."
            )
            logger.warning(error_message)
            raise RuntimeError(error_message)

    @staticmethod
    def make_yellowstone_request(endpoint: str, params: Optional[dict] = None) -> dict:
        """
        Try and Retry Fetching Data from the Yellowstone API.

        Unfortunately this is a required method to request the data since the
        Yellowstone API doesn't always return data.

        Parameters
        ----------
        endpoint: str
            API Endpoint
        params

        Returns
        -------
        dict
        """
        try:
            content = YellowstoneLodging._try_retry_get_data(
                endpoint=endpoint, params=params
            )
        except RuntimeError as re:
            raise RuntimeError(f"error_message: {re}") from re
        return content

    @classmethod
    def _get_api_endpoint(cls, url_path: str, query: Optional[dict] = None) -> str:
        """
        Build the API Endpoint for All Yellowstone Lodging
        """
        if query is not None:
            query_string = parse.urlencode(query=query)
        else:
            query_string = ""
        url_components = {
            "scheme": YellowstoneConfig.API_SCHEME,
            "netloc": YellowstoneConfig.API_BASE_ENDPOINT,
            "url": url_path,
            "params": "",
            "query": query_string,
            "fragment": "",
        }
        api_endpoint = parse.urlunparse(tuple(url_components.values()))
        return api_endpoint

    @classmethod
    def _return_lodging_url(
        cls, lodging_code: str, month: datetime, params: Optional[dict] = ""
    ) -> str:
        """
        Return a Browser Loadable URL to book from

        Parameters
        ----------
        lodging_code: str
            Lodging Code from API
        month: datetime
            Month to return bookings filtered to
        params: Optional[dict]
            Optional URL Parameters

        Returns
        -------
        str
            URL String
        """
        query = {
            "dateFrom": month.strftime("%m-%d-%Y"),
            "adults": 1,
            "destination": lodging_code,
            "children": 0,
        }
        if params is not None:
            query.update(params)
        query_string = parse.urlencode(query=query)

        url_components = {
            "scheme": YellowstoneConfig.API_SCHEME,
            "netloc": YellowstoneConfig.WEBUI_BASE_ENDPOINT,
            "url": YellowstoneConfig.WEBUI_BOOKING_PATH,
            "params": "",
            "query": query_string,
            "fragment": "",
        }
        webui_endpoint = parse.urlunparse(tuple(url_components.values()))
        return webui_endpoint

    @classmethod
    def _compile_campground_availabilities(
        cls, availability: XantResortData
    ) -> List[dict]:
        """
        Gather Data about campground availabilities within a JSON Availability Objet

        Parameters
        ----------
        availability: ResortData
            JSON Availability Object

        Returns
        -------
        available_campsites:  List[dict]
            List of Availabilities as JSON
        """
        available_campsites = []
        for booking_date, daily_data in availability.availability.items():
            camping_keys = [
                key
                for key in daily_data.keys()
                if YellowstoneConfig.LODGING_CAMPGROUND_QUALIFIER in key
            ]
            for hotel_code in camping_keys:
                hotel_data = daily_data[hotel_code]
                try:
                    hotel_title = hotel_data.rates[YellowstoneConfig.RATE_CODE].title
                    hotel_rate_mins = hotel_data.rates[YellowstoneConfig.RATE_CODE].mins
                    if hotel_rate_mins != {1: 0}:
                        min_capacity = min(hotel_rate_mins.keys())
                        max_capacity = max(hotel_rate_mins.keys())
                        capacity = (min_capacity, max_capacity)
                        campsite = {
                            "campsite_id": None,
                            "booking_date": booking_date,
                            "campsite_occupancy": capacity,
                            "recreation_area": YellowstoneConfig.YELLOWSTONE_RECREATION_AREA_NAME,
                            "recreation_area_id": YellowstoneConfig.YELLOWSTONE_RECREATION_AREA_ID,
                            "facility_name": hotel_title.replace(
                                *YellowstoneConfig.YELLOWSTONE_CAMPGROUND_NAME_REPLACE
                            ),
                            "facility_id": hotel_code,
                        }
                        available_campsites.append(campsite)
                except KeyError:
                    pass
        logger.info(
            f"\t{logging_utils.get_emoji(available_campsites)}\t"
            f"{len(available_campsites)} sites found."
        )
        return available_campsites

    def _gather_campsite_specific_availability(
        self,
        available_campsites: List[dict],
        month: datetime,
        nights: Optional[int] = None,
    ) -> List[dict]:
        """
        Get campsite extra information

        Given a DataFrame of campsite availability, return updated Data with details
        about the actual campsites that are available (i.e Tent Size, RV Length, Etc)

        Parameters
        ----------
        available_campsites: List[dict]
            List of Available Campsites as JSON objects
        month: datetime
            Month object

        Returns
        -------
        List[dict]
        """
        available_room_array = []
        availability_df = DataFrame(data=available_campsites)
        if availability_df.empty is True:
            return available_room_array
        for facility_id, _facility_df in availability_df.groupby(
            YellowstoneConfig.FACILITY_ID
        ):
            api_endpoint = self._get_api_endpoint(
                url_path=YellowstoneConfig.YELLOWSTONE_CAMPSITE_AVAILABILITY, query=None
            )
            params = {"date": self._ensure_current_month(month=month), "limit": 31}
            if nights is not None:
                params.update({"nights": nights})
            campsite_data = self.make_yellowstone_request(
                endpoint=f"{api_endpoint}/{facility_id}", params=params
            )
            campsite_availability = campsite_data[
                YellowstoneConfig.BOOKING_AVAILABILITY
            ]
            booking_dates = campsite_availability.keys()
            availabilities = self._process_daily_availability(
                booking_dates=booking_dates,
                campsite_availability=campsite_availability,
                facility_id=facility_id,
            )
            available_room_array += availabilities
        return available_room_array

    @classmethod
    def _process_daily_availability(
        cls, booking_dates: List[str], campsite_availability: dict, facility_id: str
    ) -> List[dict]:
        """
        Process Monthly Availability

        Parameters
        ----------
        booking_dates: List[str]
            List of booking dates to process
        campsite_availability: dict
            Campsite availability dict
        facility_id: str
            Identification of the Facility

        Returns
        -------
        List[dict]
        """
        daily_availabilities = []
        for booking_date_str in booking_dates:
            daily_availability = campsite_availability[booking_date_str]
            if (
                daily_availability[YellowstoneConfig.FACILITY_STATUS]
                == YellowstoneConfig.FACILITY_STATUS_QUALIFIER
            ):
                available_rooms = daily_availability[YellowstoneConfig.FACILITY_ROOMS]
                for room in available_rooms:
                    if room[YellowstoneConfig.FACILITY_AVAILABLE_QUALIFIER] > 0:
                        daily_availabilities.append(
                            {
                                "booking_date": booking_date_str,
                                "facility_id": facility_id,
                                "campsite_code": room[
                                    YellowstoneConfig.FACILITY_ROOM_CODE
                                ],
                                "available": room[
                                    YellowstoneConfig.FACILITY_AVAILABLE_QUALIFIER
                                ],
                                "price": room[YellowstoneConfig.FACILITY_PRICE],
                            }
                        )
        return daily_availabilities

    def _get_property_information(self, available_rooms: List[dict]) -> List[dict]:
        """
        Gather Information About All Campgrounds / Hotels within Yellowstone

        Parameters
        ----------
        available_rooms: List[dict]

        Returns
        -------
        List[dict]
        """
        property_info_array = []
        availability_df = DataFrame(data=available_rooms)
        if availability_df.empty is True:
            return property_info_array
        facility_identifiers = availability_df[YellowstoneConfig.FACILITY_ID].unique()
        for facility_id in facility_identifiers:
            api_endpoint = self._get_api_endpoint(
                url_path=YellowstoneConfig.YELLOWSTONE_PROPERTY_INFO, query=None
            )
            campsite_info = self.make_yellowstone_request(
                endpoint=f"{api_endpoint}/{facility_id}"
            )
            campsite_codes = campsite_info.keys()
            for campsite_code in campsite_codes:
                campsite_data = campsite_info[campsite_code]
                property_info_array.append(
                    {
                        "facility_id": facility_id,
                        "campsite_code": campsite_code,
                        "campsite_title": campsite_data[
                            YellowstoneConfig.LODGING_TITLE
                        ],
                        "campsite_type": campsite_data[
                            YellowstoneConfig.FACILITY_TYPE
                        ].upper(),
                        "capacity": (
                            campsite_data[YellowstoneConfig.LODGING_OCCUPANCY_BASE],
                            campsite_data[YellowstoneConfig.LODGING_OCCUPANCY_MAX],
                        ),
                    }
                )
        return property_info_array

    def get_monthly_campsites(
        self, month: datetime, nights: Optional[int] = None
    ) -> List[AvailableCampsite]:
        """
        Return All Campsites Available in a Given Month

        Parameters
        ----------
        month: datetime
            Month to Search
        nights: Optional[int]
            Search for consecutive nights

        Returns
        -------
        List[AvailableCampsite]
        """
        now = datetime.now().date()
        search_date = month.replace(day=1)
        if month <= now:
            logger.info(
                "Cannot input search dates before today, adjusting search parameters."
            )
            search_date = search_date.replace(
                year=now.year, month=now.month, day=now.day
            )
        availability_found = self._get_monthly_availability(
            month=search_date, nights=nights
        )
        availability = XantResortData(**availability_found)
        monthly_campsites = self._compile_campground_availabilities(
            availability=availability
        )
        campsite_data = DataFrame(
            monthly_campsites, columns=YellowstoneConfig.CAMPSITE_DATA_COLUMNS
        ).drop_duplicates()
        if campsite_data.empty is True:
            return []
        available_room_array = self._gather_campsite_specific_availability(
            available_campsites=monthly_campsites, month=month, nights=nights
        )
        available_rooms = DataFrame(available_room_array)
        property_info = self._get_property_information(
            available_rooms=available_room_array
        )
        properties = DataFrame(property_info)
        merged_campsites = available_rooms.merge(
            properties,
            on=[
                YellowstoneConfig.FACILITY_ID_COLUMN,
                YellowstoneConfig.CAMPSITE_ID_COLUMN,
            ],
        )
        merged_campsites[YellowstoneConfig.BOOKING_DATE_COLUMN] = to_datetime(
            merged_campsites[YellowstoneConfig.BOOKING_DATE_COLUMN]
        )
        if nights is not None:
            nights_param = {"nights": nights}
        else:
            nights_param = {"nights": 1}
        booking_nights = nights_param.get("nights")
        merged_campsites[YellowstoneConfig.BOOKING_END_DATE_COLUMN] = merged_campsites[
            YellowstoneConfig.BOOKING_DATE_COLUMN
        ] + timedelta(days=booking_nights)
        merged_campsites[YellowstoneConfig.BOOKING_NIGHTS_COLUMN] = booking_nights
        final_campsites = merged_campsites.merge(
            campsite_data, on=YellowstoneConfig.FACILITY_ID_COLUMN
        ).sort_values(by=YellowstoneConfig.BOOKING_DATE_COLUMN)
        final_campsites[YellowstoneConfig.BOOKING_URL_COLUMN] = final_campsites.apply(
            lambda x: self._return_lodging_url(
                lodging_code=x.facility_id, month=x.booking_date, params=nights_param
            ),
            axis=1,
        )
        all_monthly_campsite_array = self._df_to_campsites(campsite_df=final_campsites)
        return all_monthly_campsite_array

    @classmethod
    def _df_to_campsites(cls, campsite_df: DataFrame) -> List[AvailableCampsite]:
        """
        Transform a DataFrame into an array of AvailableCampsites

        Parameters
        ----------
        campsite_df: DataFrame

        Returns
        -------
        List[AvailableCampsite]
        """
        all_monthly_campsite_array = []
        for _, row in campsite_df.iterrows():
            campsite = AvailableCampsite(
                campsite_id=row[YellowstoneConfig.CAMPSITE_ID_COLUMN],
                booking_date=row[YellowstoneConfig.BOOKING_DATE_COLUMN],
                booking_end_date=row[YellowstoneConfig.BOOKING_END_DATE_COLUMN],
                booking_nights=row[YellowstoneConfig.BOOKING_NIGHTS_COLUMN],
                campsite_site_name=row[YellowstoneConfig.CAMPSITE_SITE_NAME_COLUMN],
                campsite_loop_name=YellowstoneConfig.YELLOWSTONE_LOOP_NAME,
                campsite_type=row[YellowstoneConfig.CAMPSITE_TYPE_COLUMN],
                campsite_occupancy=row[YellowstoneConfig.CAMPSITE_OCCUPANCY_COLUMN],
                campsite_use_type=row[YellowstoneConfig.CAMPSITE_USE_TYPE_COLUMN],
                availability_status=YellowstoneConfig.CAMPSITE_AVAILABILITY_STATUS,
                recreation_area=YellowstoneConfig.YELLOWSTONE_RECREATION_AREA_NAME,
                recreation_area_id=YellowstoneConfig.YELLOWSTONE_RECREATION_AREA_ID,
                facility_name=row[YellowstoneConfig.FACILITY_NAME_COLUMN],
                facility_id=row[YellowstoneConfig.FACILITY_ID_COLUMN],
                booking_url=row[YellowstoneConfig.BOOKING_URL_COLUMN],
            )
            all_monthly_campsite_array.append(campsite)
        return all_monthly_campsite_array

    @classmethod
    def _ensure_current_month(cls, month: datetime) -> datetime:
        """
        Ensure That We Never Give the Yellowstone API Dates in the past.

        Parameters
        ----------
        month: datetime

        Returns
        -------
        datetime
        """
        yellowstone_timezone = timezone(YellowstoneConfig.YELLOWSTONE_TIMEZONE)
        yellowstone_current_time = datetime.now(yellowstone_timezone).date()
        today = datetime(
            year=yellowstone_current_time.year,
            month=yellowstone_current_time.month,
            day=yellowstone_current_time.day,
        ).date()
        if today > month:
            month = today
        return month

    def find_campgrounds(self, **kwargs) -> List[CampgroundFacility]:
        """
        Print the Campgrounds inside of Yellowstone
        """
        log_sorted_response(YellowstoneConfig.YELLOWSTONE_CAMPGROUND_OBJECTS)
        return YellowstoneConfig.YELLOWSTONE_CAMPGROUND_OBJECTS
