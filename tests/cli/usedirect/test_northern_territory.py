import os
import pathlib
from unittest import mock

from pytest import MonkeyPatch

from camply.providers import (
    NorthernTerritory,
)
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": NorthernTerritory.__name__})
def test_northern_territory_recreation_areas(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - NorthernTerritory Recreation Areas
    """
    monkeypatch.setattr(NorthernTerritory, "offline_cache_dir", tmp_path)
    test_command = """
    camply recreation-areas \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "NorthernTerritory"' in result.output
    assert "Litchfield National Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": NorthernTerritory.__name__})
def test_northern_territory_campgrounds(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - NorthernTerritory Campgrounds
    """
    monkeypatch.setattr(NorthernTerritory, "offline_cache_dir", tmp_path)
    test_command = """
    camply campgrounds \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "NorthernTerritory"' in result.output
    assert "Litchfield National Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": NorthernTerritory.__name__})
def test_northern_territory_campsites(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - NorthernTerritory Campsites
    """
    monkeypatch.setattr(NorthernTerritory, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
        --campground 82 \
        --start-date 2023-07-01 \
        --end-date 2023-07-14
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "NorthernTerritory"' in result.output
    assert "Sandy Creek Campground" in result.output
    assert "total sites found in month of July" in result.output
