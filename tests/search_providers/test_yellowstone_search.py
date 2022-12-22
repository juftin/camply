"""
Yellowstone Testing Provider
"""

import logging
from datetime import datetime

import pytest

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchYellowstone
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
        end_date=datetime(2023, 10, 1),
    )
    return search_window


@pytest.fixture
def yellowstone_finder(search_window) -> SearchYellowstone:
    """
    Assemble The Searching Class

    Returns
    -------
    SearchYellowstone
    """
    yellowstone_finder = SearchYellowstone(search_window=search_window)
    logger.info("Yellowstone Campsite Searcher Established.")
    logger.info(f"Search Months: {yellowstone_finder.search_months}")
    return yellowstone_finder


@vcr_cassette
def test_yellowstone_get_all_campsites(yellowstone_finder) -> None:
    """
    Get all of the Yellowstone Campsites
    """
    logger.info("Searching for Campsites")
    all_campsites = yellowstone_finder.get_all_campsites()
    for camp in all_campsites:
        assert isinstance(camp, AvailableCampsite)
