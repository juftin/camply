"""
Tests for geo_utils
"""
import pytest

from camply.utils.geo_utils import haversine_distance_miles, geocode_location


def test_haversine_same_point():
    assert haversine_distance_miles(37.77, -122.41, 37.77, -122.41) == pytest.approx(0.0, abs=0.001)


def test_haversine_sf_to_la():
    # San Francisco to Los Angeles is ~347 miles
    result = haversine_distance_miles(37.7749, -122.4194, 34.0522, -118.2437)
    assert 340 < result < 360


def test_haversine_sf_to_nyc():
    # SF to NYC is ~2570 miles
    result = haversine_distance_miles(37.7749, -122.4194, 40.7128, -74.0060)
    assert 2500 < result < 2650


def test_geocode_returns_tuple(mocker):
    mock_location = mocker.MagicMock()
    mock_location.latitude = 37.7749
    mock_location.longitude = -122.4194
    mocker.patch(
        "camply.utils.geo_utils.Nominatim.geocode",
        return_value=mock_location,
    )
    lat, lon = geocode_location("San Francisco, CA")
    assert lat == pytest.approx(37.7749)
    assert lon == pytest.approx(-122.4194)


def test_geocode_raises_on_not_found(mocker):
    mocker.patch("camply.utils.geo_utils.Nominatim.geocode", return_value=None)
    with pytest.raises(Exception, match="Could not geocode"):
        geocode_location("zzzznotarealplace12345")
