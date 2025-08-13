"""
Campgrounds
"""

from fastapi import APIRouter
from sqlalchemy import select

from backend.dependencies import SessionDep
from backend.models.campgrounds import Campground
from db.models import Campground as CampgroundDB

campground_router = APIRouter(prefix="/campground", tags=["campgrounds"])


@campground_router.get("/{provider}/{id}")
async def get_campground(provider: int, id: str, session: SessionDep) -> Campground:
    """
    Get Campground by ID
    """
    result = await session.execute(
        select(CampgroundDB).where(
            CampgroundDB.provider_id == provider,
            CampgroundDB.id == id,
            CampgroundDB.reservable.is_(True),
        )
    )
    fetched = result.scalar_one_or_none()
    if fetched is None:
        raise ValueError("Campground not found")
    return Campground(
        id=fetched.id,
        provider_id=fetched.provider_id,
        recreation_area_id=fetched.recreation_area_id,
        name=fetched.name,
        description=fetched.description,
        country=fetched.country,
        state=fetched.state,
        longitude=fetched.longitude,
        latitude=fetched.latitude,
        reservable=fetched.reservable,
        enabled=fetched.enabled,
    )
