"""
CLI Testing: `camply ...`
"""

import logging

from camply import __version__
from camply.cli import camply_command_line
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette

logger = logging.getLogger(__name__)


@vcr_cassette
def test_main_succeeds(cli_runner: CamplyRunner) -> None:
    """
    It exits with a status code of zero.
    """
    result = cli_runner.invoke(camply_command_line)
    assert "Welcome to camply, the campsite finder" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_debug(cli_runner: CamplyRunner) -> None:
    """
    Use the Debug Option
    """
    test_command = """
    camply \
        campgrounds \
        --provider Yellowstone \
        --debug
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert __version__ in result.output
    cli_status_checker(result=result)
