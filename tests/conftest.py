"""
Pytest Fixtures Shared Across all Unit Tests
"""
import datetime
import logging
from typing import Any, Dict

import pytest
from click.testing import CliRunner, Result

from camply import AvailableCampsite

logger = logging.getLogger(__name__)
logging.getLogger("vcr.cassette").setLevel(logging.WARNING)

module_scope = pytest.fixture(scope="module")


@pytest.fixture
def cli_runner() -> CliRunner:
    """
    Fixture for invoking command-line interfaces.
    """
    return CliRunner()


def assert_cli_success(result: Result) -> None:
    """
    Handle Exceptions from the CLI
    """
    try:
        assert result.exit_code == 0
    except AssertionError:
        logger.exception(result.exception, exc_info=result.exc_info)
        raise result.exception


def scrub_string(string, replacement=""):
    """
    Nested Scrubbing Function
    """

    def before_record_response(response):
        body = response["body"]["string"]
        sensitive_strings = string.split(",")
        try:
            sensitive_strings.remove("<CAMPLY>")
        except ValueError:
            pass
        for string_part in sensitive_strings:
            string_part = string_part.strip()
            if isinstance(body, bytes):
                try:
                    body = body.decode("utf-8").replace(string_part, replacement)
                    body = str.encode(body)
                except UnicodeDecodeError:
                    pass
            else:
                body = body.replace(string, replacement)
        response["body"]["string"] = body
        return response

    return before_record_response


@module_scope
def vcr_config() -> Dict[str, Any]:
    """
    VCR Cassette Privacy Enforcer

    This fixture ensures the API Credentials are obfuscated

    Returns
    -------
    Dict[str, Any]
    """
    return {
        "filter_headers": [("authorization", "REDACTED"), ("apikey", "REDACTED")],
        "filter_query_parameters": [("user", "REDACTED"), ("token", "REDACTED")],
        # "before_record_response": scrub_string(
        #     getenv("SENSITIVE_REQUEST_STRINGS", "<CAMPLY>"), "REDACTED"
        # ),
    }


# Decorator Object to Use pyvcr Cassettes on Unit Tests (see `pytest-vcr`)
# pass `--vcr-record=none` to pytest CI runs to ensure new cassettes are generated
vcr_cassette = pytest.mark.vcr(scope="module")


@pytest.fixture
def available_campsite() -> AvailableCampsite:
    """
    Test AvailableCampsite Instance
    """
    return AvailableCampsite(
        campsite_id=100,
        booking_date=datetime.datetime(2023, 9, 1),
        booking_end_date=datetime.datetime(2023, 9, 2),
        booking_nights=1,
        campsite_site_name="Test Campsite Name",
        campsite_loop_name="A1",
        campsite_type="Test",
        campsite_occupancy=(1, 5),
        campsite_use_type="Test",
        availability_status="Available",
        recreation_area="Test Recreation Area",
        recreation_area_id=20,
        facility_name="Test Campground",
        facility_id=50,
        booking_url="https://youtu.be/eBGIQ7ZuuiU",
        permitted_equipment=[],
        campsite_attributes=[],
    )
