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
from urllib import parse

import requests

from camply.config import API_HEADERS, YellowstoneConfig
from camply.utils.notifications import PushoverNotifications

logger = logging.getLogger(__name__)


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

    def check_yellowstone_lodging(self) -> dict:
        """
        Check All Lodging in Yellowstone for Campground Availability

        Returns
        -------
        data_availability: dict
            Data Availability Dictionary
        """
        query_dict = dict(date=self._formatted_booking_start_slashes,
                          nights=self.number_of_nights,
                          limit=self.number_of_nights,
                          adults=self.number_of_guests,
                          rate_code=YellowstoneConfig.RATE_CODE)
        api_endpoint = self._get_api_endpoint(query=query_dict)
        logger.info(f"Searching for Yellowstone Lodging Availability: "
                    f"{self._formatted_booking_start_slashes} | "
                    f"{self.number_of_nights} Nights | {self.number_of_guests} Guests")

        try:
            # EXPONENTIAL BACKOFF: 27, 81, 243, 729...
            wait_time = 27
            for _ in range(5):
                yellowstone_headers = choice(API_HEADERS)
                yellowstone_headers.update(YellowstoneConfig.API_HEADERS)
                all_resort_availability = requests.get(url=api_endpoint,
                                                       headers=yellowstone_headers)
                if all_resort_availability.status_code == 200 and \
                        all_resort_availability.text.strip() != "":
                    break
                logger.warning("Uh oh, something went wrong while requesting data from "
                               f"Yellowstone. Waiting {wait_time} seconds before trying again.")
                sleep(wait_time)
                wait_time *= 3
            assert all_resort_availability.status_code == 200
        except AssertionError:
            error_message = ("Something went wrong with checking the "
                             f"Yellowstone Booking API. Exiting. {all_resort_availability.text}")
            logger.error(error_message)
            PushoverNotifications.send_message(
                message=error_message,
                title="Campsite Search: SOS")
            raise RuntimeError(f"error_message: {all_resort_availability}")
        all_resort_availability_data = loads(all_resort_availability.content)
        starting_day_availability = all_resort_availability_data[
            YellowstoneConfig.BOOKING_AVAILABILITY][self._formatted_booking_start_slashes]
        data_availability = self._scan_for_availabilities(
            starting_day_availability=starting_day_availability)
        return data_availability

    @classmethod
    def _get_api_endpoint(cls, query) -> str:
        """
        Build the API Endpoint for All Yellowstone Lodging
        """
        query_string = parse.urlencode(query=query)
        url_components = dict(scheme=YellowstoneConfig.API_SCHEME,
                              netloc=YellowstoneConfig.API_BASE_ENDPOINT,
                              url=YellowstoneConfig.YELLOWSTONE_LODGING_PATH,
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
        query = dict(dateFrom=self._formatted_booking_start_dashes,
                     adults=self.number_of_guests,
                     children=0,
                     nights=self.number_of_nights,
                     destination=lodging_code)
        query_string = parse.urlencode(query=query)
        url_components = dict(scheme=YellowstoneConfig.API_SCHEME,
                              netloc=YellowstoneConfig.WEBUI_BASE_ENDPOINT,
                              url=YellowstoneConfig.WEBUI_BOOKING_PATH,
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
