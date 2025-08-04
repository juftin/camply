"""
CLI Testing: `camply campgrounds ...`
"""

import logging

from camply import __version__
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette

logger = logging.getLogger(__name__)


@vcr_cassette
def test_list_recdotgov_campgrounds(cli_runner: CamplyRunner) -> None:
    """
    Test the Campground Search for a Fire Tower
    """
    test_command = """
    camply \
        campgrounds \
        --provider RecreationDotGov \
        --search "Fire Tower" \
        --state CA
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Furnace Creek Campground" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_campground_search_by_recarea_id(cli_runner: CamplyRunner) -> None:
    """
    Search for Campgrounds by RecArea ID
    """
    test_command = """
    camply \
        campgrounds \
        --rec-area 2991
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Bridalveil Creek Campground" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_campground_search_by_campsite_id(cli_runner: CamplyRunner) -> None:
    """
    Search for Campgrounds by Campsite ID
    """
    test_command = """
    camply \
        campgrounds \
        --campsite 40107
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Ledgefork" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_campground_search_yellowstone(cli_runner: CamplyRunner) -> None:
    """
    Search for Campgrounds Yellowstone Provider
    """
    test_command = """
    camply \
        --debug \
        campgrounds \
        --provider Yellowstone
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert __version__ in result.output
    cli_status_checker(result=result)
    assert "Madison Campground" in result.output
    cli_status_checker(result=result)
