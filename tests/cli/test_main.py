"""
CLI Testing: `camply ...`
"""

import logging

from click.testing import CliRunner

from camply.cli import camply_command_line
from tests.conftest import assert_cli_success

logger = logging.getLogger(__name__)


def test_main_succeeds(cli_runner: CliRunner) -> None:
    """
    It exits with a status code of zero.
    """
    result = cli_runner.invoke(camply_command_line)
    assert "Welcome to camply, the campsite finder" in result.output
    assert_cli_success(result=result)
