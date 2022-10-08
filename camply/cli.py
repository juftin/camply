"""
Camply Command Line Interface
"""

import logging
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple, Union

import click
from rich import traceback

from camply import __application__, __version__
from camply.config import SearchConfig
from camply.config.logging_config import set_up_logging
from camply.containers import SearchWindow
from camply.providers import RecreationDotGov
from camply.search import CAMPSITE_SEARCH_PROVIDER, SearchYellowstone
from camply.utils import configure_camply, log_camply, make_list, yaml_utils

logging.Logger.camply = log_camply
logger = logging.getLogger(__name__)

DEFAULT_CAMPLY_PROVIDER: str = "RecreationDotGov"


@dataclass
class CamplyContext:
    """
    Context Object Passed Around Application
    """

    debug: Optional[bool] = None
    provider: Optional[str] = None


provider_argument = click.option(
    "--provider",
    show_default=False,
    default=None,
    help="Camping Search Provider. Options available are 'Yellowstone' and "
    "'RecreationDotGov'. Defaults to 'RecreationDotGov', not case-sensitive.",
)
debug_option = click.option(
    "--debug/--no-debug", default=None, help="Enable extra debugging output"
)


def _set_up_debug(debug: Optional[bool] = None) -> None:
    """
    Set up the Camply Debugging Mode
    """
    if debug is None:
        debug = False
    if debug is True:
        set_up_logging(log_level=logging.DEBUG)
        logger.debug("Setting up camply debugging")
        logger.debug("Camply Version: %s", __version__)
        logger.debug("Python Version: %s", sys.version.split(" ")[0])
        logger.debug("Platform: %s", sys.platform)
    traceback.install(show_locals=debug)


@click.group()
@click.version_option(version=__version__, prog_name=__application__)
@provider_argument
@debug_option
@click.pass_context
def camply_command_line(ctx: click.core.Context, provider: str, debug: bool) -> None:
    """
    Welcome to camply, the campsite finder.

    Finding reservations at sold out campgrounds can be
    tough. That's where camply comes in. It searches the APIs of booking services like
    https://recreation.gov (which indexes thousands of campgrounds across the USA) to continuously
    check for cancellations and availabilities to pop up. Once a campsite becomes available,
    camply sends you a notification to book your spot!

    visit the camply documentation at https://github.com/juftin/camply
    """
    set_up_logging(log_level=None if debug is False else logging.INFO)
    logger.camply("camply, the campsite finder ⛺️")  # noqa
    ctx.obj = CamplyContext(debug=debug, provider=provider)
    _set_up_debug(debug=debug)


@camply_command_line.command()
@debug_option
@click.pass_obj
def configure(context: CamplyContext, debug: bool) -> None:
    """
    Set up camply configuration file with an interactive console

    In order to send notifications through camply you must set up some authorization values.
    Whether you need to set up pushover notifications (push notifications on your phone,
    your pushover account can be set up at https://pushover.net) or Email messages, everything
    can be done through the configure command. The end result is a file called .camply in your
    home folder.
    """
    if context.debug is None:
        context.debug = debug
        _set_up_debug(debug=context.debug)
    configure_camply.generate_dot_camply_file()


# Shared Arguments
search_argument = click.option(
    "--search",
    default=None,
    help="Search for Campgrounds or Recreation Areas by search string.",
)
state_argument = click.option("--state", default=None, help="Filter by US state code.")
campsite_id_argument = click.option(
    "--campsite", default=None, multiple=True, help="Add individual Campsites by ID."
)
rec_area_argument = click.option(
    "--rec-area",
    default=None,
    multiple=True,
    help="Add Recreation Areas (comprised of campgrounds) by ID.",
)
campground_argument = click.option(
    "--campground",
    default=None,
    multiple=True,
    help="Add individual Campgrounds by ID.",
)


@camply_command_line.command()
@search_argument
@state_argument
@debug_option
@click.pass_obj
def recreation_areas(
    context: CamplyContext, search: Optional[str], state: Optional[str], debug: bool
) -> None:
    """
    Search for Recreation Areas and list them

    Search for Recreation Areas and their IDs. Recreation Areas are places like
    National Parks and National Forests that can contain one or many campgrounds.
    """
    if context.debug is None:
        context.debug = debug
        _set_up_debug(debug=context.debug)
    if all([search is None, state is None]):
        logger.error(
            "You must add a --search or --state parameter to search "
            "for Recreation Areas."
        )
        exit(1)
    camp_finder = RecreationDotGov()
    params = dict()
    if state is not None:
        params.update(dict(state=state))
    camp_finder.find_recreation_areas(search_string=search, **params)


