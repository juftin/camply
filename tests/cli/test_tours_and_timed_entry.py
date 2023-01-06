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
