#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Redshift Unload Pipeline Script
"""

from argparse import ArgumentParser, Namespace
from datetime import datetime
import logging

from camply.containers import SearchWindow
from camply.providers import RecreationDotGov
from camply.search import CAMPSITE_SEARCH_PROVIDER

logger = logging.getLogger(__name__)

__version__ = "0.1.0"


def gather_cli_arguments() -> Namespace:
    """
    Gather the Arguments From the CLI

    Returns
    -------
    Namespace
    """
    # ARG PARSER
    parser = ArgumentParser(description="Camply: Campsite Reservation Cancellation Finder",
                            prog="camply")
    primary_exclusives = parser.add_mutually_exclusive_group()

    primary_exclusives.add_argument("--find-recreation-areas",
                                    action="store",
                                    dest="recreation_areas",
                                    nargs="?",
                                    const="",
                                    default=None,
                                    required=False,
                                    help="Search for Recreation Areas and list them.")

    primary_exclusives.add_argument("--find-campgrounds",
                                    action="store",
                                    dest="campgrounds",
                                    nargs="?",
                                    const="",
                                    default=None,
                                    required=False,
                                    help="Search for Campgrounds by String areas and return a "
                                         "list of Recreation Facilities.")
    primary_exclusives.add_argument("--find-availabilities",
                                    action="store_true",
                                    dest="availabilities",
                                    required=False,
                                    help="Search for Campsites. Requires --start-date and "
                                         "--end-date flags as well as --campground or "
                                         "--rec-area-id")
    parser.add_argument("--start-date",
                        action="store",
                        dest="start_date",
                        required=False,
                        help="Start of Search window, YYYY-MM-DD. "
                             "You will be arriving this day")
    parser.add_argument("--end-date",
                        action="store",
                        dest="end_date",
                        required=False,
                        help="Start of Search window, YYYY-MM-DD. "
                             "You will be leaving the following day")
    parser.add_argument("--weekends",
                        action="store_true",
                        dest="weekends",
                        required=False,
                        help="Only search for weekend bookings (Fri/Sat)"
                             "\n")
    parser.add_argument("--continuous",
                        action="store_true",
                        dest="continuous",
                        required=False,
                        default=False,
                        help="Continuously check, forever, for a campsite to become available.")
    parser.add_argument("--polling-interval",
                        action="store",
                        dest="polling_interval",
                        required=False,
                        default=10,
                        help="If --continuous is activated, how often to wait in between checks "
                             "(in minutes). Defaults to 10, cannot be less than 5")
    parser.add_argument("--notifications",
                        action="store",
                        dest="notifications",
                        required=False,
                        default="silent",
                        help="Types of notifications to receive. Options available are 'email', "
                             "'pushover', or 'silent'. Defaults to 'silent' - which just logs "
                             "messages to console")
    parser.add_argument("--notify-first-try",
                        action="store_true",
                        dest="notify_first_try",
                        required=False,
                        default=False,
                        help="Whether to send a notification if a matching campsite is "
                             "found on the first try. Defaults to false, please try a quick")
    parser.add_argument("--rec-area-id",
                        action="append",
                        dest="rec_area_id",
                        required=False,
                        help="Add Recreation Areas (comprised of campgrounds) by ID")
    parser.add_argument("--campground",
                        action="append",
                        dest="campground_list",
                        required=False,
                        help="Add individual Campgrounds by ID")
    parser.add_argument("--provider",
                        action="store",
                        dest="provider",
                        required=False,
                        default="RecreationDotGov",
                        help="Camping Search Provider. Options available are 'Yellowstone' and "
                             "'RecreationDotGov'. Defaults to 'RecreationDotGov")
    parser.add_argument("--state",
                        action="store",
                        dest="state",
                        required=False,
                        help="Useful for Searching commands. Filter by state")
    parser.add_argument("--version",
                        action="version",
                        version=f"%(prog)s {__version__}")

    # ARGUMENT VALIDATION
    cli_arguments = parser.parse_args()
    if cli_arguments.availabilities is True and any([cli_arguments.campground_list is not None,
                                                     cli_arguments.rec_area_id is not None,
                                                     cli_arguments.provider != "RecreationDotGov"
                                                     ]) is False:
        parser.error("--find-availabilities requires "
                     "(--rec-area-id / --campground) + --start-date + "
                     "--end-date.")
    if all([cli_arguments.recreation_areas is None,
            cli_arguments.campgrounds is None,
            cli_arguments.availabilities is False]):
        parser.print_help()
    return cli_arguments


def process_cli_arguments(cli_arguments: Namespace):
    """
    Execute the Camply CLI

    Returns
    -------

    """

    # --find-availabilities
    if cli_arguments.availabilities is True:
        search_window = SearchWindow(
            start_date=datetime.strptime(cli_arguments.start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(cli_arguments.end_date, "%Y-%m-%d"))
        provider_class = {key.lower(): value for
                          key, value in CAMPSITE_SEARCH_PROVIDER.items()}[
            cli_arguments.provider.lower()]
        camping_finder = provider_class(search_window=search_window,
                                        recreation_area=cli_arguments.rec_area_id,
                                        campgrounds=cli_arguments.campground_list,
                                        weekends_only=cli_arguments.weekends)
        camping_finder.get_matching_campsites(
            log=True, verbose=True,
            continuous=cli_arguments.continuous,
            polling_interval=float(cli_arguments.polling_interval),
            notify_first_try=cli_arguments.notify_first_try,
            notification_provider=cli_arguments.notifications)
    else:
        camp_finder = RecreationDotGov()
        params = dict()
        if cli_arguments.state is not None:
            params.update(dict(state=cli_arguments.state))
        # --find-recreation-areas
        if cli_arguments.recreation_areas is not None:
            camp_finder.find_recreation_areas(search_string=cli_arguments.recreation_areas,
                                              **params)
        # --find-campgrounds
        elif cli_arguments.campgrounds is not None:
            camp_finder.find_campsites(search_string=cli_arguments.campgrounds,
                                       rec_area_id=cli_arguments.rec_area_id,
                                       campground_id=None, **params)


def main() -> None:
    """
    Full Execution of the CLI

    Returns
    -------
    None
    """
    logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                        level=logging.INFO)
    cli_arguments = gather_cli_arguments()
    exit_messsage = "Exiting camply, bye 👋"
    try:
        process_cli_arguments(cli_arguments=cli_arguments)
    except (KeyboardInterrupt, SystemExit):
        logger.debug("Exit Signal detected, exiting.")
    finally:
        logger.info(exit_messsage)
        exit()


if __name__ == "__main__":
    main()
