"""
Debugging Script
"""

from tests.conftest import CamplyRunner


def test_debug_usedirect(cli_runner: CamplyRunner) -> None:
    """
    Debug the Camply CLI - ReserveCalifornia - UseDirect

    https://reservecalifornia.com/Web/#!park/726/737
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
    assert result.exit_code == 0
