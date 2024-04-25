"""
Debugging Script
"""

from tests.conftest import CamplyRunner


def test_debug_camply(cli_runner: CamplyRunner) -> None:
    """
    Search for Multiple Campsites
    """
    test_command = """
    camply \
        campsites \
        --provider ReserveCalifornia \
        --campground 737 \
        --start-date 2024-04-29 \
        --end-date 2024-04-30
    """
    result = cli_runner.run_camply_command(command=test_command)
