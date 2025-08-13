"""
Recreation Areas
"""

from functools import cached_property

from fastapi import APIRouter
from pydantic import BaseModel, computed_field
from sqlalchemy import select

from backend.dependencies import SessionDep
from backend.models.campgrounds import Campground
from db.models import Campground as CampgroundDB
from db.models import RecreationArea as RecreationAreaDB
from providers import PROVIDERS
from providers.base import BaseProvider

recreation_area_router = APIRouter(prefix="/rec-area", tags=["recreation_areas"])


class RecreationArea(BaseModel):
    """
    Recreation Area Model
    """

    id: str
    provider_id: int
    name: str
    description: str | None
    country: str | None
    state: str | None
    longitude: float | None
    latitude: float | None
    reservable: bool = True
    enabled: bool = True

    @cached_property
    def provider(self) -> type[BaseProvider]:
        """
        Get the provider instance for this recreation area.
        """
        return PROVIDERS[self.provider_id]

    @computed_field
    def url(self) -> str:
        return self.provider.get_rec_area_url(rec_area_id=self.id)


@recreation_area_router.get("/{provider}/{id}")
async def recreation_area(
    provider: int, id: str, session: SessionDep
) -> RecreationArea:
    """
    Get Recreation Area by ID
    """
    result = await session.execute(
        select(RecreationAreaDB).where(
            RecreationAreaDB.provider_id == provider,
            RecreationAreaDB.id == id,
        )
    )
    fetched = result.scalar_one_or_none()
    if fetched is None:
        raise ValueError("Recreation Area not found")
    return RecreationArea(
        id=fetched.id,
        provider_id=fetched.provider_id,
        name=fetched.name,
        description=fetched.description,
        country=fetched.country,
        state=fetched.state,
        longitude=fetched.longitude,
        latitude=fetched.latitude,
        reservable=fetched.reservable,
        enabled=fetched.enabled,
    )


@recreation_area_router.get("/{provider}/{id}/campgrounds")
async def list_campgrounds(
    provider: int, id: str, session: SessionDep
) -> list[Campground]:
    """
    List all Campgrounds for a Recreation Area
    """
    result = await session.execute(
        select(CampgroundDB).where(
            CampgroundDB.provider_id == provider, CampgroundDB.recreation_area_id == id
        )
    )
    campgrounds = result.scalars().all()
    return [
        Campground(
            id=c.id,
            provider_id=c.provider_id,
            recreation_area_id=c.recreation_area_id,
            name=c.name,
            description=c.description,
            country=c.country,
            state=c.state,
            longitude=c.longitude,
            latitude=c.latitude,
            reservable=c.reservable,
            enabled=c.enabled,
        )
        for c in campgrounds
    ]