@camply_command_line.command()
@search_argument
@state_argument
@rec_area_argument
@campground_argument
@campsite_id_argument
@provider_argument
@debug_option
@click.pass_obj
def campgrounds(
    context: CamplyContext,
    debug: bool,
    search: Optional[str] = None,
    state: Optional[str] = None,
    rec_area: Optional[int] = None,
    campground: Optional[int] = None,
    campsite: Optional[int] = None,
    provider: Optional[str] = "RecreationDotGov",
) -> None:
    """
    Search for Campgrounds (inside of Recreation Areas) and list them

    Search for Campgrounds and their IDs. Campgrounds are facilities inside of
    Recreation Areas that contain campsites. Most 'campgrounds' are areas made up of
    multiple campsites, others are facilities like fire towers or cabins that might only
    contain a single 'campsite' to book.
    """
    if context.debug is None:
        context.debug = debug
        _set_up_debug(debug=context.debug)
    if context.provider is None:
        context.provider = provider
    provider = DEFAULT_CAMPLY_PROVIDER if context.provider is None else context.provider
    if provider.lower() == "yellowstone":
        SearchYellowstone.print_campgrounds()
        exit(0)
    if all(
        [
            search is None,
            state is None,
            len(rec_area) == 0,
            len(campground) == 0,
            len(campsite) == 0,
        ]
    ):
        logger.error(
            "You must add a --search, --state, --campground, --campsite, "
            "or --rec-area parameter to search for Campgrounds."
        )
        exit(1)
    camp_finder = RecreationDotGov()
    params = dict()
    if state is not None:
        params.update(dict(state=state))
    camp_finder.find_campgrounds(
        search_string=search,
        rec_area_id=make_list(rec_area, coerce=int),
        campground_id=make_list(campground, coerce=int),
        campsite_id=make_list(campsite, coerce=int),
        **params,
    )


# `campsite` arguments
start_date_argument = click.option(
    "--start-date",
    default=None,
    help="(YYYY-MM-DD) Start of Search window. You will be arriving this day.",
)
end_date_argument = click.option(
    "--end-date",
    default=None,
    help="(YYYY-MM-DD) End of Search window. You will be checking out this day.",
)
weekends_argument = click.option(
    "--weekends",
    is_flag=True,
    show_default=True,
    default=False,
    help="Only search for weekend bookings (Fri/Sat nights).",
)
nights_argument = click.option(
    "--nights",
    show_default=True,
    default=1,
    help="Search for campsite stays with consecutive nights. "
    "Defaults to 1 which returns all campsites found.",
)
continuous_argument = click.option(
    "--continuous",
    is_flag=True,
    show_default=True,
    default=False,
    help="Continuously check for a campsite to become available, and quit once "
    "at least one campsite is found.",
)
polling_interval_argument = click.option(
    "--polling-interval",
    show_default=True,
    default=SearchConfig.RECOMMENDED_POLLING_INTERVAL,
    help="If --continuous is activated, how often to wait in between "
    "checks (in minutes). Defaults to 10, cannot be less than 5.",
)
notifications_argument = click.option(
    "--notifications",
    multiple=True,
    show_default=True,
    default=["silent"],
    help="If --continuous is activated, types of notifications to receive. "
    "Options available are 'email', 'pushover', "
    "'pushbullet', 'telegram', 'twilio', or 'silent'. Defaults to 'silent' - "
    "which just logs messages to console.",
)
notify_first_try_argument = click.option(
    "--notify-first-try",
    is_flag=True,
    show_default=True,
    default=False,
    help="If --continuous is activated, whether to send all "
    "non-silent notifications if more than 5 matching "
    "campsites are found on the first try. Defaults to false which "
    "only sends the first 5.",
)
search_forever_argument = click.option(
    "--search-forever",
    is_flag=True,
    show_default=True,
    default=False,
    help="If --continuous is activated, this method continues to search "
    "after the first availability has been found. The one caveat is "
    "that it will never notify about the same identical campsite for "
    "the same booking date.",
)
yaml_config_argument = click.option(
    "--yaml-config",
    "--yml-config",
    default=None,
    help="Rather than provide arguments to the command line utility, instead "
    "pass a file path to a YAML configuration file. See the documentation "
    "for more information on how to structure your configuration file.",
)
equipment_argument = click.option(
    "--equipment",
    default=None,
    nargs=2,
    multiple=True,
    help="Search for campsites compatible with your camping equipment. "
    "This argument accepts two options, the equipment name and its length "
    "If you don't want to filter based on length provide a length of 0. Accepted "
    "equipment names include `Tent`, `RV`. `Trailer`, `Vehicle` and are "
    "not case-sensitive.",
)
offline_search_argument = click.option(
    "--offline-search",
    is_flag=True,
    show_default=True,
    default=False,
    help="When set to True, the campsite search will both save the results of the "
    "campsites it's found, but also load those campsites before beginning a "
    "search for other campsites.",
)
offline_search_path_argument = click.option(
    "--offline-search-path",
    show_default=True,
    default=None,
    help="When offline search is set to True, this is the name of the file to be saved/loaded. "
    "Campsites can be saved as a serialized pickle file or "
    "a JSON file, depending on the file extension. When not specified, "
    "the filename will default to `camply_campsites.json`",
)


def _get_equipment(equipment: Optional[List[str]]) -> List[Tuple[str, Optional[int]]]:
    """
    Parse Equipment from CLI Args
    """
    equipment_list = []
    for (equipment_name, equipment_length) in equipment:
        try:
            equipment_length = round(float(equipment_length), 0)
            if equipment_length == 0:
                equipment_length = None
        except ValueError:
            equipment_length = None
        equipment_list.append((equipment_name, equipment_length))
    return equipment_list


