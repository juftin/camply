"""
GoingToCamp Testing Provider
"""

import logging
from datetime import datetime

import pytest

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchGoingToCamp
from tests.conftest import vcr_cassette

logger = logging.getLogger(__name__)


@pytest.fixture
def search_window() -> SearchWindow:
    """
    Get A Search Window For September 2023

    Returns
    -------
    SearchWindow
    """
    search_window = SearchWindow(
        start_date=datetime(2023, 9, 1),
        end_date=datetime(2023, 9, 2),
    )
    return search_window


@pytest.fixture
def going_to_camp_finder(search_window) -> SearchGoingToCamp:
    """
    Assemble The Searching Class

    Returns
    -------
    SearchGoingToCamp
    """
    gtc_finder = SearchGoingToCamp(
        search_window=search_window,
        recreation_area=[1],  # Long Point Region, Ontario
        campgrounds="-2147483643",  # Waterford North Conservation Area
    )
    logger.info("GoingToCamp Campsite Searcher Established.")
    logger.info(f"Search Months: {gtc_finder.search_months}")
    return gtc_finder


@vcr_cassette
def test_going_to_camp_get_all_campsites(
    going_to_camp_finder: SearchGoingToCamp,
) -> None:
    """
    Get all GTC sites for the rec area
    """
    logger.info("Searching for Campsites")
    all_campsites = going_to_camp_finder.get_all_campsites()
    assert all_campsites
    for camp in all_campsites:
        assert isinstance(camp, AvailableCampsite)
