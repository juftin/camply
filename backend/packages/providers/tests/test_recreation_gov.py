"""
Tests for Recreation.gov Provider
"""

import datetime
from unittest.mock import AsyncMock, patch

import pytest

from providers.dto import CampsiteType
from providers.recreation_gov.provider import (
    RecreationGovProvider,
    check_is_electric,
    map_campsite_type,
)


@pytest.fixture
def anyio_backend():
    return "asyncio"


def test_map_campsite_type():
    """
    Test that campsite type strings are parsed correctly into standardized enums.
    """
    assert map_campsite_type("Standard Tent Only") == CampsiteType.TENT
    assert map_campsite_type("Tent Only Nonelectric") == CampsiteType.TENT
    assert map_campsite_type("RV Electric") == CampsiteType.RV
    assert map_campsite_type("RV Nonelectric") == CampsiteType.RV
    assert map_campsite_type("Cabin") == CampsiteType.CABIN
    assert map_campsite_type("Yurt") == CampsiteType.CABIN
    assert map_campsite_type("Group Picnic Area") == CampsiteType.OTHER
    assert map_campsite_type(None) == CampsiteType.OTHER


def test_check_is_electric():
    """
    Test electric hookup checking logic from attributes and type.
    """
    from providers.recreation_gov.models.api import (
        RecDotGovAttribute,
        RecDotGovCampsite,
    )

    # 1. Electric in type
    campsite_with_type = RecDotGovCampsite(
        campsite_id=1,
        name="1",
        type="Electric RV",
    )
    assert check_is_electric(campsite_with_type) is True

    # 2. Electric in attributes
    campsite_with_attr = RecDotGovCampsite(
        campsite_id=2,
        name="2",
        attributes=[
            RecDotGovAttribute(
                attribute_id=1,
                attribute_name="Electricity Hookup",
                attribute_value="50 Amp",
            )
        ],
    )
    assert check_is_electric(campsite_with_attr) is True

    # 3. Not electric
    campsite_non_electric = RecDotGovCampsite(
        campsite_id=3,
        name="3",
        attributes=[
            RecDotGovAttribute(
                attribute_id=1,
                attribute_name="Electricity Hookup",
                attribute_value="No",
            )
        ],
    )
    assert check_is_electric(campsite_non_electric) is False


@pytest.mark.vcr
@pytest.mark.anyio
async def test_find_availabilities():
    """
    Test the complete async find_availabilities flow using VCRPy recorded HTTP requests.
    """
    provider = RecreationGovProvider()

    # We will query Apache Trout Campground (facility ID 234708)
    # for a specific date range that we record/replay.
    start_date = datetime.date(2026, 9, 1)
    end_date = datetime.date(2026, 9, 2)

    availabilities = await provider.find_availabilities(
        park_id="234708",
        start_date=start_date,
        end_date=end_date,
    )

    # Structural assertions to verify that data is loaded and mapped correctly
    assert isinstance(availabilities, list)
    # Check that we successfully fetch and map to DTOs
    for avail in availabilities:
        assert avail.campsite_id
        assert avail.campsite_name
        assert avail.campsite_type in CampsiteType
        assert isinstance(avail.available_dates, list)
        assert len(avail.available_dates) > 0
        assert all(start_date <= d <= end_date for d in avail.available_dates)


@pytest.mark.anyio
async def test_sync_metadata():
    """
    Test that sync_metadata calls populate_database.
    """
    provider = RecreationGovProvider()
    with patch.object(
        provider, "populate_database", new_callable=AsyncMock
    ) as mock_populate:
        await provider.sync_metadata()
        mock_populate.assert_called_once()
