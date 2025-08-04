import os
import pathlib
from unittest import mock

from pytest import MonkeyPatch

from camply.providers import (
    OregonMetro,
)
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": OregonMetro.__name__})
def test_oregon_metro_recreation_areas(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - OregonMetro recreation areas
    """
    monkeypatch.setattr(OregonMetro, "offline_cache_dir", tmp_path)
    test_command = """
    camply recreation-areas \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "OregonMetro"' in result.output
    assert "Oxbow Regional Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": OregonMetro.__name__})
def test_oregon_metro_campgrounds(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - OregonMetro campgrounds
    """
    monkeypatch.setattr(OregonMetro, "offline_cache_dir", tmp_path)
    test_command = """
    camply campgrounds \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "OregonMetro"' in result.output
    assert "Oxbow Regional Park Campground" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": OregonMetro.__name__})
def test_oregon_metro_campsites(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - OregonMetro campsites
    """
    monkeypatch.setattr(OregonMetro, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
        --campground 107 \
        --start-date 2023-06-01 \
        --end-date 2023-07-01
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "Oxbow Regional Park Campground" in result.output
    assert 'Using Camply Provider: "OregonMetro"' in result.output
    assert "total sites found in month of June" in result.output
