"""
CLI Testing - RecreationDotGov Tours and Timed Entry
"""

import logging

from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette

logger = logging.getLogger(__name__)


@vcr_cassette
def test_recdotgov_daily_ticket_campgrounds(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovDailyTicket - Campgrounds
    """
    test_command = """
    camply campgrounds \
        --provider RecreationDotGovDailyTicket \
        --state CO
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Canyons Of The Ancients Museum Tours" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_recdotgov_daily_ticket_campsites(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovDailyTicket - Campsites
    """
    test_command = """
    camply campsites \
        --provider RecreationDotGovDailyTicket \
        --campground 234787 \
        --start-date 2023-09-09 \
        --end-date 2023-09-17
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "total sites found in month of" in result.output
    assert " Chimney Rock National Monument" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_recdotgov_ticket_campgrounds(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovTicket - Campgrounds
    """
    test_command = """
    camply campgrounds --state HI --provider RecreationDotGovTicket
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Haleakala National Park Summit Sunrise" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_recdotgov_ticket_campsites(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovTicket - Campsites
    """
    test_command = """
    camply campsites \
      --provider RecreationDotGovTicket \
      --start-date 2023-06-09 \
      --end-date 2023-06-10 \
      --campground 253731
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Haleakala National Park Summit Sunrise" in result.output
    assert "total sites found in month of" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_recdotgov_timed_entry_campgrounds(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovTimedEntry - Campgrounds
    """
    test_command = """
    camply campgrounds --provider RecreationDotGovTimedEntry --state OR
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Lava River Cave" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_recdotgov_timed_entry_campsites(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovTimedEntry - Campsites
    """
    test_command = """
    camply campsites \
      --provider RecreationDotGovTimedEntry \
      --start-date 2023-06-09 \
      --end-date 2023-06-10 \
      --campground 10089508
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Lava River Cave" in result.output
    assert "total sites found in month of" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_recdotgov_daily_ticket_campsites_equipment(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovDailyTicket - Campsites + Equipment
    """
    test_command = """
    camply campsites \
      --provider RecreationDotGovDailyTicket \
      --start-date 2023-07-06 \
      --end-date 2023-07-07 \
      --campground 300004 \
      --equipment 1300 4
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Filtering Campsites based on Equipment: 1300" in result.output
    assert "Joshua Tree National Park Tours" in result.output
    assert "total sites found in month of" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_list_campsites_ticket(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovTicket - List Campsites
    """
    test_command = """
    camply list-campsites \
        --provider RecreationDotGovTicket \
        --campground 253731
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Searching for campsites to list" in result.output
    assert "Haleakala Sunrise - Summit - (#255)" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_list_campsites_time_entry(cli_runner: CamplyRunner) -> None:
    """
    Provider: RecreationDotGovTimedEntry - List Campsites
    """
    test_command = """
    camply list-campsites \
        --provider RecreationDotGovTimedEntry \
        --campground 10089508
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Searching for campsites to list" in result.output
    assert "Lava River Cave Vehicle Reservations - (#10089509)" in result.output
    cli_status_checker(result=result, exit_code_zero=True)
