"""
Health Check API
"""

from typing import Any

from fastapi import APIRouter

from backend.dependencies import SessionDep

search_router = APIRouter(tags=["search"])


@search_router.get("/search")
async def search(
    query: str, session: SessionDep, limit: int = 20
) -> list[dict[str, Any]]:
    """
    Database Search for Recreation Areas and Campgrounds
    """
    return []
