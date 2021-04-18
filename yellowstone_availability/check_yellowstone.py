#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Check Yellowstone Campground Booking API for Availability
"""

from datetime import datetime
from json import loads
import logging
from os import environ
from time import sleep
from typing import Optional
from urllib import parse

import requests

logger = logging.getLogger(__name__)


class PushoverNotifications(logging.StreamHandler):
    """
    Push Notifications via Pushover + a Logging Handler
    """
    PUSH_TOKEN: str = environ["PUSHOVER_PUSH_TOKEN"]
    PUSH_USER: str = environ["PUSHOVER_PUSH_USER"]

    def __init__(self, level: Optional[int] = logging.INFO):
        logging.StreamHandler.__init__(self)
        self.setLevel(level=level)

    def __repr__(self):
        return "<PushoverNotifications>"

    @staticmethod
    def send_message(message: str, **kwargs) -> requests.Response:
        """
        Send a message via Pushover

        Parameters
        ----------
        message: str

        Returns
        -------
        Response
        """
        response = requests.post(url="https://api.pushover.net/1/messages.json",
                                 headers={"Content-Type": "application/json"},
                                 params=dict(token=PushoverNotifications.PUSH_TOKEN,
                                             user=PushoverNotifications.PUSH_USER,
                                             message=message,
                                             **kwargs)
                                 )
        return response

    def emit(self, record):
        """
        Produce a logging record

        Parameters
        ----------
        record: str
            Message to log
        """
        log_formatted_message = "[{:>10}]: {}".format(record.levelname.upper(),
                                                      record.msg)
        title = f"Pushover {record.levelname.title()} Message"
        self.send_message(message=log_formatted_message, title=title)


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
        url_components = dict(scheme="https", netloc="webapi.xanterra.net",
                              url="/v1/api/availability/hotels/yellowstonenationalparklodges",
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
        webui_url = (f"https://secure.yellowstonenationalparklodges.com/booking/"
                     f"lodging-search?dateFrom={booking_start.strftime('%m-%d-%Y')}&"
                     f"adults={number_of_guests}&children=0&nights={number_of_nights}&"
                     f"destination={lodging_code}")
        return webui_url

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
                          rate_code="INTERNET")
        api_endpoint = cls._get_api_endpoint(query=query_dict)
        logger.info(f"Searching for Yellowstone Lodging Availability: {formatted_date}")

        try:
            all_resort_availability = requests.get(url=api_endpoint,
                                                   headers={"Content-Type": "application/json"})
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
        starting_day_availability = all_resort_availability_data["availability"][
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
            if ":RV" in hotel_code:
                try:
                    hotel_title = hotel_data["rates"]["INTERNET"]["title"]
                    logger.info(f"Searching {hotel_title} ({hotel_code}) for availability.")
                    hotel_rate_mins = hotel_data["rates"]["INTERNET"]["mins"]
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
        check_counter = 0
        while looking_for_booking is True:
            availability_found = YellowstoneLodging.check_yellowstone_lodging(
                booking_start=booking_start,
                number_of_guests=number_of_guests,
                number_of_nights=number_of_nights)
            for hotel_code, lodging_found in availability_found.items():
                if lodging_found is True:
                    looking_for_booking = False
                    break
            logger.info(f"No availabilities found. Waiting {polling_interval} seconds "
                        "before checking again.")
            # Remind every 72nd Run (12 hrs = 10 min * 72)
            if check_counter >= 71:
                PushoverNotifications.send_message(
                    message=(f"Still checking for Yellowstone "
                             f"Campsites to open up: {datetime.now()}"),
                    title="Still looking for Campsites in Yellowstone")
                check_counter = 0
            check_counter += 1
            sleep(polling_interval)


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s [%(name)s]",
                        level=logging.INFO)
    YellowstoneLodging.continuously_check_for_availability(
        booking_start=datetime.strptime(environ["BOOKING_DATE_START"], "%Y-%m-%d"),
        number_of_guests=environ["NUMBER_OF_GUESTS"],
        number_of_nights=environ["NUMBER_OF_NIGHTS"],
        polling_interval=int(environ["POLLING_INTERVAL"]))
