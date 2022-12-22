"""
GoingToCamp Testing Provider
"""

import logging
from datetime import datetime, timedelta
from typing import List

import pytest
from dateutil.relativedelta import relativedelta

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchGoingToCamp

logger = logging.getLogger(__name__)


@pytest.fixture
def search_window() -> SearchWindow:
    """
    Get a Search Window For Next Month

    Returns
    -------
    SearchWindow
    """
    beginning_of_next_month = (datetime.now() + relativedelta(months=1)).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    search_window = SearchWindow(
        start_date=beginning_of_next_month,
        end_date=beginning_of_next_month + timedelta(days=15),
    )
    logger.info(
        "Setting Up Search Window starting Next Month: "
        f"{search_window.start_date.strftime('%B, %Y')}"
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
        campgrounds=[-2147483644],  # Waterford North Conservation Area
    )
    logger.info("GoingToCamp Campsite Searcher Established.")
    logger.info(f"Search Months: {gtc_finder.search_months}")
    return gtc_finder


def test_get_all_campsites(going_to_camp_finder) -> List[AvailableCampsite]:
    """
    Get all GTC sites for the rec area

    Returns
    -------
    List[AvailableCampsite]
    """
    logger.info("Searching for Campsites")
    all_campsites = going_to_camp_finder.get_all_campsites()
    return all_campsites
