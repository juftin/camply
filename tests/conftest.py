"""
Pytest Fixtures Shared Across all Unit Tests
"""

from typing import Dict

import pytest

module_scope = pytest.fixture(scope="module")


@module_scope
def vcr_config() -> Dict[str, list]:
    """
    VCR Cassette Privacy Enforcer

    This fixture ensures the API Credentials are obfuscated

    Returns
    -------
    Dict[str, list]:
    """
    return {
        "filter_headers": [
            ("authorization", "XXXXXXXXXX"),
            ("apikey", "XXXXXXXXXX"),
        ],
    }


# Decorator Object to Use pyvcr Cassettes on Unit Tests (see `pytest-vcr`)
# pass `--vcr-record=none` to pytest CI runs to ensure new cassettes are generated
camply_cassette = pytest.mark.vcr(scope="module")
