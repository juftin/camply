"""
CLI Testing: `camply list-campsites...`
"""

import pathlib

from pytest import MonkeyPatch

from camply.providers import ReserveCalifornia
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette


@vcr_cassette
def test_list_campsites_recdotgov(cli_runner: CamplyRunner) -> None:
    """
    List campsites from Recreation.gov
    """
    test_command = "camply list-campsites --campground 232446"
    result = cli_runner.run_camply_command(command=test_command)
    assert "Wawona Campground" in result.output
    assert "⛺️ 003 - (#540)" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_list_campsites_reservecalifornia(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    List campsites from ReserveCalifornia
    """
    monkeypatch.setattr(ReserveCalifornia, "offline_cache_dir", tmp_path)
    test_command = "camply list-campsites --campground 598 --provider ReserveCalifornia"
    result = cli_runner.run_camply_command(command=test_command)
    assert "Campground Northern End (sites 44-111)" in result.output
    assert "Premium Campsite #82 - (#43467)" in result.output
    cli_status_checker(result=result, exit_code_zero=True)
