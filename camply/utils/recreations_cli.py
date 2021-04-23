#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Redshift Unload Pipeline Script
"""

from argparse import ArgumentParser
from datetime import datetime
import logging

__version__ = 0.01

from camply.search.camping_search import SearchRecreationDotGov
from camply.containers import SearchWindow
from camply.providers import RecreationDotGov

camp_finder = RecreationDotGov()
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)

### ARG PARSER
parser = ArgumentParser(description="Camply - Campsite Finder",
                        prog="camply")
parser.add_argument("--version",
                    action="version",
                    version=f"%(prog)s {__version__}")
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

parser.add_argument("--state",
                    action="store",
                    dest="state",
                    required=False,
                    help="Useful for Searching commands. Filter by state")
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
                    help="Only search for weekend bookings (Fri/Sat)")

# ARGUMENT VALIDATION
cli_arguments = parser.parse_args()

if cli_arguments.availabilities is True and any([cli_arguments.campground_list is not None,
                                                 cli_arguments.rec_area_id is not None]) is False:
    parser.error("--find-availabilities requires (--rec-area-id / --campground) + --start-date + "
                 "--end-date.")

# CODE EXECUTION

# --find-availabilities
if cli_arguments.availabilities is True:
    search_window = SearchWindow(
        start_date=datetime.strptime(cli_arguments.start_date, "%Y-%m-%d"),
        end_date=datetime.strptime(cli_arguments.end_date, "%Y-%m-%d"))
    rec_dot_gov = RecreationDotGov()
    camping_finder = SearchRecreationDotGov(search_window=search_window,
                                            recreation_area=cli_arguments.rec_area_id,
                                            campgrounds=cli_arguments.campground_list,
                                            weekends_only=cli_arguments.weekends)
    matches = camping_finder.search_matching_campsites_available()
    camping_finder._assemble_availabilities(matches, log=True, verbose=True)

else:
    params = dict()
    if cli_arguments.state is not None:
        params.update(dict(state=cli_arguments.state))
    # --find-recreation-areas
    if cli_arguments.recreation_areas is not None:
        camp_finder.find_recreation_areas(search_string=cli_arguments.recreation_areas, **params)
    # --find-campgrounds
    elif cli_arguments.campgrounds is not None:
        camp_finder.find_campsites(search_string=cli_arguments.campgrounds,
                                   rec_area_id=cli_arguments.rec_area_id, **params)
