#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Camply CLI
"""

from argparse import ArgumentParser, Namespace
from datetime import datetime
import logging
from os import getenv
from typing import Optional

from camply.containers import SearchWindow
from camply.providers import RecreationDotGov
from camply.search import CAMPSITE_SEARCH_PROVIDER
from camply.utils import log_camply

logging.Logger.camply = log_camply
logger = logging.getLogger(__name__)


def main():
    """
    Run the Camply CLI. The CLI is wrapped in a main() function to
    interface with Poetry

    Returns
    ------
    None
    """
    logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                        level=logging.getLevelName(getenv("LOG_LEVEL", "INFO")))
    try:
        logger.camply("camply, the campsite finder ⛺️")
        camply_cli = CamplyCommandLine()
        camply_cli.run_cli()
    except (KeyboardInterrupt, SystemExit):
        logger.debug(f"Handling Exit Request")
    finally:
        logger.camply("Exiting camply 👋")


class CommandLineError(Exception):
    """
    Generic CLI Error
    """
    pass


class CamplyCommandLine(object):
    """
    Camply Command Line Interface
    """

    __name__ = "camply"
    __version__ = "0.1.0"

    def __init__(self):
        """
        Initialized CLI
        """

        self.parser = ArgumentParser(description="Camply: Campsite Reservation Cancellation Finder",
                                     prog=self.__name__)
        self.arguments_compiled: bool = False
        self.arguments_parsed: bool = False
        self.cli_arguments: Namespace = None
        self.arguments_validated: bool = False
        self.arguments_executed: bool = False

        self.recreation_areas = None
        self.campgrounds = None
        self.campsites = None

    def __repr__(self) -> str:
        """
        String Representation

        Returns
        -------
        str
        """
        return f"<CamplyCommandLine>"

    def assemble_cli_arguments(self) -> None:
        """
        Gather the Arguments From the CLI

        Returns
        -------
        Namespace
        """
        assert self.arguments_compiled is False

        self.parser.add_argument("--version",
                                 action="version",
                                 version=f"%(prog)s {self.__version__}")
        subparsers = self.parser.add_subparsers(dest="command")

        state_argument = ArgumentParser(add_help=False)
        state_argument.add_argument(
            "--state", action="store", dest="state", required=False,
            help="Useful for Searching commands. Filter by state")

        recreation_area_id_argument = ArgumentParser(add_help=False)
        recreation_area_id_argument.add_argument(
            "--rec-area-id", action="append", dest="recreation_area_id", required=False,
            help="Add Recreation Areas (comprised of campgrounds) by ID")

        campground_argument = ArgumentParser(add_help=False)
        campground_argument.add_argument(
            "--campground", action="append", dest="campground_list", required=False, default=[],
            help="Add individual Campgrounds by ID")

        search_argument = ArgumentParser(add_help=False)
        search_argument.add_argument(
            "--search", action="store", dest="search", required=False,
            help="Search for Campgrounds or Recreation Areas by search string")

        self.recreation_areas = subparsers.add_parser(
            name="recreation-areas",
            help="Search for Recreation Areas and list them.",
            description="Search for Recreation Areas. Recreation Areas are places like National "
                        "Parks and National Forests that can contain one or many campgrounds.",
            parents=[search_argument, state_argument])

        self.campgrounds = subparsers.add_parser(
            name="campgrounds",
            help="Search for Campgrounds (inside of Recreation Areas) and list them",
            parents=[search_argument, state_argument,
                     recreation_area_id_argument, campground_argument])

        self.campsites = subparsers.add_parser(
            name="campsites",
            help="Search for Available Campsites (inside of Campgrounds) using search criteria",
            parents=[recreation_area_id_argument, campground_argument])
        self.campsites.add_argument(
            "--start-date", action="store", dest="start_date", required=False,
            help="Start of Search window, YYYY-MM-DD. "
                 "You will be arriving this day")
        self.campsites.add_argument(
            "--end-date", action="store", dest="end_date", required=False,
            help="Start of Search window, YYYY-MM-DD. "
                 "You will be leaving the following day")
        self.campsites.add_argument(
            "--weekends", action="store_true", dest="weekends", required=False,
            help="Only search for weekend bookings (Fri/Sat)")
        self.campsites.add_argument(
            "--provider", action="store", dest="provider", required=False,
            default="RecreationDotGov",
            help="Camping Search Provider. Options available are 'Yellowstone' and "
                 "'RecreationDotGov'. Defaults to 'RecreationDotGov")
        self.campsites.add_argument(
            "--continuous", action="store_true", dest="continuous", required=False, default=False,
            help="Continuously check, forever, for a campsite to become available.")
        self.campsites.add_argument(
            "--polling-interval", action="store", dest="polling_interval", required=False,
            default=10,
            help="If --continuous is activated, how often to wait in between checks "
                 "(in minutes). Defaults to 10, cannot be less than 5")
        self.campsites.add_argument(
            "--notifications", action="store", dest="notifications", required=False,
            default="silent",
            help="Types of notifications to receive. Options available are 'email', "
                 "'pushover', or 'silent'. Defaults to 'silent' - which just logs "
                 "messages to console")
        self.campsites.add_argument(
            "--notify-first-try", action="store_true",
            dest="notify_first_try", required=False, default=False,
            help="Whether to send a notification if a matching campsite is "
                 "found on the first try. Defaults to false, please try a quick")
        self.arguments_compiled = True

    def parse_arguments(self) -> Namespace:
        """
        Actually Parse the Arguments

        Returns
        -------
        Namespace
        """
        assert self.arguments_compiled is True and self.arguments_parsed is False
        self.cli_arguments = self.parser.parse_args()
        self.arguments_parsed = True
        return self.cli_arguments

    def validate_arguments(self) -> bool:
        """
        Validate the Arguments Provided and Raise an Error if there's a problem

        Returns
        -------
        bool
        """
        assert self.arguments_validated is False
        error_message = None
        if self.cli_arguments.command is None:
            error_message = "You must provide an argument to the Camply CLI"
            help_parser = self.parser
        elif self.cli_arguments.command == "recreation-areas":
            if all([self.cli_arguments.search is None,
                    self.cli_arguments.state is None]):
                error_message = ("You must add a --search or --state parameter to search "
                                 "for Recreation Areas")
                help_parser = self.recreation_areas
        elif self.cli_arguments.command == "campgrounds":
            if all([self.cli_arguments.search is None,
                    self.cli_arguments.state is None,
                    self.cli_arguments.recreation_area_id is None]):
                error_message = ("You must add a --search, --state, or --rec-area-id "
                                 " parameter to search for Campgrounds")
                help_parser = self.campgrounds
        elif self.cli_arguments.command == "campsites":
            if self.cli_arguments.provider == "RecreationDotGov" and all(
                    [self.cli_arguments.recreation_area_id is None,
                     len(self.cli_arguments.campground_list) == 0]):
                error_message = ("To search for Recreation.gov Campsites you must provide "
                                 "either the --rec-area-id or the --campground parameter")
                help_parser = self.campsites
            mandatory_parameters = [self.cli_arguments.start_date,
                                    self.cli_arguments.end_date]
            mandatory_string_parameters = ["--start-date", "--end_date"]
            for field in mandatory_parameters:
                if field is None:
                    error_message = ("Campsite searches require the following mandatory search "
                                     f"parameters: {', '.join(mandatory_string_parameters)}")
                    help_parser = self.campsites

        if error_message is not None:
            help_parser.print_help()
            print("\n")
            logger.error(error_message)
            exit(0)
        self.arguments_validated = True

    def execute_cli_arguments(self) -> Optional[object]:
        """
        Execute the CLI Arguments

        Parameters
        ----------
        self

        Returns
        -------

        """
        assert self.arguments_validated is True
        assert self.arguments_executed is False

        if self.cli_arguments.command == "recreation-areas":
            self.execute_recreation_areas()
        elif self.cli_arguments.command == "campgrounds":
            self.execute_campgrounds()
        elif self.cli_arguments.command == "campsites":
            self.execute_campsites()

    def execute_recreation_areas(self):
        """
        Execute the `recreation-areas` command on the CLI

        Returns
        -------

        """
        camp_finder = RecreationDotGov()
        params = dict()
        if self.cli_arguments.state is not None:
            params.update(dict(state=self.cli_arguments.state))
        camp_finder.find_recreation_areas(search_string=self.cli_arguments.search,
                                          **params)

    def execute_campgrounds(self):
        """
        Execute the `recreation-areas` command on the CLI

        Returns
        -------

        """
        camp_finder = RecreationDotGov()
        params = dict()
        if self.cli_arguments.state is not None:
            params.update(dict(state=self.cli_arguments.state))
        camp_finder.find_campgrounds(search_string=self.cli_arguments.search,
                                     rec_area_id=self.cli_arguments.recreation_area_id,
                                     campground_id=self.cli_arguments.campground_list)

    def execute_campsites(self):
        """
        Execute the `recreation-areas` command on the CLI

        Returns
        -------

        """
        search_window = SearchWindow(
            start_date=datetime.strptime(self.cli_arguments.start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(self.cli_arguments.end_date, "%Y-%m-%d"))
        provider_class = {key.lower(): value for
                          key, value in CAMPSITE_SEARCH_PROVIDER.items()}[
            self.cli_arguments.provider.lower()]
        camping_finder = provider_class(search_window=search_window,
                                        recreation_area=self.cli_arguments.recreation_area_id,
                                        campgrounds=self.cli_arguments.campground_list,
                                        weekends_only=self.cli_arguments.weekends)
        camping_finder.get_matching_campsites(
            log=True, verbose=True,
            continuous=self.cli_arguments.continuous,
            polling_interval=float(self.cli_arguments.polling_interval),
            notify_first_try=self.cli_arguments.notify_first_try,
            notification_provider=self.cli_arguments.notifications)

    def run_cli(self) -> None:
        """
        Full Execution of the CLI

        Returns
        -------
        None
        """
        self.assemble_cli_arguments()
        self.parse_arguments()
        self.validate_arguments()
        self.execute_cli_arguments()


if __name__ == "__main__":
    main()
