"""
CLI Testing - GoingToCamp - Campsites: `camply campsites ... --provider GoingToCamp`
"""

import logging

from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette

logger = logging.getLogger(__name__)


@vcr_cassette
def test_goingtocamp_list_recareas(cli_runner: CamplyRunner) -> None:
    """
    Testing GoingToCamp - List All RecAreas
    """
    test_command = """
    camply \
      --provider GoingToCamp \
      recreation-areas
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Long Point Region" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_goingtocamp_equipment_types(cli_runner: CamplyRunner) -> None:
    """
    Testing GoingToCamp - List Equipment Types
    """
    test_command = """
    camply \
      equipment-types \
      --rec-area 1 \
      --provider goingtocamp
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Trailer up to 25ft" in result.output
    assert "Trailer up to 40ft" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_goingtocamp_search_by_equipment_types(cli_runner: CamplyRunner) -> None:
    """
    Testing GoingToCamp - Search By Equipment Types
    """
    test_command = """
    camply \
      campsites \
      --provider goingtocamp \
      --rec-area 1 \
      --start-date 2023-09-01 \
      --end-date 2023-09-02 \
      --equipment-id -32768 \
      --campground -2147483643
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Long Point Region" in result.output
    assert "Waterford North Conservation Area" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_goingtocamp_search_nova_scotia(cli_runner: CamplyRunner) -> None:
    """
    Testing GoingToCamp - Nova Scotia
    """
    test_command = """
    camply campsites \
        --campground -2147483629 \
        --start-date 2023-07-01 \
        --end-date 2023-07-14 \
        --provider GoingToCamp \
        --rec-area 13
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Whycocomagh Provincial Park" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_goingtocamp_search_nova_scotia_yaml(cli_runner: CamplyRunner) -> None:
    """
    Testing GoingToCamp - Nova Scotia - YAML
    """
    test_command = """
    camply campsites \
        --yaml-config tests/yaml/goingtocamp.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Boylston Provincial Park" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_goingtocamp_search_parks_canada_campgrounds(cli_runner: CamplyRunner) -> None:
    """
    Testing GoingToCamp - Parks Canada Campgrounds
    """
    test_command = """
    camply campgrounds --provider GoingToCamp --rec-area 14 --search "Two Jack"
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Banff" in result.output
    assert "Two Jack Lakeside" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_goingtocamp_search_parks_canada_campsites(cli_runner: CamplyRunner) -> None:
    """
    Testing GoingToCamp - Parks Canada Campsites
    """
    test_command = """
    camply campsites \
        --provider GoingToCamp \
        --rec-area 14 \
        --start-date 2023-07-01 \
        --end-date 2023-07-14 \
        --campground -2147483643
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Banff" in result.output
    assert "Two Jack Lakeside" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_goingtocamp_search_manitoba(cli_runner: CamplyRunner) -> None:
    """
    Testing GoingToCamp - Manitoba Campsites
    """
    test_command = """
    camply campsites \
        --provider GoingToCamp \
        --rec-area 15 \
        --start-date 2023-08-01 \
        --end-date 2023-08-14 \
        --campground -2147483632
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Manitoba" in result.output
    assert "Winnipeg Beach Campground" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result)
