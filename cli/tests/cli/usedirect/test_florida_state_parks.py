import os
import pathlib
from unittest import mock

from pytest import MonkeyPatch

from camply.providers import (
    FloridaStateParks,
)
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": FloridaStateParks.__name__})
def test_florida_state_parks_recreation_areas(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - FloridaStateParks Recreation Areas
    """
    monkeypatch.setattr(FloridaStateParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply recreation-areas \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "FloridaStateParks"' in result.output
    assert "William J. Rish Recreation Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": FloridaStateParks.__name__})
def test_florida_state_parks_campgrounds(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - FloridaStateParks Campgrounds
    """
    monkeypatch.setattr(FloridaStateParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply campgrounds \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "FloridaStateParks"' in result.output
    assert "Rainbow Springs State Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": FloridaStateParks.__name__})
def test_florida_state_parks_campsites(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - FloridaStateParks Campsites
    """
    monkeypatch.setattr(FloridaStateParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
        --campground 54 \
        --start-date 2023-07-01 \
        --end-date 2023-07-14
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "total sites found in month of July" in result.output
    assert 'Using Camply Provider: "FloridaStateParks"' in result.output
    assert "total sites found in month of July" in result.output
