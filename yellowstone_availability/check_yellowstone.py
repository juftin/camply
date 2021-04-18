#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Python Class Check Yellowstone Campground Booking API for Availability
"""

from datetime import datetime, timedelta
from json import loads
import logging
from time import sleep
from urllib import parse

import requests

from yellowstone_availability.config import YellowstoneConfig
from yellowstone_availability.notifications import PushoverNotifications

logger = logging.getLogger(__name__)


class YellowstoneLodging(object):
    """
    Scanner for Lodging in Yellowstone
    """

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

    @classmethod
    def _return_lodging_url(cls, booking_start: datetime, number_of_nights: int,
                            number_of_guests: int, lodging_code: str) -> str:
        """
        Return a Browser Loadable URL to book from

        Parameters
        ----------
        booking_start : datetime
            Datetime object, will be truncated to the day level
        number_of_nights: int
            Minimum Number of nights staying
        number_of_guests: int
            Number of people staying (defaults to 2)
        lodging_code: str
            Lodging Code from API

        Returns
        -------
        str
            URL String
        """
        query = dict(dateFrom=booking_start.strftime('%m-%d-%Y'),
                     adults=number_of_guests,
                     children=0,
                     nights=number_of_nights,
                     destination=lodging_code)
        query_string = parse.urlencode(query=query)
        url_components = dict(scheme=YellowstoneConfig.API_SCHEME,
                              netloc=YellowstoneConfig.WEBUI_BASE_ENDPOINT,
                              url=YellowstoneConfig.WEBUI_BOOKING_PATH,
                              params="", query=query_string, fragment="")
        webui_endpoint = parse.urlunparse(tuple(url_components.values()))
        return webui_endpoint

    @classmethod
    def check_yellowstone_lodging(cls, booking_start: datetime, number_of_nights: int = 1,
                                  number_of_guests: int = 2) -> dict:
        """
        Check All Lodging in Yellowstone for Campground Availability

        Parameters
        ----------
        booking_start : datetime
            Datetime object, will be truncated to the day level
        number_of_nights: int
            Minimum Number of nights staying
        number_of_guests: int
            Number of people staying (defaults to 2)

        Returns
        -------
        data_availability: dict
            Data Availability Dictionary
        """
        formatted_date = booking_start.strftime("%m/%d/%Y")
        query_dict = dict(date=formatted_date,
                          nights=number_of_nights,
                          limit=number_of_nights,
                          adults=number_of_guests,
                          rate_code=YellowstoneConfig.RATE_CODE)
        api_endpoint = cls._get_api_endpoint(query=query_dict)
        logger.info(f"Searching for Yellowstone Lodging Availability: {formatted_date} | "
                    f"{number_of_nights} Nights | {number_of_guests} Guests")

        try:
            # EXPONENTIAL BACKOFF: 9, 27, 81, 243, 729...
            wait_time = 9
            for _ in range(5):
                all_resort_availability = requests.get(url=api_endpoint,
                                                       headers=YellowstoneConfig.API_HEADERS)
                if all_resort_availability.status_code == 200:
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
            YellowstoneConfig.BOOKING_AVAILABILITY][
            formatted_date]
        data_availability = cls._scan_for_availabilities(
            booking_start=booking_start,
            number_of_guests=number_of_guests,
            number_of_nights=number_of_nights,
            starting_day_availability=starting_day_availability)
        return data_availability

    @classmethod
    def _scan_for_availabilities(cls, booking_start: datetime, number_of_nights: int,
                                 number_of_guests: int,
                                 starting_day_availability: dict) -> dict:
        """
        Scan Availability Data and Log any Openings

        Parameters
        ----------
        booking_start : datetime
            Datetime object, will be truncated to the day level
        number_of_nights: int
            Minimum Number of nights staying
        number_of_guests: int
            Number of people staying (defaults to 2)
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
                    logger.info(f"Searching {hotel_title} ({hotel_code}) for availability.")
                    hotel_rate_mins = hotel_data[YellowstoneConfig.LODGING_RATES][
                        YellowstoneConfig.RATE_CODE][
                        YellowstoneConfig.LODGING_BASE_PRICES]
                    try:
                        minimum_booking_rate = hotel_rate_mins[str(number_of_guests)]
                        webui_url = cls._return_lodging_url(booking_start=booking_start,
                                                            number_of_guests=number_of_guests,
                                                            number_of_nights=number_of_nights,
                                                            lodging_code=hotel_code)
                        log_message = (f"Available Booking Found: {hotel_title} | "
                                       f"{booking_start.strftime('%m/%d/%Y')} | "
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

    @classmethod
    def continuously_check_for_availability(cls, booking_start: datetime, number_of_nights: int,
                                            number_of_guests: int,
                                            polling_interval: int = 600) -> None:
        """
        Check All Lodging in Yellowstone for Campground Availability

        Parameters
        ----------
        booking_start : datetime
            Datetime object, will be truncated to the day level
        number_of_nights: int
            Minimum Number of nights staying
        number_of_guests: int
            Number of people staying (defaults to 2)
        polling_interval: int
            Amount of seconds to wait in between checks. Defaults to 10 minutes (600)

        Returns
        -------
        starting_day_availability: dict
            Returns Data About Yellowstone Availability Beginning on Booking Start
        """
        looking_for_booking = True
        sleep_time = YellowstoneConfig.get_polling_interval(interval=polling_interval)
        search_start_time = datetime.now()
        while looking_for_booking is True:
            availability_found = YellowstoneLodging.check_yellowstone_lodging(
                booking_start=booking_start,
                number_of_guests=number_of_guests,
                number_of_nights=number_of_nights)
            for hotel_code, lodging_found in availability_found.items():
                if lodging_found is True:
                    looking_for_booking = False
                    exit(0)
            logger.info(f"No availabilities found. Waiting {polling_interval} seconds "
                        "before checking again.")
            # Remind every 12th hour
            run_time = datetime.now() - search_start_time
            if run_time >= timedelta(hours=12):
                PushoverNotifications.send_message(
                    message=(f"Still checking for Yellowstone "
                             f"Campsites to open up: {datetime.now()}"),
                    title="Still looking for Campsites in Yellowstone")
                search_start_time = datetime.now()
            sleep(sleep_time)
