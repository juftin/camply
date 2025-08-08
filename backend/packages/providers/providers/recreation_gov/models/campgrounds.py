"""
Data Models for Upstream Recreation.gov Provider
"""

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Campground, RecreationArea
from providers.base import DatabasePopulator, NullHandler
from providers.recreation_gov import PROVIDER

logger = structlog.getLogger(__name__)


class RecDotGovCampground(NullHandler):
    """
    Model representing a recreation area from Recreation.gov.
    """

    FacilityID: int | str
    ParentRecAreaID: int | str | None
    FacilityName: str | None
    FacilityDescription: str | None
    FacilityTypeDescription: str
    FacilityLongitude: float
    FacilityLatitude: float
    Reservable: bool
    Enabled: bool


class RecDotGovCampgroundData(DatabasePopulator):
    """
    Root model for a list of campgrounds.
    """

    RECDATA: list[RecDotGovCampground]

    async def to_database(self, session: AsyncSession) -> None:
        """
        Convert the data to database entries.
        """
        provider_id = 1
        sync_count = 0
        async with session.begin():
            logger.info(
                "%s campgrounds detected",
                len(self.RECDATA),
                provider=PROVIDER,
            )
            id_query = select(RecreationArea.id).where(
                RecreationArea.provider_id == provider_id
            )
            id_result = await session.execute(id_query)
            existing_recreation_area_ids = set(id_result.scalars())
            for camp in self.RECDATA:
                campground = Campground(
                    id=camp.FacilityID,
                    recreation_area_id=camp.ParentRecAreaID,
                    provider_id=provider_id,
                    name=camp.FacilityName,
                    description=camp.FacilityDescription,
                    longitude=camp.FacilityLongitude,
                    latitude=camp.FacilityLatitude,
                    reservable=camp.Reservable,
                    enabled=camp.Enabled,
                )
                if not camp.FacilityName:
                    continue
                elif camp.ParentRecAreaID not in existing_recreation_area_ids:
                    continue
                await session.merge(campground)
                sync_count += 1
            logger.info(
                "%s campgrounds processed",
                sync_count,
                provider=PROVIDER,
            )
            await session.commit()
