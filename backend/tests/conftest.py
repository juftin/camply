"""
camply-web conftest
"""

from fastapi.testclient import TestClient
from pytest import fixture


@fixture
def test_client() -> TestClient:
    """
    Test Client Fixture
    """
    from camply_web.app import app

    return TestClient(app)
