"""
Yellowstone Testing Provider
"""

import logging
from datetime import datetime

import pytest

from camply.containers import AvailableCampsite, CampgroundFacility, SearchWindow
from camply.search import SearchRecreationDotGov
from tests.conftest import vcr_cassette

logger = logging.getLogger(__name__)


@pytest.fixture
def search_window() -> SearchWindow:
    """
    Get A RecDotGov Search Window For September 2023

    Returns
    -------
    SearchWindow
    """
    search_window = SearchWindow(
        start_date=datetime(2023, 9, 1),
        end_date=datetime(2023, 10, 1),
    )
    return search_window


@pytest.fixture
def recdotgov_recarea_finder(search_window) -> SearchRecreationDotGov:
    """
    Assemble The Searching Class

    Returns
    -------
    SearchYellowstone
    """
    recdotgov_finder = SearchRecreationDotGov(
        search_window=search_window, recreation_area=2584
    )  # Big Bend National Park
    logger.info("RecreationDotGov Recreation Area Searcher Established.")
    logger.info(f"Search Months: {recdotgov_finder.search_months}")
    return recdotgov_finder


@pytest.fixture
def recdotgov_campground_finder(search_window) -> SearchRecreationDotGov:
    """
    Assemble The Searching Class

    Returns
    -------
    SearchYellowstone
    """
    recdotgov_finder = SearchRecreationDotGov(
        search_window=search_window, campgrounds=234708
    )  # Apache Trout CampgroundApache Trout Campground
    logger.info("RecreationDotGov Campground Searcher Established.")
    logger.info(f"Search Months: {recdotgov_finder.search_months}")
    return recdotgov_finder


@pytest.fixture
def recdotgov_campsite_finder(search_window) -> SearchRecreationDotGov:
    """
    Assemble The Searching Class

    Returns
    -------
    SearchYellowstone
    """
    recdotgov_finder = SearchRecreationDotGov(
        search_window=search_window, campsites=93740
    )  # Site: O, Loop: Group Sites L-R - Chisos Basin Group Campground
    logger.info("RecreationDotGov Campground Searcher Established.")
    logger.info(f"Search Months: {recdotgov_finder.search_months}")
    return recdotgov_finder


@vcr_cassette
def test_get_searchable_campgrounds_recarea(
    recdotgov_recarea_finder,
) -> None:
    """
    Retrieve Campground Information for a Recreation Area
    """
    logger.info("Searching for Matching Recreation Area Campgrounds")
    campgrounds = recdotgov_recarea_finder._get_searchable_campgrounds()
    assert campgrounds
    for camp in campgrounds:
        assert isinstance(camp, CampgroundFacility)


@vcr_cassette
def test_get_searchable_campgrounds_campground(
    recdotgov_campground_finder,
) -> None:
    """
    Retrieve Campground Information for a Campground ID
    """
    logger.info("Searching for Matching Campgrounds to Campground ID")
    campgrounds = recdotgov_campground_finder._get_searchable_campgrounds()
    assert campgrounds
    for camp in campgrounds:
        assert isinstance(camp, CampgroundFacility)


@vcr_cassette
def test_get_all_campsites_recarea(recdotgov_recarea_finder) -> None:
    """
    Get all of the Yellowstone Campsites
    """
    logger.info("Searching for All Recreation Area Campsites")
    all_campsites = recdotgov_recarea_finder.get_all_campsites()
    SearchRecreationDotGov.assemble_availabilities(
        matching_data=all_campsites, log=True, verbose=False
    )
    assert all_campsites
    for camp in all_campsites:
        assert isinstance(camp, AvailableCampsite)


@vcr_cassette
def test_get_all_campsites_campground(
    recdotgov_campground_finder,
) -> None:
    """
    Get all of the Yellowstone Campsites
    """
    logger.info("Searching for Campground Specific Campsites")
    all_campsites = recdotgov_campground_finder.get_all_campsites()
    SearchRecreationDotGov.assemble_availabilities(
        matching_data=all_campsites, log=True, verbose=False
    )
    assert all_campsites
    for camp in all_campsites:
        assert isinstance(camp, AvailableCampsite)


@vcr_cassette
def test_get_campsite_specific_campgrounds(
    recdotgov_campsite_finder,
) -> None:
    """
    Get all of the Related Campgrounds
    """
    logger.info("Searching for Campground Specific Campsites")
    campgrounds = recdotgov_campsite_finder._get_campgrounds_by_campsite_id()
    assert campgrounds
    for camp in campgrounds:
        assert isinstance(camp, CampgroundFacility)


@vcr_cassette
def test_get_campsite_specific_results(
    recdotgov_campsite_finder,
) -> None:
    """
    Get the related Campsite's availability
    """
    logger.info("Searching for Campground Specific Campsites")
    all_campsites = recdotgov_campsite_finder.get_all_campsites()
    SearchRecreationDotGov.assemble_availabilities(
        matching_data=all_campsites, log=True, verbose=False
    )
    assert all_campsites
    for camp in all_campsites:
        assert isinstance(camp, AvailableCampsite)
