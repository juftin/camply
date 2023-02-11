import datetime
import logging

from dateutil.relativedelta import relativedelta

from camply.config.logging_config import set_up_logging
from camply.providers import ReserveCalifornia
from tests.conftest import cli_status_checker, vcr_cassette

set_up_logging(log_level=logging.DEBUG)


@vcr_cassette
def test_rc_get_rec_areas_api():
    prov = ReserveCalifornia()
    expected_rec_area = 678
    rec_areas = prov.search_recareas_api(query="Millerton Lake SRA")
    assert rec_areas[0].recreation_area_id == expected_rec_area


@vcr_cassette
def test_rc_get_campgrounds_api():
    prov = ReserveCalifornia()
    expected_facility = 572
    campgrounds = prov.get_campgrounds_api(rec_area_id=678)
    found = False
    for campground in campgrounds:
        if campground.facility_name == "North Shore Group Camp":
            assert campground.facility_id == expected_facility
            found = True
    assert found is True


@vcr_cassette
def test_rc_search_campgrounds_no_api():
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
    prov = ReserveCalifornia()
    start_date = datetime.date(2023, 6, 5)
    campsites = prov.get_campsites(
        campground_id=543,
        start_date=start_date,
        end_date=start_date + relativedelta(days=2),
    )
    assert len({item.campsite_id for item in campsites}) > 1
    assert any([item.campsite_site_name == "M93" for item in campsites])


@vcr_cassette
def test_rc_get_metadata():
    prov = ReserveCalifornia()
    prov.refresh_metadata()


@vcr_cassette
def test_rc_search_recreation_area():
    prov = ReserveCalifornia()
    results = prov.search_for_recreation_areas(query="Half Moon Bay")
    assert results[0].recreation_area_location == "Half Moon Bay, CA"


@vcr_cassette
def test_rc_search_campgrounds():
    prov = ReserveCalifornia()
    results = prov.find_campgrounds(search_string="Half Moon Bay", rec_area_id=[])
    assert results[0].recreation_area.__contains__("Half Moon Bay")


@vcr_cassette
def test_rc_find_campsites_cli(cli_runner):
    result = cli_runner.run_camply_command(
        """
    camply campsites \
      --start-date 2023-06-01 \
      --end-date 2023-07-01  \
      --campground 1121 \
      --provider ReserveCalifornia
    """
    )
    cli_status_checker(result=result, exit_code_zero=False)
    raise ValueError(result.output)
