#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Redshift Unload Pipeline Script
"""

from argparse import ArgumentParser, Namespace
import logging

__version__ = 0.01

from camply.providers import RecreationDotGov

camp_finder = RecreationDotGov()
logger = logging.getLogger(__name__)


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Campsite Availability Finder",
                            prog="camping-finder")
    exclusive_commands = parser.add_mutually_exclusive_group()

    # CLI VERSION
    parser.add_argument("--version",
                        action="version",
                        version=f"%(prog)s {__version__}")

    exclusive_commands.add_argument("--find-recreation-areas",
                                    action="store",
                                    dest="recreation_areas",
                                    nargs="?",
                                    const="",
                                    default=None,
                                    required=False,
                                    help="Search for Recreation Areas and list them.")

    exclusive_commands.add_argument("--find-campgrounds",
                                    action="store",
                                    dest="campgrounds",
                                    nargs="?",
                                    const="",
                                    default=None,
                                    required=False,
                                    help="Search for Campgrounds by String areas and return a "
                                         "list of Recreation Facilities.")

    parser.add_argument("--state",
                        action="store",
                        dest="state",
                        required=False,
                        help="Useful for Searching commands. Filter by state")
    parser.add_argument("--rec-area-id",
                        action="store",
                        dest="rec_area_id",
                        required=False,
                        help="Used to search for campgrounds by ID")

    cli_arguments = parser.parse_args()
    try:
        validate_arguments(cli_arguments=cli_arguments)
    except AssertionError:
        parser.print_help()
        print("\n\n\n")
        raise RuntimeError("You must provide arguments to the CLI")
    return cli_arguments


def validate_arguments(cli_arguments: Namespace) -> None:
    """
    Validate proper CLI Params Entered

    Parameters
    ----------
    cli_arguments

    Returns
    -------

    """
    distinct_values = set(vars(cli_arguments).values())
    assert distinct_values != {None}


def run_cli(cli_arguments: Namespace) -> None:
    """
    Run the pipeline if this file is called directly - use arguments
    """
    params = dict()
    if cli_arguments.state is not None:
        params = dict(state=cli_arguments.state)
    validate_arguments(cli_arguments=cli_arguments)
    # --find-recreation-areas
    if cli_arguments.recreation_areas is not None:
        camp_finder.find_recreation_areas(search_string=cli_arguments.recreation_areas, **params)
    # --find-campgrounds
    elif cli_arguments.campgrounds is not None:
        camp_finder.find_campsites(search_string=cli_arguments.campgrounds,
                                   rec_area_id=cli_arguments.rec_area_id, **params)


if __name__ == "__main__":
    # SET UP LOGGING
    logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                        level=logging.INFO)
    # GET THE DIRECTORY NAME FROM ARGUMENT PARSER
    activated_cli_arguments = parse_arguments()
    # RUN THE PIPELINE
    run_cli(cli_arguments=activated_cli_arguments)