def _validate_campsites(
    rec_area: Optional[int],
    campground: Optional[int],
    campsite: Optional[int],
    start_date: Optional[str],
    end_date: Optional[str],
    provider: str,
    yaml_config: Optional[str],
    **kwargs,
) -> None:
    """
    Validate the campsites portion of the CLI
    """
    if provider.lower() == "recreationdotgov" and all(
        [
            len(rec_area) == 0,
            len(campground) == 0,
            len(campsite) == 0,
            yaml_config is None,
        ]
    ):
        logger.error(
            "To search for Recreation.gov Campsites you must provide "
            "either the --rec-area, --campground, or --campsite "
            "parameters."
        )
        exit(1)

    if not kwargs.get("notifications") == ["silent"] and not kwargs.get("continuous"):
        logger.error(
            "To receive notifications about campsites you must search "
            "continuously by passing the --continuous option."
        )
        exit(1)

    mandatory_parameters = [start_date, end_date]
    mandatory_string_parameters = ["--start-date", "--end-date"]
    for field in mandatory_parameters:
        if field is None and yaml_config is None:
            logger.error(
                "Campsite searches require the following mandatory search parameters: "
                f"{', '.join(mandatory_string_parameters)}"
            )
            exit(1)


@camply_command_line.command()
@yaml_config_argument
@offline_search_path_argument
@offline_search_argument
@search_forever_argument
@notify_first_try_argument
@notifications_argument
@polling_interval_argument
@continuous_argument
@provider_argument
@equipment_argument
@nights_argument
@weekends_argument
@end_date_argument
@start_date_argument
@campsite_id_argument
@campground_argument
@rec_area_argument
@debug_option
@click.pass_obj
def campsites(
    context: CamplyContext,
    debug: bool,
    rec_area: Optional[int] = None,
    campground: Optional[int] = None,
    campsite: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    weekends: bool = False,
    nights: int = 1,
    provider: str = "RecreationDotGov",
    continuous: bool = False,
    polling_interval: int = SearchConfig.RECOMMENDED_POLLING_INTERVAL,
    notifications: Union[str, List[str]] = "silent",
    notify_first_try: bool = False,
    search_forever: bool = False,
    yaml_config: Optional[str] = None,
    equipment: Optional[List[str]] = None,
    offline_search: bool = False,
    offline_search_path: Optional[str] = None,
) -> None:
    """
    Find available Campsites using search criteria

    Search for a campsite within camply. Campsites are returned based on the search criteria
    provided. Campsites contain properties like booking date, site type (tent, RV, cabin, etc),
    capacity, price, and a link to make the booking. Required parameters include
    `--start-date`, `--end-date`, `--rec-area` / `--campground`. Constant searching
    functionality can be enabled with  `--continuous` and notifications can be enabled using
    `--notifications`.
    """
    if context.debug is None:
        context.debug = debug
        _set_up_debug(debug=context.debug)
    if context.provider is None:
        context.provider = provider
    provider = DEFAULT_CAMPLY_PROVIDER if context.provider is None else context.provider
    notifications = make_list(notifications)
    _validate_campsites(
        rec_area=rec_area,
        campground=campground,
        campsite=campsite,
        start_date=start_date,
        end_date=end_date,
        weekends=weekends,
        nights=nights,
        provider=provider,
        continuous=continuous,
        polling_interval=polling_interval,
        notifications=notifications,
        notify_first_try=notify_first_try,
        search_forever=search_forever,
        yaml_config=yaml_config,
    )
    if yaml_config is not None:
        provider, provider_kwargs, search_kwargs = yaml_utils.yaml_file_to_arguments(
            file_path=yaml_config
        )
    else:
        provider = provider.lower()
        search_window = SearchWindow(
            start_date=datetime.strptime(start_date, "%Y-%m-%d"),
            end_date=datetime.strptime(end_date, "%Y-%m-%d"),
        )
        provider_kwargs = dict(
            search_window=search_window,
            recreation_area=make_list(rec_area),
            campgrounds=make_list(campground),
            campsites=make_list(campsite),
            weekends_only=weekends,
            nights=int(nights),
            equipment=make_list(equipment),
            offline_search=offline_search,
            offline_search_path=offline_search_path,
        )
        search_kwargs = dict(
            log=True,
            verbose=True,
            continuous=continuous,
            polling_interval=float(polling_interval),
            notify_first_try=notify_first_try,
            notification_provider=notifications,
            search_forever=search_forever,
        )
    provider_class = {
        key.lower(): value for key, value in CAMPSITE_SEARCH_PROVIDER.items()
    }[provider.lower()]
    camping_finder = provider_class(**provider_kwargs)
    camping_finder.get_matching_campsites(**search_kwargs)


def cli():
    """
    Camply Command Line Utility Wrapper
    """
    try:
        camply_command_line()
    except KeyboardInterrupt:
        logger.debug("Handling Exit Request")
    finally:
        logger.camply("Exiting camply 👋")  # noqa


if __name__ == "__main__":
    cli()
