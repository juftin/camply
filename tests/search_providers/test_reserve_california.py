"""
ReserveCalifornia Testing
"""

import datetime

from dateutil.relativedelta import relativedelta

from camply.providers import ReserveCalifornia
from tests.conftest import cli_status_checker, vcr_cassette


@vcr_cassette
def test_rc_get_rec_areas_api():
    """
    Test Pinging the API Directly: Rec Areas
    """
    prov = ReserveCalifornia()
    expected_rec_area = 678
    rec_areas = prov._search_recareas_api(query="Millerton Lake SRA")
    assert rec_areas[0].recreation_area_id == expected_rec_area


@vcr_cassette
def test_rc_get_campgrounds_api():
    """
    Test Pinging the API Directly: Campgrounds
    """
    prov = ReserveCalifornia()
    expected_facility = 572
    campgrounds = prov._get_campgrounds_api(rec_area_id=678)
    found = False
    for campground in campgrounds:
        if campground.facility_name == "North Shore Group Camp":
            assert campground.facility_id == expected_facility
            found = True
    assert found is True


@vcr_cassette
def test_rc_search_campgrounds_no_api():
    """
    Cached Results: Search Campgrounds
    """
    prov = ReserveCalifornia()
    expected_facility = 572
    campgrounds = prov.find_campgrounds(rec_area_id=[678])
    found = False
    for campground in campgrounds:
        if campground.facility_name == "North Shore Group Camp":
            assert campground.facility_id == expected_facility
            found = True
    assert found is True


@vcr_cassette
def test_rc_get_campsites():
    """
    Get Campsites
    """
    prov = ReserveCalifornia()
    start_date = datetime.date(2023, 6, 5)
    campsites = prov.get_campsites(
        campground_id=543,
        start_date=start_date,
        end_date=start_date + relativedelta(days=2),
    )
    assert len({item.campsite_id for item in campsites}) > 1
    assert any([item.campsite_site_name == "Campsite #M93" for item in campsites])


@vcr_cassette
def test_rc_get_metadata():
    """
    Cached Results: Metadata Fetching
    """
    prov = ReserveCalifornia()
    prov.refresh_metadata()


@vcr_cassette
def test_rc_search_recreation_area():
    """
    Cached Results: Search For RecArea
    """
    prov = ReserveCalifornia()
    results = prov.search_for_recreation_areas(query="Half Moon Bay")
    assert results[0].recreation_area_location == "Half Moon Bay, CA"


@vcr_cassette
def test_rc_search_campgrounds():
    """
    Cached Results: Search For Campground
    """
    prov = ReserveCalifornia()
    results = prov.find_campgrounds(search_string="Half Moon Bay", rec_area_id=[])
    assert results[0].recreation_area.__contains__("Half Moon Bay")


@vcr_cassette
def test_rc_cli_recreation_areas(cli_runner):
    """
    CLI Testing - recreation-areas
    """
    test_command = """
    camply recreation-areas --provider ReserveCalifornia --search "Los Angeles"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "Los Angeles State Historic Park, Calabasas, CA" in result.output


@vcr_cassette
def test_rc_cli_campgrounds(cli_runner):
    """
    CLI Testing - campgrounds
    """
    test_command = """
    camply campgrounds --provider ReserveCalifornia --search "Sonoma Coast"
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "Bodega Dunes" in result.output


@vcr_cassette
def test_rc_cli_campsites(cli_runner):
    """
    CLI Testing - Night Filtering
    """
    test_command = """
    camply campsites \
        --provider ReserveCalifornia \
        --start-date 2023-07-01 \
        --end-date 2023-08-01 \
        --rec-area 718 \
        --weekends
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "total sites found in month of July" in result.output
    assert "Sonoma Coast State Park" in result.output


@vcr_cassette
def test_rc_cli_campsites_nights(cli_runner):
    """
    CLI Testing - Night Filtering
    """
    test_command = """
    camply campsites \
      --start-date 2023-06-01 \
      --end-date 2023-07-01  \
      --campground 1121 \
      --provider ReserveCalifornia
    """
    result = cli_runner.run_camply_command(test_command)
    cli_status_checker(result=result, exit_code_zero=True)
    assert "Valley Oak Loop (sites 85-90)" in result.output
    assert "total sites found in month of June" in result.output
    assert "https://www.reservecalifornia.com" in result.output
