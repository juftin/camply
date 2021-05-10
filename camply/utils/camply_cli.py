#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Camply CLI
"""

from argparse import ArgumentParser, Namespace
from datetime import datetime
import logging
from typing import Optional

from camply.config import CommandLineConfig
from camply.containers import SearchWindow
from camply.providers import RecreationDotGov
from camply.search import CAMPSITE_SEARCH_PROVIDER
from camply.search.base_search import SearchError
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
                        level=CommandLineConfig.LOG_LEVEL)
    try:
        logger.camply(f"{CommandLineConfig.CAMPLY_DESCRIPTION} ⛺️")
        camply_cli = CamplyCommandLine()
        camply_cli.run_cli()
    except (KeyboardInterrupt, SystemExit):
        logger.debug(f"Handling Exit Request")
    finally:
        logger.camply(CommandLineConfig.CAMPLY_EXIT_MESSAGE)


class CommandLineError(Exception):
    """
    Generic CLI Error
    """
    pass


class CamplyCommandLine(object):
    """
    Camply Command Line Interface
    """

    __name__ = CommandLineConfig.CAMPLY_APP_NAME
    __version__ = CommandLineConfig.CAMPLY_APP_VERSION

    def __init__(self):
        """
        Initialized CLI
        """

        self.parser = ArgumentParser(description=CommandLineConfig.CAMPLY_LONG_DESCRIPTION,
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

        self.parser.add_argument(CommandLineConfig.VERSION_ARGUMENT,
                                 action=CommandLineConfig.VERSION,
                                 version=f"%(prog)s {self.__version__}")
        subparsers = self.parser.add_subparsers(dest=CommandLineConfig.COMMAND_DESTINATION)

        state_argument = ArgumentParser(add_help=False)
        state_argument.add_argument(CommandLineConfig.STATE_ARGUMENT,
                                    action=CommandLineConfig.STORE,
                                    dest=CommandLineConfig.STATE_DESTINATION,
                                    required=False,
                                    help=CommandLineConfig.STATE_HELP)

        recreation_area_id_argument = ArgumentParser(add_help=False)
        recreation_area_id_argument.add_argument(CommandLineConfig.REC_AREA_ID_ARGUMENT,
                                                 action=CommandLineConfig.APPEND,
                                                 dest=CommandLineConfig.REC_AREA_ID_DESTINATION,
                                                 required=False,
                                                 help=CommandLineConfig.REC_AREA_ID_HELP)

        campground_argument = ArgumentParser(add_help=False)
        campground_argument.add_argument(CommandLineConfig.CAMPGROUND_LIST_ARGUMENT,
                                         action=CommandLineConfig.APPEND,
                                         dest=CommandLineConfig.CAMPGROUND_LIST_DESTINATION,
                                         required=False,
                                         default=list(),
                                         help=CommandLineConfig.CAMPGROUND_LIST_HELP)

        search_argument = ArgumentParser(add_help=False)
        search_argument.add_argument(CommandLineConfig.SEARCH_ARGUMENT,
                                     action=CommandLineConfig.STORE,
                                     dest=CommandLineConfig.SEARCH_DESTINATION,
                                     required=False,
                                     help=CommandLineConfig.SEARCH_HELP)

        self.recreation_areas = subparsers.add_parser(
            name=CommandLineConfig.COMMAND_RECREATION_AREA,
            help=CommandLineConfig.COMMAND_RECREATION_AREA_HELP,
            description=CommandLineConfig.COMMAND_RECREATION_AREA_DESCRIPTION,
            parents=[search_argument, state_argument])

        self.campgrounds = subparsers.add_parser(
            name=CommandLineConfig.COMMAND_CAMPGROUNDS,
            help=CommandLineConfig.COMMAND_CAMPGROUNDS_HELP,
            description=CommandLineConfig.COMMAND_CAMPGROUNDS_DESCRIPTION,
            parents=[search_argument, state_argument,
                     recreation_area_id_argument, campground_argument])

        self.campsites = subparsers.add_parser(
            name=CommandLineConfig.COMMAND_CAMPSITES,
            help=CommandLineConfig.COMMAND_CAMPSITES_HELP,
            description=CommandLineConfig.COMMAND_CAMPSITES_DESCRIPTION,
            parents=[recreation_area_id_argument, campground_argument])

        self.campsites.add_argument(CommandLineConfig.START_DATE_ARGUMENT,
                                    action=CommandLineConfig.STORE,
                                    dest=CommandLineConfig.START_DATE_DESTINATION,
                                    required=False,
                                    help=CommandLineConfig.START_DATE_HELP)
        self.campsites.add_argument(CommandLineConfig.END_DATE_ARGUMENT,
                                    action=CommandLineConfig.STORE,
                                    dest=CommandLineConfig.END_DATE_DESTINATION,
                                    required=False,
                                    help=CommandLineConfig.END_DATE_HELP)
        self.campsites.add_argument(CommandLineConfig.WEEKENDS_ARGUMENT,
                                    action=CommandLineConfig.STORE_TRUE,
                                    dest=CommandLineConfig.WEEKENDS_DESTINATION,
                                    default=False,
                                    required=False,
                                    help=CommandLineConfig.WEEKENDS_HELP)
        self.campsites.add_argument(CommandLineConfig.PROVIDER_ARGUMENT,
                                    action=CommandLineConfig.STORE,
                                    dest=CommandLineConfig.PROVIDER_DESTINATION,
                                    default=CommandLineConfig.PROVIDER_DEFAULT,
                                    required=False,
                                    help=CommandLineConfig.PROVIDER_HELP)
        self.campsites.add_argument(CommandLineConfig.CONTINUOUS_ARGUMENT,
                                    action=CommandLineConfig.STORE_TRUE,
                                    dest=CommandLineConfig.CONTINUOUS_DESTINATION,
                                    default=False,
                                    required=False,
                                    help=CommandLineConfig.CONTINUOUS_HELP)
        self.campsites.add_argument(CommandLineConfig.POLLING_INTERVAL_ARGUMENT,
                                    action=CommandLineConfig.STORE,
                                    dest=CommandLineConfig.POLLING_INTERVAL_DESTINATION,
                                    default=CommandLineConfig.POLLING_INTERVAL_DEFAULT,
                                    required=False,
                                    help=CommandLineConfig.POLLING_INTERVAL_HELP)
        self.campsites.add_argument(CommandLineConfig.NOTIFICATIONS_ARGUMENT,
                                    action=CommandLineConfig.STORE,
                                    dest=CommandLineConfig.NOTIFICATIONS_DESTINATION,
                                    required=False,
                                    default=CommandLineConfig.NOTIFICATIONS_DEFAULT,
                                    help=CommandLineConfig.NOTIFICATIONS_HELP)
        self.campsites.add_argument(CommandLineConfig.NOTIFY_FIRST_TRY_ARGUMENT,
                                    action=CommandLineConfig.STORE_TRUE,
                                    dest=CommandLineConfig.NOTIFY_FIRST_TRY_DESTINATION,
                                    required=False,
                                    default=False,
                                    help=CommandLineConfig.NOTIFY_FIRST_TRY_HELP)
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
            error_message = CommandLineConfig.ERROR_NO_ARGUMENT_FOUND
            help_parser = self.parser
        elif self.cli_arguments.command == CommandLineConfig.COMMAND_RECREATION_AREA:
            if all([self.cli_arguments.search is None,
                    self.cli_arguments.state is None]):
                error_message = CommandLineConfig.ERROR_MESSAGE_RECREATION_AREA
                help_parser = self.recreation_areas
        elif self.cli_arguments.command == CommandLineConfig.COMMAND_CAMPGROUNDS:
            if all([self.cli_arguments.search is None,
                    self.cli_arguments.state is None,
                    self.cli_arguments.recreation_area_id is None]):
                error_message = CommandLineConfig.ERROR_MESSAGE_CAMPGROUNDS
                help_parser = self.campgrounds
        elif self.cli_arguments.command == CommandLineConfig.COMMAND_CAMPSITES:
            if self.cli_arguments.provider == CommandLineConfig.RECREATION_DOT_GOV and all(
                    [self.cli_arguments.recreation_area_id is None,
                     len(self.cli_arguments.campground_list) == 0]):
                error_message = CommandLineConfig.ERROR_MESSAGE_REC_DOT_GOV
                help_parser = self.campsites
            mandatory_parameters = [self.cli_arguments.start_date,
                                    self.cli_arguments.end_date]
            mandatory_string_parameters = [CommandLineConfig.START_DATE_ARGUMENT,
                                           CommandLineConfig.END_DATE_ARGUMENT]
            for field in mandatory_parameters:
                if field is None:
                    error_message = (f"{CommandLineConfig.ERROR_MESSAGE_CAMPSITES}: "
                                     f"{', '.join(mandatory_string_parameters)}")
                    help_parser = self.campsites

        if error_message is not None:
            help_parser.print_help()
            print("\n")
            logger.error(error_message)
            exit(1)
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

        if self.cli_arguments.command == CommandLineConfig.COMMAND_RECREATION_AREA:
            self.execute_recreation_areas()
        elif self.cli_arguments.command == CommandLineConfig.COMMAND_CAMPGROUNDS:
            self.execute_campgrounds()
        elif self.cli_arguments.command == CommandLineConfig.COMMAND_CAMPSITES:
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
                                     campground_id=self.cli_arguments.campground_list,
                                     **params)

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
        try:
            camping_finder.get_matching_campsites(
                log=True, verbose=True,
                continuous=self.cli_arguments.continuous,
                polling_interval=float(self.cli_arguments.polling_interval),
                notify_first_try=self.cli_arguments.notify_first_try,
                notification_provider=self.cli_arguments.notifications)
        except SearchError:
            exit(1)

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
