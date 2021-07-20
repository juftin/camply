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
from camply.search import SearchRecreationDotGov

logger = logging.getLogger(__name__)


@pytest.fixture
def search_window() -> SearchWindow:
    """
    Get A RecDotGov Search Window For Next Month

    Returns
    -------
    SearchWindow
    """
    beginning_of_next_month = (datetime.now() + relativedelta(months=2)).replace(day=1, hour=0,
                                                                                 minute=0, second=0,
                                                                                 microsecond=0)
    search_window = SearchWindow(start_date=beginning_of_next_month,
                                 end_date=beginning_of_next_month + timedelta(days=29))
    logger.info("Setting Up Search Window starting Next Month: "
                f"{search_window.start_date.strftime('%B, %Y')}")
    return search_window


@pytest.fixture
def recdotgov_recarea_finder(search_window) -> SearchRecreationDotGov:
    """
    Assemble The Searching Class

    Returns
    -------
    SearchYellowstone
    """
    recdotgov_finder = SearchRecreationDotGov(search_window=search_window,
                                              recreation_area=2907)  # Rocky Mtn / Arapahoe
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
    recdotgov_finder = SearchRecreationDotGov(search_window=search_window,
                                              campgrounds=232493)  # Fish Creek, Glacier Ntl Park
    logger.info("RecreationDotGov Campground Searcher Established.")
    logger.info(f"Search Months: {recdotgov_finder.search_months}")
    return recdotgov_finder


def test_get_searchable_campgrounds_recarea(recdotgov_recarea_finder) -> List[AvailableCampsite]:
    """
    Retrieve Campground Information for a Recreation Area

    Returns
    -------
    List[AvailableCampsite]
    """
    logger.info("Searching for Matching Recreation Area Campgrounds")
    all_campsites = recdotgov_recarea_finder._get_searchable_campgrounds()
    return all_campsites


def test_get_searchable_campgrounds_campground(
        recdotgov_campground_finder) -> List[AvailableCampsite]:
    """
    Retrieve Campground Information for a Campground ID

    Returns
    -------
    List[AvailableCampsite]
    """
    logger.info("Searching for Matching Campgrounds to Campground ID")
    all_campsites = recdotgov_campground_finder._get_searchable_campgrounds()
    return all_campsites


def test_get_all_campsites_recarea(recdotgov_recarea_finder) -> List[AvailableCampsite]:
    """
    Get all of the Yellowstone Campsites

    Returns
    -------
    List[AvailableCampsite]
    """
    logger.info("Searching for All Recreation Area Campsites")
    all_campsites = recdotgov_recarea_finder.get_all_campsites()
    SearchRecreationDotGov.assemble_availabilities(matching_data=all_campsites, log=True,
                                                   verbose=False)
    return all_campsites


def test_get_all_campsites_campground(recdotgov_campground_finder) -> List[AvailableCampsite]:
    """
    Get all of the Yellowstone Campsites

    Returns
    -------
    List[AvailableCampsite]
    """
    logger.info("Searching for Campground Specific Campsites")
    all_campsites = recdotgov_campground_finder.get_all_campsites()
    SearchRecreationDotGov.assemble_availabilities(matching_data=all_campsites, log=True,
                                                   verbose=False)
    return all_campsites
