"""
CLI Testing: `camply campgrounds ...`
"""

import logging

from click.testing import CliRunner

from camply.cli import camply_command_line
from tests.conftest import assert_cli_success, vcr_cassette

logger = logging.getLogger(__name__)


@vcr_cassette
def test_list_recdotgov_campgrounds(cli_runner: CliRunner) -> None:
    """
    Test the Campground Search for a Fire Tower
    """
    result = cli_runner.invoke(
        cli=camply_command_line,
        args=[
            "campgrounds",
            "--provider",
            "RecreationDotGov",
            "--search",
            "Fire Tower",
            "--state",
            "CA",
        ],
    )
    assert "Furnace Creek Campground" in result.output
    assert_cli_success(result=result)
