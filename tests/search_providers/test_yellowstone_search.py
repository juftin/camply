#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Yellowstone Testing Provider
"""

from datetime import datetime, timedelta
import logging
from typing import List

from dateutil.relativedelta import relativedelta
import pytest

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchYellowstone

logger = logging.getLogger(__name__)


@pytest.fixture
def search_window() -> SearchWindow:
    """
    Get A Yellowstone Search Window For Next Month

    Returns
    -------
    SearchWindow
    """
    beginning_of_next_month = (datetime.now() + relativedelta(months=1)).replace(day=1, hour=0,
                                                                                 minute=0, second=0,
                                                                                 microsecond=0)
    search_window = SearchWindow(start_date=beginning_of_next_month,
                                 end_date=beginning_of_next_month + timedelta(days=15))
    logger.info("Setting Up Search Window starting Next Month: "
                f"{search_window.start_date.strftime('%B, %Y')}")
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


def test_get_all_campsites(yellowstone_finder) -> List[AvailableCampsite]:
    """
    Get all of the Yellowstone Campsites

    Returns
    -------
    List[AvailableCampsite]
    """
    logger.info("Searching for Campsites")
    all_campsites = yellowstone_finder.get_all_campsites()
    return all_campsites
