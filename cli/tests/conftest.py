"""
Pytest Fixtures Shared Across all Unit Tests
"""

import datetime
import logging
from textwrap import dedent
from typing import Any, Dict

import pytest
from click.testing import CliRunner, Result
from freezegun import freeze_time

from camply import AvailableCampsite
from camply.cli import camply_command_line

logger = logging.getLogger(__name__)
[
    logging.getLogger(loggo).setLevel(logging.WARNING)
    for loggo in [
        "vcr.cassette",
        "vcr.request",
        "vcr.matchers",
    ]
]
module_scope = pytest.fixture(scope="module")


@pytest.fixture(autouse=True)
def freeze_current_time():
    """
    Freeze the Current Time to April 28, 2023 at Noon

    Since camply saves the responses of the API calls, we need to freeze the time
    to ensure the responses are the same across all tests.
    """
    year = 2023
    time_of_year = [4, 28, 12, 0, 0]  # April 28th
    frozen_time = datetime.datetime(year, *time_of_year)
    with freeze_time(frozen_time, tick=True):
        yield


class CamplyRunner(CliRunner):
    """
    Custom CLI Runner for Camply
    """

    def run_camply_command(self, command: str) -> Result:
        """
        Run a Camply Command and Return the Result

        Parameters
        ----------
        command

        Returns
        -------
        Result
        """
        parsed_command = self.parse_camply_command(command=command)
        logger.debug("Camply CLI: %s", parsed_command)
        result = self.invoke(cli=camply_command_line, args=parsed_command)
        return result

    @classmethod
    def parse_camply_command(cls, command: str) -> str:
        """
        Parse a Camply CLI Command to a Parseable Str

        Parameters
        ----------
        command: str

        Returns
        -------
        str
        """
        command_parsed = dedent(command).strip()
        for r in (("\\", ""), ("\n", ""), ("\t", " "), ("  ", " "), ("camply ", "")):
            command_parsed = command_parsed.replace(*r)
        return command_parsed


@pytest.fixture
def cli_runner() -> CamplyRunner:
    """
    Fixture for invoking command-line interfaces.
    """
    return CamplyRunner()


def cli_status_checker(result: Result, exit_code_zero: bool = True) -> None:
    """
    Handle Exceptions from the CLI

    Parameters
    ----------
    result : Result
        CliRunner Invoke Result
    exit_code_zero: bool
        Whether the exit code should be `0` - defaults to True
    """
    try:
        assert (result.exit_code == 0) == exit_code_zero
    except AssertionError as e:
        logger.exception(result.exception, exc_info=result.exc_info)
        raise result.exception from e


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
