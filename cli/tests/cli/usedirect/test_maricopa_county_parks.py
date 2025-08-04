import os
import pathlib
from unittest import mock

from pytest import MonkeyPatch

from camply.providers import MaricopaCountyParks
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": MaricopaCountyParks.__name__})
def test_maricopa_county_parks_recreation_areas(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - Maricopa County Parks Recreation Areas
    """
    monkeypatch.setattr(MaricopaCountyParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply recreation-areas \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "MaricopaCountyParks"' in result.output
    assert "Cave Creek Regional Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": MaricopaCountyParks.__name__})
def test_maricopa_county_parks_campgrounds(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - Maricopa County Parks Campgrounds
    """
    monkeypatch.setattr(MaricopaCountyParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply campgrounds \
     --search "Park"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert 'Using Camply Provider: "MaricopaCountyParks"' in result.output
    assert "Cave Creek Regional Park" in result.output


@vcr_cassette
@mock.patch.dict(os.environ, {"CAMPLY_PROVIDER": MaricopaCountyParks.__name__})
def test_maricopa_county_parks_campsites(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    CLI Testing - Maricopa County Parks Campsites
    """
    monkeypatch.setattr(MaricopaCountyParks, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
        --campground 14 \
        --start-date 2023-07-01 \
        --end-date 2023-07-14
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "Lake Pleasant Regional Park" in result.output
    assert 'Using Camply Provider: "MaricopaCountyParks"' in result.output
    assert "total sites found in month of July" in result.output
