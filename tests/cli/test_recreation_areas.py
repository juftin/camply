"""
CLI Testing: `camply recreation-areas ...`
"""

import logging

from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette

logger = logging.getLogger(__name__)


@vcr_cassette
def test_search_recreation_areas(cli_runner: CamplyRunner) -> None:
    """
    Search By a Query String with Rec Areas
    """
    test_command = """
    camply \
        recreation-areas \
        --search "Yosemite National Park"
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "2991" in result.output
    cli_status_checker(result=result)
