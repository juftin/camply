"""
Health Check API
"""

import datetime
from functools import partial

from fastapi import APIRouter
from pydantic import BaseModel, Field

health_router = APIRouter(tags=["health"])


class ApiStatus(BaseModel):
    """
    API Status Response
    """

    status: int = Field(default=200, ge=100, le=599, description="HTTP Status Code")
    timestamp: datetime.datetime = Field(
        default_factory=partial(datetime.datetime.now, datetime.timezone.utc),
        description="Timestamp of the Health Check",
    )


@health_router.get("/ping")
def ping() -> ApiStatus:
    """
    API Ping
    """
    return ApiStatus(status=200)


@health_router.get("/health")
def healthcheck() -> ApiStatus:
    """
    API Health Check
    """
    return ApiStatus(status=200)
