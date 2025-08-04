import os
import pathlib
from unittest import mock

from pytest import MonkeyPatch

from camply.providers import (
    OhioStateParks,
)
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": OhioStateParks.__name__})
def test_reserve_ohio_recreation_areas(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - OhioStateParks Recreation Areas
    """
    monkeypatch.setattr(OhioStateParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply recreation-areas \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "OhioStateParks"' in result.output
    assert "Mosquito Lake State Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": OhioStateParks.__name__})
def test_reserve_ohio_campgrounds(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - OhioStateParks Campgrounds
    """
    monkeypatch.setattr(OhioStateParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply campgrounds \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "OhioStateParks"' in result.output
    assert "Wingfoot Lake State Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": OhioStateParks.__name__})
def test_reserve_ohio_campsites(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - OhioStateParks Campsites
    """
    monkeypatch.setattr(OhioStateParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
        --campground 536 \
        --start-date 2023-07-01 \
        --end-date 2023-07-14
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "total sites found in month of July" in result.output
    assert "Pymatuning Cabins" in result.output
    assert 'Using Camply Provider: "OhioStateParks"' in result.output
    assert "total sites found in month of July" in result.output
