"""
Health check tests
"""

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("path", ["/api/health", "/api/ping"])
def test_health_check(test_client: TestClient, path: str) -> None:
    """
    Test health check
    """
    response = test_client.get(path)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == 200
