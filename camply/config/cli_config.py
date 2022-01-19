#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Command Line Configuration
"""

import logging
from os import getenv

from dotenv import load_dotenv

from camply import __version__ as camply_version
from camply.config.file_config import FileConfig
from camply.config.search_config import SearchConfig

load_dotenv(FileConfig.DOT_CAMPLY_FILE, override=False)


class CommandLineActions:
    """
    ArgParse Actions
    """

    VERSION: str = "version"
    STORE: str = "store"
    STORE_TRUE: str = "store_true"
    APPEND: str = "append"


class CommandLineArguments:
    """
    Argument Config
    """

    VERSION_ARGUMENT: str = "--version"

    STATE_ARGUMENT: str = "--state"
    STATE_DESTINATION: str = "state"
    STATE_HELP: str = "Filter by US state code."

    REC_AREA_ID_ARGUMENT: str = "--rec-area"
    REC_AREA_ID_DESTINATION: str = "recreation_area_id"
    REC_AREA_ID_HELP: str = "Add Recreation Areas (comprised of campgrounds) by ID."

    CAMPGROUND_LIST_ARGUMENT: str = "--campground"
    CAMPGROUND_LIST_DESTINATION: str = "campground_id"
    CAMPGROUND_LIST_HELP: str = "Add individual Campgrounds by ID."

    SEARCH_ARGUMENT: str = "--search"
    SEARCH_DESTINATION: str = "search"
    SEARCH_HELP: str = "Search for Campgrounds or Recreation Areas by search string."

    START_DATE_ARGUMENT: str = "--start-date"
    START_DATE_DESTINATION: str = "start_date"
    START_DATE_HELP: str = "(YYYY-MM-DD) Start of Search window. You will be arriving this day."

    END_DATE_ARGUMENT: str = "--end-date"
    END_DATE_DESTINATION: str = "end_date"
    END_DATE_HELP: str = "(YYYY-MM-DD) End of Search window. You will be checking out this day."

    WEEKENDS_ARGUMENT: str = "--weekends"
    WEEKENDS_DESTINATION: str = "weekends"
    WEEKENDS_HELP: str = "Only search for weekend bookings (Fri/Sat nights)."

    NIGHTS_ARGUMENT: str = "--nights"
    NIGHTS_DESTINATION: str = "nights"
    NIGHTS_DEFAULT: int = 1
    NIGHTS_HELP: str = ("Search for campsite stays with consecutive nights. "
                        "Defaults to 1 which returns all campsites found.")

    PROVIDER_ARGUMENT: str = "--provider"
    PROVIDER_DESTINATION: str = "provider"
    PROVIDER_DEFAULT: str = "RecreationDotGov"
    PROVIDER_HELP: str = ("Camping Search Provider. Options available are 'Yellowstone' and "
                          "'RecreationDotGov'. Defaults to 'RecreationDotGov', not case-sensitive.")

    CONTINUOUS_ARGUMENT: str = "--continuous"
    CONTINUOUS_DESTINATION: str = "continuous"
    CONTINUOUS_HELP: str = ("Continuously check for a campsite to become available, and quit once "
                            "at least one campsite is found.")

    POLLING_INTERVAL_ARGUMENT: str = "--polling-interval"
    POLLING_INTERVAL_DESTINATION: str = "polling_interval"
    POLLING_INTERVAL_DEFAULT: int = SearchConfig.RECOMMENDED_POLLING_INTERVAL
    POLLING_INTERVAL_HELP: str = ("If --continuous is activated, how often to wait in between "
                                  "checks (in minutes). Defaults to 10, cannot be less than 5.")

    NOTIFICATIONS_ARGUMENT: str = "--notifications"
    NOTIFICATIONS_DESTINATION: str = "notifications"
    NOTIFICATIONS_DEFAULT: str = "silent"
    NOTIFICATIONS_HELP: str = ("If --continuous is activated, types of notifications to receive. "
                               "Options available are 'email', "
                               "'pushover', 'pushbullet', or 'silent'. Defaults to 'silent' - "
                               "which just logs messages to console.")

    NOTIFY_FIRST_TRY_ARGUMENT: str = "--notify-first-try"
    NOTIFY_FIRST_TRY_DESTINATION: str = "notify_first_try"
    NOTIFY_FIRST_TRY_HELP: str = ("If --continuous is activated, whether to send all "
                                  "non-silent notifications if more than 5 matching "
                                  "campsites are found on the first try. Defaults to false which "
                                  "only sends the first 5.")

    SEARCH_FOREVER_ARGUMENT: str = "--search-forever"
    SEARCH_FOREVER_DESTINATION: str = "search_forever"
    SEARCH_FOREVER_HELP: str = ("If --continuous is activated, this method continues to search "
                                "after the first availability has been found. The one caveat is "
                                "that it will never notify about the same identical campsite for "
                                "the same booking date.")

    YAML_SEARCH_ARGUMENT: str = "--yml-config"
    YAML_SEARCH_DESTINATION: str = "yml_config"
    YAML_SEARCH_HELP: str = ("Rather than provide arguments to the command line utility, instead "
                             "pass a file path to a YAML configuration file. See the documentation "
                             "for more information on how to structure your configuration file.")


class CommandLineValidation:
    """
    Camply CLI Validation Config
    """

    ERROR_NO_ARGUMENT_FOUND: str = "You must provide an argument to the Camply CLI"
    ERROR_MESSAGE_RECREATION_AREA: str = ("You must add a --search or --state parameter to search "
                                          "for Recreation Areas.")
    ERROR_MESSAGE_CAMPGROUNDS: str = ("You must add a --search, --state, --campground, or "
                                      "--rec-area parameter to search for Campgrounds.")
    ERROR_MESSAGE_REC_DOT_GOV: str = ("To search for Recreation.gov Campsites you must provide "
                                      "either the --rec-area or the --campground parameters.")
    ERROR_MESSAGE_CAMPSITES: str = ("Campsite searches require the following mandatory search "
                                    "parameters.")


class CommandLineConfig(CommandLineActions, CommandLineArguments, CommandLineValidation):
    """
    Command Line String Arguments and Flags
    """

    CAMPLY_APP_NAME: str = "camply"
    CAMPLY_APP_VERSION: str = camply_version
    CAMPLY_DESCRIPTION: str = "camply, the campsite finder"
    CAMPLY_EXIT_MESSAGE: str = "Exiting camply 👋"

    CAMPLY_LONG_DESCRIPTION: str = ("Welcome to camply, the campsite finder. "
                                    "Finding reservations at sold out campgrounds can be "
                                    "tough. That's where camply comes in. It searches the APIs of "
                                    "booking services like https://recreation.gov (which indexes "
                                    "thousands of campgrounds across the USA) to continuously "
                                    "check for cancellations and availabilities to pop up. "
                                    "Once a campsite becomes available, camply sends you a "
                                    "notification to book your spot!")
    CAMPLY_EPILOG: str = "visit the camply documentation at https://github.com/juftin/camply"

    LOG_LEVEL = logging.getLevelName(getenv("LOG_LEVEL", "INFO").upper())

    COMMAND_DESTINATION: str = "command"

    COMMAND_RECREATION_AREA: str = "recreation-areas"
    COMMAND_RECREATION_AREA_HELP: str = "Search for Recreation Areas and list them"
    COMMAND_RECREATION_AREA_DESCRIPTION: str = ("Search for Recreation Areas and their IDs. "
                                                "Recreation Areas are places like National Parks "
                                                "and National Forests that can contain one or many "
                                                "campgrounds.")

    COMMAND_CAMPGROUNDS: str = "campgrounds"
    COMMAND_CAMPGROUNDS_HELP: str = ("Search for Campgrounds (inside of Recreation Areas) "
                                     "and list them")
    COMMAND_CAMPGROUNDS_DESCRIPTION: str = ("Search for Campgrounds and their IDs. "
                                            "Campgrounds are facilities inside of Recreation Areas "
                                            "that contain campsites. Most 'campgrounds' are areas "
                                            "made up of multiple campsites, others are "
                                            "facilities like fire towers or cabins that might only "
                                            "contain a single 'campsite' to book.")

    COMMAND_CAMPSITES: str = "campsites"
    COMMAND_CAMPSITES_HELP: str = "Find available Campsites using search criteria"
    COMMAND_CAMPSITES_DESCRIPTION: str = ("Search for a campsite within camply. Campsites are "
                                          "returned based on the search criteria provided. "
                                          "Campsites contain properties like booking date, site "
                                          "type (tent, RV, cabin, etc), capacity, price, and a "
                                          "link to make the booking. "
                                          "Required parameters include `--start-date`, "
                                          "`--end-date`, `--rec-area` / `--campground`. "
                                          "Constant searching functionality can be enabled with "
                                          " `--continuous` and notifications "
                                          "can be enabled using `--notifications`.")

    COMMAND_CONFIGURE: str = "configure"
    COMMAND_CONFIGURE_HELP: str = "Set up camply configuration file with an interactive console"
    COMMAND_CONFIGURE_DESCRIPTION: str = (
        "In order to send notifications through camply you must set up some authorization "
        "values. Whether you need to set up pushover notifications (push notifications on "
        "your phone, your pushover account can be set up at https://pushover.net) or Email "
        "messages, everything can be done through the configure command. The end result "
        "is a file called .camply in your home folder."
    )
    RECREATION_DOT_GOV: str = "RecreationDotGov"
