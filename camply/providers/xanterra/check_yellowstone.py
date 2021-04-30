#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Python Class Check Yellowstone Campground Booking API for Availability
"""

from datetime import datetime, timedelta
from json import loads
import logging
from random import choice
from time import sleep
from typing import List, Optional
from urllib import parse

from pandas import DataFrame
import requests

from camply.config import STANDARD_HEADERS, USER_AGENTS, YellowstoneConfig
from camply.containers import AvailableCampsite
from camply.utils.notifications import PushoverNotifications

logger = logging.getLogger(__name__)


# TODO: Build All 3 API Layers (https://webapi.xanterra.net/):
#   - [x] /v1/api/availability/hotels/yellowstonenationalparklodges?date=...
#   - [ ] /v1/api/availability/rooms/yellowstonenationalparklodges/YLYB:RV?date=...
#   - [ ] /v1/api/property/rooms/yellowstonenationalparklodges/YLYB:RV


class YellowstoneLodging(object):
    """
    Scanner for Lodging in Yellowstone
    """

    def __init__(self, booking_start: datetime, number_of_nights: int = 1,
                 number_of_guests: int = 2, polling_interval: int = 600):
        """
        Initialize with Important Campsite Searching Parameters

        Parameters
        ----------
        booking_start : datetime
            Datetime object, will be truncated to the day level
        number_of_nights: int
            Minimum Number of nights staying (defaults to 1)
        number_of_guests: int
            Number of people staying (defaults to 2)
        polling_interval: int
            Amount of seconds to wait in between checks. Defaults to 10 minutes (600)
        """
        self.booking_start = booking_start
        self.number_of_nights = number_of_nights
        self.number_of_guests = number_of_guests
        self.polling_interval: int = YellowstoneConfig.get_polling_interval(
            interval=polling_interval)
        self._formatted_booking_start_dashes = self.booking_start.strftime("%m-%d-%Y")
        self._formatted_booking_start_slashes = self.booking_start.strftime("%m/%d/%Y")

    def __repr__(self):
        """
        String Representation

        Returns
        -------
        str
        """
        return f"<YellowstoneLodging: {self._formatted_booking_start_dashes}>"

    def continuously_check_for_availability(self) -> None:
        """
        Check All Lodging in Yellowstone for Campground Availability

        Returns
        -------
        starting_day_availability: dict
            Returns Data About Yellowstone Availability Beginning on Booking Start
        """
        looking_for_booking = True
        search_start_time = datetime.now()
        while looking_for_booking is True:
            availability_found = self.check_yellowstone_lodging()
            for hotel_code, lodging_found in availability_found.items():
                if lodging_found is True:
                    looking_for_booking = False
                    exit(0)
            logger.info(f"No availabilities found. Waiting {self.polling_interval} seconds "
                        "before checking again.")
            # Remind every 12th hour
            run_time = datetime.now() - search_start_time
            if run_time >= timedelta(hours=12):
                PushoverNotifications.send_message(
                    message=(f"Still checking for Yellowstone "
                             f"Campsites to open up: {datetime.now()}"),
                    title="Still looking for Campsites in Yellowstone")
                search_start_time = datetime.now()
            sleep(self.polling_interval)

    def get_monthly_availability(self) -> dict:
        """
        Check All Lodging in Yellowstone for Campground Data

        Returns
        -------
        data_availability: dict
            Data Availability Dictionary
        """
        query_dict = dict(date=self.booking_start.replace(day=1),
                          limit=31,
                          rate_code=YellowstoneConfig.RATE_CODE)
        api_endpoint = self._get_api_endpoint(url_path=YellowstoneConfig.YELLOWSTONE_LODGING_PATH,
                                              query=None)
        logger.info(f"Searching for Yellowstone Lodging Availability: "
                    f"{self._formatted_booking_start_slashes} | "
                    f"{self.number_of_nights} Nights | {self.number_of_guests} Guests")
        all_resort_availability_data = self._try_retry_get_data(endpoint=api_endpoint,
                                                                params=query_dict)
        return all_resort_availability_data

    @staticmethod
    def _try_retry_get_data(endpoint: str, params: Optional[dict] = None):
        """
        Try and Retry Fetching Data from the Yellowstone API. Unfortunately this is a required
        method to request the data since the Yellowstone API doesn't always return data.

        Parameters
        ----------
        endpoint: str
            API Endpoint
        params

        Returns
        -------

        """
        try:
            # EXPONENTIAL BACKOFF: 27, 81, 243, 729...
            wait_time = 27
            for _ in range(5):
                yellowstone_headers = choice(USER_AGENTS)
                yellowstone_headers.update(STANDARD_HEADERS)
                yellowstone_headers.update(YellowstoneConfig.API_REFERRERS)
                response = requests.get(url=endpoint,
                                        headers=yellowstone_headers,
                                        params=params)
                if response.status_code == 200 and \
                        response.text.strip() != "":
                    break
                logger.warning("Uh oh, something went wrong while requesting data from "
                               f"Yellowstone. Waiting {wait_time} seconds before trying again.")
                sleep(wait_time)
                wait_time *= 3
            assert response.status_code == 200
        except AssertionError:
            error_message = ("Something went wrong with checking the "
                             f"Yellowstone Booking API. Exiting. {response.text}")
            logger.error(error_message)
            PushoverNotifications.send_message(
                message=error_message,
                title="Campsite Search: SOS")
            raise RuntimeError(f"error_message: {response}")
        return loads(response.content)

    def check_yellowstone_lodging(self) -> dict:
        """
        Check All Lodging in Yellowstone for Campground Availability

        Returns
        -------
        data_availability: dict
            Data Availability Dictionary
        """

        all_resort_availability_data = self.get_monthly_availability()
        starting_day_availability = all_resort_availability_data[
            YellowstoneConfig.BOOKING_AVAILABILITY][self._formatted_booking_start_slashes]
        data_availability = self._scan_for_availabilities(
            starting_day_availability=starting_day_availability)
        return data_availability

    @classmethod
    def _get_api_endpoint(cls, url_path: str, query: Optional[dict] = None) -> str:
        """
        Build the API Endpoint for All Yellowstone Lodging
        """
        if query is not None:
            query_string = parse.urlencode(query=query)
        else:
            query_string = ""
        url_components = dict(scheme=YellowstoneConfig.API_SCHEME,
                              netloc=YellowstoneConfig.API_BASE_ENDPOINT,
                              url=url_path,
                              params="", query=query_string, fragment="")
        api_endpoint = parse.urlunparse(tuple(url_components.values()))
        return api_endpoint

    def _return_lodging_url(self, lodging_code: str) -> str:
        """
        Return a Browser Loadable URL to book from

        Parameters
        ----------
        lodging_code: str
            Lodging Code from API

        Returns
        -------
        str
            URL String
        """
        query = dict(dateFrom=self.booking_start,
                     adults=self.number_of_guests,
                     children=0,
                     nights=self.number_of_nights)
        query_string = parse.urlencode(query=query)

        url_components = dict(scheme=YellowstoneConfig.API_SCHEME,
                              netloc=YellowstoneConfig.WEBUI_BASE_ENDPOINT,
                              url=f"{YellowstoneConfig.WEBUI_BOOKING_PATH}/{lodging_code}",
                              params="", query=query_string, fragment="")
        webui_endpoint = parse.urlunparse(tuple(url_components.values()))
        return webui_endpoint

    def _scan_for_availabilities(self, starting_day_availability: dict) -> dict:
        """
        Scan Availability Data and Log any Openings

        Parameters
        ----------
        starting_day_availability: dict
            Data About Yellowstone Availability Beginning on Booking Start

        Returns
        -------
        data_availability: dict
            Data Availability Dictionary
        """
        data_availability = dict()
        for hotel_code, hotel_data in starting_day_availability.items():
            if YellowstoneConfig.LODGING_CAMPGROUND_QUALIFIER in hotel_code:
                try:
                    hotel_title = hotel_data[YellowstoneConfig.LODGING_RATES][
                        YellowstoneConfig.RATE_CODE][
                        YellowstoneConfig.LODGING_TITLE]
                    logger.info(f"Searching {hotel_title} ({hotel_code}) for availability_status.")
                    hotel_rate_mins = hotel_data[YellowstoneConfig.LODGING_RATES][
                        YellowstoneConfig.RATE_CODE][
                        YellowstoneConfig.LODGING_BASE_PRICES]
                    try:
                        minimum_booking_rate = hotel_rate_mins[str(self.number_of_guests)]
                        webui_url = self._return_lodging_url(lodging_code=hotel_code)
                        log_message = (f"Available Booking Found: {hotel_title} | "
                                       f"{self._formatted_booking_start_slashes} | "
                                       f"${minimum_booking_rate}\n"
                                       f"Go get it! {webui_url}")
                        logger.critical(log_message)
                        PushoverNotifications.send_message(
                            message=log_message,
                            title=f"Yellowstone Campground: {hotel_title}")
                        data_availability[hotel_code] = True
                    except KeyError:
                        data_availability[hotel_code] = False
                except (KeyError, TypeError):
                    error_message = hotel_data["message"]
                    logger.debug(
                        f"Something went wrong searching for {hotel_code}: {error_message}")
                    data_availability[hotel_code] = False
        return data_availability

    def _compile_campground_availabilities(self, availability: dict) -> List[AvailableCampsite]:
        """

        Parameters
        ----------
        availability

        Returns
        -------

        """
        available_campsites = list()
        for date_string in availability.keys():
            booking_date = datetime.strptime(date_string, "%m/%d/%Y")
            daily_data = availability[date_string]
            camping_keys = [key for key in daily_data.keys() if
                            YellowstoneConfig.LODGING_CAMPGROUND_QUALIFIER in key]
            for hotel_code in camping_keys:
                hotel_data = daily_data[hotel_code]
                try:
                    hotel_title = hotel_data[YellowstoneConfig.LODGING_RATES][
                        YellowstoneConfig.RATE_CODE][
                        YellowstoneConfig.LODGING_TITLE]
                    hotel_rate_mins = hotel_data[YellowstoneConfig.LODGING_RATES][
                        YellowstoneConfig.RATE_CODE][
                        YellowstoneConfig.LODGING_BASE_PRICES]
                    if hotel_rate_mins != {"1": 0}:
                        min_capacity = int(min(hotel_rate_mins.keys()))
                        max_capacity = int(max(hotel_rate_mins.keys()))
                        capacity = (min_capacity, max_capacity)
                        webui_url = self._return_lodging_url(lodging_code=hotel_code)
                        campsite = dict(campsite_id=None,
                                        booking_date=booking_date,
                                        campsite_occupancy=capacity,
                                        recreation_area="Yellowstone",
                                        recreation_area_id=1,
                                        facility_name=hotel_title,
                                        facility_id=hotel_code,
                                        booking_url=webui_url)
                        available_campsites.append(campsite)
                except (KeyError, TypeError):
                    error_message = hotel_data["message"]
                    logger.debug(
                        f"Something went wrong searching for {hotel_code}: {error_message}")
        return available_campsites

    def _gather_campsite_specific_availability(
            self, available_campsites: List[AvailableCampsite]) -> List[dict]:
        """
        Given a DataFrame of campsite availability, return updated Data with details about the
        actual campsites that are available (i.e Tent Size, RV Length, Etc)

        Parameters
        ----------
        campsite_df: DataFrame
            Dataframe of Availability data

        Returns
        -------
        DataFrame
        """
        available_room_array = list()
        availability_df = DataFrame(data=available_campsites)
        for facility_id, facility_df in availability_df.groupby(YellowstoneConfig.FACILITY_ID):
            api_endpoint = self._get_api_endpoint(
                url_path=YellowstoneConfig.YELLOWSTONE_CAMPSITE_AVAILABILITY,
                query=None)
            params = dict(date=self.booking_start.replace(day=1), limit=31)
            campsite_data = self._try_retry_get_data(endpoint=f"{api_endpoint}/{facility_id}",
                                                     params=params)
            campsite_availability = campsite_data[YellowstoneConfig.BOOKING_AVAILABILITY]
            booking_dates = campsite_availability.keys()
            for booking_date_str in booking_dates:
                daily_availability = campsite_availability[booking_date_str]
                if daily_availability[YellowstoneConfig.FACILITY_STATUS] == \
                        YellowstoneConfig.FACILITY_STATUS_QUALIFIER:
                    available_rooms = daily_availability[YellowstoneConfig.FACILITY_ROOMS]
                    for room in available_rooms:
                        if room[YellowstoneConfig.FACILITY_AVAILABLE_QUALIFIER] > 0:
                            available_room_array.append(dict(
                                booking_date=booking_date_str,
                                facility_id=facility_id,
                                campsite_code=room[YellowstoneConfig.FACILITY_ROOM_CODE],
                                available=room[YellowstoneConfig.FACILITY_AVAILABLE_QUALIFIER],
                                price=room[YellowstoneConfig.FACILITY_PRICE],
                            ))
        return available_room_array

    def _get_property_information(self, available_rooms: List[dict]) -> List[dict]:
        """

        Parameters
        ----------
        facility_id

        Returns
        -------

        """
        property_info_array = list()
        availability_df = DataFrame(data=available_rooms)
        facility_identifiers = availability_df[YellowstoneConfig.FACILITY_ID].unique()
        for facility_id in facility_identifiers:
            api_endpoint = self._get_api_endpoint(
                url_path=YellowstoneConfig.YELLOWSTONE_PROPERTY_INFO,
                query=None)
            campsite_info = self._try_retry_get_data(endpoint=f"{api_endpoint}/{facility_id}")
            campsite_codes = campsite_info.keys()
            for campsite_code in campsite_codes:
                campsite_data = campsite_info[campsite_code]
                property_info_array.append(dict(
                    facility_id=facility_id,
                    campsite_code=campsite_code,
                    campsite_title=campsite_data["title"],
                    campsite_type=campsite_data["type"].upper(),
                    capacity=(campsite_data["occupancyBase"], campsite_data["occupancyMax"])
                ))
        return property_info_array
