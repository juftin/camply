"""
camply-backend conftest
"""

from fastapi.testclient import TestClient
from pytest import fixture


@fixture
def test_client() -> TestClient:
    """
    Test Client Fixture
    """
    from backend.app import app

    return TestClient(app)
