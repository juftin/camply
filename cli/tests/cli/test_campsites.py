"""
CLI Testing - Campsites: `camply campsites...`
"""

import logging
import pathlib

from pytest import MonkeyPatch

import camply.config
from camply.providers import ReserveCalifornia
from tests.conftest import CamplyRunner, cli_status_checker, vcr_cassette

logger = logging.getLogger(__name__)


@vcr_cassette
def test_no_options_passed(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites with no options - this should fail
    """
    test_command = """
    camply campsites --debug
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "ERROR" in result.output
    cli_status_checker(result=result, exit_code_zero=False)


@vcr_cassette
def test_search_by_recarea(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by RecArea
    """
    test_command = """
    camply \
        campsites \
        --rec-area 2991 \
        --start-date 2023-09-15 \
        --end-date 2023-09-17
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Wawona Campground" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_campground(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by Campground
    """
    test_command = """
    camply \
        campsites \
        --campground 252037 \
        --start-date 2023-09-15 \
        --end-date 2023-09-17
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Sardine Peak Lookout" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_yaml(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by YAML
    """
    test_command = """
    camply \
        campsites \
        --yaml-config \
        tests/yaml/example_search.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "YAML File Parsed: example_search.yaml" in result.output
    assert "Rocky Mountain National Park" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_another_yaml(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by Another YAML!
    """
    test_command = """
    camply \
        campsites \
        --yaml-config \
        tests/yaml/example_campsite_search.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "YAML File Parsed: example_campsite_search.yaml" in result.output
    assert "Ledgefork" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_misspelled_yaml(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by YAML (Misspelled Provider)
    """
    test_command = """
    camply \
        campsites \
        --yaml-config \
        tests/yaml/misspelled_search.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    cli_status_checker(result=result, exit_code_zero=False)


@vcr_cassette
def test_search_by_lowercase_yaml(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by YAML (Lowercase Provider)
    """
    test_command = """
    camply \
        campsites \
        --yaml-config \
        tests/yaml/lowercase_search.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_nights(cli_runner: CamplyRunner) -> None:
    """
    Search Functionality: Nights
    """
    test_command = """
    camply \
        campsites \
        --campground 232045 \
        --start-date 2023-07-15 \
        --end-date 2023-10-01 \
        --nights 5
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Forbes Creek" in result.output
    assert "5 consecutive" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_yellowstone(cli_runner: CamplyRunner) -> None:
    """
    Search Functionality: Yellowstone Provider
    """
    test_command = """
    camply \
        campsites \
        --provider yellowstone \
        --start-date 2023-10-10 \
        --end-date 2023-10-16
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Madison Campground" in result.output
    assert "Searching for Yellowstone Lodging" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_campsite_id(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by Campsite ID
    """
    test_command = """
    camply \
        campsites \
        --campsite 40107 \
        --start-date 2023-09-15 \
        --end-date 2023-09-17
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Ledgefork" in result.output
    assert "Searching Specific Campsite" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_yellowstone_campground(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by Campsite ID
    """
    test_command = """
    camply \
        campsites \
        --provider yellowstone \
        --start-date 2023-09-01 \
        --end-date 2023-09-14 \
        --campground YLYF:RV
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "13 booking nights selected for search" in result.output
    assert "Fishing Bridge RV Park" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_equipment(cli_runner: CamplyRunner) -> None:
    """
    Search for Campsites by Equipment
    """
    test_command = """
    camply \
        campsites \
        --rec-area 2018 \
        --start-date 2023-09-09 \
        --end-date 2023-09-17 \
        --nights 3 \
        --equipment RV 25
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Stone Cellar Guard Station" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_multiple_campsites(cli_runner: CamplyRunner) -> None:
    """
    Search for Multiple Campsites
    """
    test_command = """
    camply \
        campsites \
        --campsite 84865 \
        --campsite 84001 \
        --start-date 2023-09-27 \
        --end-date 2023-09-28
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Okanogan-Wenatchee National Forest, WA" in result.output
    assert "Searching Specific Campsite: ⛺️ 116" in result.output
    assert "Searching Specific Campsite: ⛺️ 118" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_error_prone_campground(cli_runner: CamplyRunner) -> None:
    """
    Search for a bad campground: 234779

    This campground didn't have a Parent Rec Area at one point
    """
    test_command = """
    camply \
        campsites \
        --start-date 2023-10-01 \
        --end-date 2023-10-02 \
        --campground 234779
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "USDA Forest Service, OR" in result.output
    assert "Haystack Campground" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_persist_json(cli_runner: CamplyRunner) -> None:
    """
    Persisting Campsites Between Searches: JSON
    """
    test_command = """
    camply \
        --debug \
        campsites \
        --campground 232064 \
        --start-date 2023-09-01 \
        --end-date 2023-10-01 \
        --offline-search \
        --offline-search-path test_file.json
    """
    result_1 = cli_runner.run_camply_command(command=test_command)
    result_2 = cli_runner.run_camply_command(command=test_command)
    camply.config.FileConfig.ROOT_DIRECTORY.joinpath("test_file.json").unlink()
    cli_status_checker(result=result_1, exit_code_zero=True)
    cli_status_checker(result=result_2, exit_code_zero=True)
    assert "Campsite search is configured to save offline" in result_1.output
    assert "test_file.json" in result_2.output
    assert "campsites loaded from file" in result_2.output


@vcr_cassette
def test_search_persist_pickle(cli_runner: CamplyRunner) -> None:
    """
    Persisting Campsites Between Searches: Pickle
    """
    test_command = """
    camply \
        --debug \
        campsites \
        --campground 232064 \
        --start-date 2023-09-01 \
        --end-date 2023-10-01 \
        --offline-search \
        --offline-search-path test_file.pickle
    """
    result_1 = cli_runner.run_camply_command(command=test_command)
    result_2 = cli_runner.run_camply_command(command=test_command)
    camply.config.FileConfig.ROOT_DIRECTORY.joinpath("test_file.pickle").unlink()
    cli_status_checker(result=result_1, exit_code_zero=True)
    cli_status_checker(result=result_2, exit_code_zero=True)
    assert "Campsite search is configured to save offline" in result_1.output
    assert "test_file.pickle" in result_2.output
    assert "campsites loaded from file" in result_2.output


@vcr_cassette
def test_search_once_failure(cli_runner: CamplyRunner) -> None:
    """
    Run Once + Continuous
    """
    test_command = """
    camply campsites \
        --rec-area 2725 \
        --start-date 2023-07-10 \
        --end-date 2023-07-18 \
        --notifications pushover \
        --search-once \
        --continuous
    """
    result = cli_runner.run_camply_command(command=test_command)
    cli_status_checker(result=result, exit_code_zero=False)
    error_message = "You cannot specify `--search-once` alongside `--continuous`"
    assert error_message in result.output


@vcr_cassette
def test_search_once_pushover(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    Run Once + Continuous
    """
    monkeypatch.setattr(ReserveCalifornia, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
        --campground 343 \
        --start-date 2023-07-13 \
        --end-date 2023-07-14 \
        --provider ReserveCalifornia \
        --search-once \
        --notifications pushover
    """
    result = cli_runner.run_camply_command(command=test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert (
        "Notifications active via: <SilentNotifications>, <PushoverNotifications>"
        in result.output
    )
    assert "1 New Campsites Found." in result.output


@vcr_cassette
def test_multiple_search_windows_recdotgov(cli_runner: CamplyRunner) -> None:
    """
    Multiple Search Windows: RecreationDotGov
    """
    test_command = """
    camply campsites \
        --campground 232045 \
        --start-date 2023-07-13 \
        --end-date 2023-07-14 \
        --start-date 2023-08-13 \
        --end-date 2023-08-14
    """
    result = cli_runner.run_camply_command(command=test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "2 different months selected for search" in result.output
    assert "2 booking nights selected for search" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output


@vcr_cassette
def test_multiple_search_windows_yellowstone(cli_runner: CamplyRunner) -> None:
    """
    Multiple Search Windows: Yellowstone
    """
    test_command = """
    camply campsites \
        --provider yellowstone \
        --start-date 2023-07-13 \
        --end-date 2023-07-14 \
        --start-date 2023-08-13 \
        --end-date 2023-08-14
    """
    result = cli_runner.run_camply_command(command=test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "2 different months selected for search" in result.output
    assert "2 booking nights selected for search" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output


@vcr_cassette
def test_multiple_search_windows_reservecalifornia(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    Multiple Search Windows: ReserveCalifornia
    """
    monkeypatch.setattr(ReserveCalifornia, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
        --provider ReserveCalifornia \
        --campground 343 \
        --start-date 2023-07-13 \
        --end-date 2023-07-14 \
        --start-date 2023-08-13 \
        --end-date 2023-08-14
    """
    result = cli_runner.run_camply_command(command=test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "2 different months selected for search" in result.output
    assert "2 booking nights selected for search" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output


@vcr_cassette
def test_multiple_search_windows_goingtocamp(cli_runner: CamplyRunner) -> None:
    """
    Multiple Search Windows: GoingToCamp
    """
    test_command = """
    camply \
      campsites \
      --provider goingtocamp \
      --rec-area 1 \
      --start-date 2023-09-01 \
      --end-date 2023-09-02 \
      --start-date 2023-10-01 \
      --end-date 2023-10-02 \
      --equipment-id -32768 \
      --campground -2147483643
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "2 different months selected for search" in result.output
    assert "2 booking nights selected for search" in result.output
    assert "Long Point Region" in result.output
    assert "Waterford North Conservation Area" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result)


@vcr_cassette
def test_multiple_search_windows_yaml(cli_runner: CamplyRunner) -> None:
    """
    Multiple Search Windows: YAML
    """
    test_command = """
    camply \
        campsites \
        --yaml-config \
        tests/yaml/double_window_campsite_search.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "2 different months selected for search" in result.output
    assert "2 booking nights selected for search" in result.output
    assert "YAML File Parsed: double_window_campsite_search.yaml" in result.output
    assert "Ledgefork" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_specific_weekdays(cli_runner: CamplyRunner) -> None:
    """
    Only search for specific weekdays
    """
    test_command = """
    camply campsites \
        --campground 232446 \
        --start-date 2023-05-01 \
        --end-date 2023-08-01 \
        --day Wednesday
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "13 booking nights selected for search" in result.output
    assert "3 different months selected for search" in result.output
    assert "Wawona Campground" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_specific_weekdays_yaml(cli_runner: CamplyRunner) -> None:
    """
    Only search for specific weekdays using YAML
    """
    test_command = """
    camply \
        campsites \
        --yaml-config \
        tests/yaml/weekday_search.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "13 booking nights selected for search" in result.output
    assert "3 different months selected for search" in result.output
    assert "Wawona Campground" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_campsites_reservecalifornia(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    Search by Campsite: ReserveCalifornia
    """
    monkeypatch.setattr(ReserveCalifornia, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
      --provider ReserveCalifornia \
      --campground 598 \
      --campsite 43476 \
      --start-date 2023-07-04 \
      --end-date 2023-07-06
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "Campground Northern End (sites 44-111)" in result.output
    assert "Campsite #91" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_yaml_search_equipment_array(cli_runner: CamplyRunner) -> None:
    """
    Search by Equipment Array: YAML
    """
    test_command = """
    camply campsites \
      --yaml-config \
      tests/yaml/equipment_scenario_1.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "YAML File Parsed:" in result.output
    assert "Rocky Mountain National Park" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_yaml_search_equipment_single(cli_runner: CamplyRunner) -> None:
    """
    Search by Equipment Single: YAML
    """
    test_command = """
    camply campsites \
      --yaml-config \
      tests/yaml/equipment_scenario_2.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "YAML File Parsed:" in result.output
    assert "Rocky Mountain National Park" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result, exit_code_zero=True)


@vcr_cassette
def test_search_by_yaml_reservecalifornia(
    cli_runner: CamplyRunner, tmp_path: pathlib.Path, monkeypatch: MonkeyPatch
) -> None:
    """
    Search by Campsite YAML: ReserveCalifornia
    """
    monkeypatch.setattr(ReserveCalifornia, "offline_cache_dir", tmp_path)
    test_command = """
    camply campsites \
      --yaml-config \
      tests/yaml/reserve_california.yaml
    """
    result = cli_runner.run_camply_command(command=test_command)
    assert "YAML File Parsed:" in result.output
    assert "Andrew Molera SP" in result.output
    assert "Reservable Campsites Matching Search Preferences" in result.output
    cli_status_checker(result=result, exit_code_zero=True)
