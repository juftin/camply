"""
Tests for SearchGeo and excluded_campsite_types filtering
"""
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from camply.containers import AvailableCampsite, SearchWindow
from camply.search.search_geo import SearchGeo, _YELLOWSTONE_CENTER


@pytest.fixture
def search_window() -> SearchWindow:
    return SearchWindow(
        start_date=datetime(2026, 7, 1),
        end_date=datetime(2026, 7, 15),
    )


# --- Type exclusion filter tests ---


class TestExcludedCampsiteTypes:
    def test_excluded_type_removed(self, available_campsite):
        """A campsite with a matching type is removed by the filter."""
        group_campsite = available_campsite.copy(update={"campsite_type": "Group Standard"})
        excluded = ["group"]
        result = [
            c
            for c in [available_campsite, group_campsite]
            if not any(
                excl.lower() in (c.campsite_type or "").lower() for excl in excluded
            )
        ]
        assert available_campsite in result
        assert group_campsite not in result

    def test_exclusion_is_case_insensitive(self, available_campsite):
        """Exclusion matching ignores case."""
        horse_campsite = available_campsite.copy(update={"campsite_type": "HORSE ONLY"})
        excluded = ["horse"]
        result = [
            c
            for c in [horse_campsite]
            if not any(
                excl.lower() in (c.campsite_type or "").lower() for excl in excluded
            )
        ]
        assert result == []

    def test_none_campsite_type_not_excluded(self, available_campsite):
        """Campsites with no type are never excluded."""
        none_type_campsite = available_campsite.copy(update={"campsite_type": None})
        excluded = ["group"]
        result = [
            c
            for c in [none_type_campsite]
            if not any(
                excl.lower() in (c.campsite_type or "").lower() for excl in excluded
            )
        ]
        assert none_type_campsite in result

    def test_empty_exclusion_list_passes_all(self, available_campsite):
        """An empty exclusion list keeps all campsites."""
        group_campsite = available_campsite.copy(update={"campsite_type": "Group Standard"})
        excluded: list = []
        result = [
            c
            for c in [available_campsite, group_campsite]
            if not any(
                excl.lower() in (c.campsite_type or "").lower() for excl in excluded
            )
        ]
        assert len(result) == 2

    def test_non_matching_type_kept(self, available_campsite):
        """A campsite whose type does not match any exclusion is kept."""
        excluded = ["group"]
        result = [
            c
            for c in [available_campsite]
            if not any(
                excl.lower() in (c.campsite_type or "").lower() for excl in excluded
            )
        ]
        assert available_campsite in result  # campsite_type="Test" does not contain "group"


# --- SearchGeo construction tests ---


class TestSearchGeoYellowstone:
    def test_yellowstone_excluded_when_far(self, search_window):
        """Yellowstone is not included when the search center is far from the park."""
        searcher = SearchGeo.__new__(SearchGeo)
        searcher.latitude = 37.77   # San Francisco — ~1400 miles from Yellowstone
        searcher.longitude = -122.41
        searcher.radius_miles = 100.0

        result = searcher._build_yellowstone_search(
            shared=dict(
                search_window=search_window,
                weekends_only=False,
                nights=1,
            )
        )
        assert result == []

    def test_yellowstone_included_when_near(self, search_window):
        """Yellowstone is included when the search center is within radius."""
        searcher = SearchGeo.__new__(SearchGeo)
        searcher.latitude = _YELLOWSTONE_CENTER[0] + 0.1  # just north of center
        searcher.longitude = _YELLOWSTONE_CENTER[1]
        searcher.radius_miles = 20.0

        with patch(
            "camply.search.search_geo.SearchYellowstone.__init__",
            return_value=None,
        ):
            result = searcher._build_yellowstone_search(
                shared=dict(
                    search_window=search_window,
                    weekends_only=False,
                    nights=1,
                )
            )
        assert len(result) == 1


class TestSearchGeoNoCampgrounds:
    def test_no_campgrounds_found_exits(self, search_window):
        """SearchGeo exits with sys.exit(1) when no campgrounds are found within radius."""
        with patch.object(
            SearchGeo,
            "_build_sub_searches",
            return_value=[],
        ):
            with pytest.raises(SystemExit):
                SearchGeo(
                    search_window=search_window,
                    latitude=37.77,
                    longitude=-122.41,
                    radius_miles=1.0,
                )
