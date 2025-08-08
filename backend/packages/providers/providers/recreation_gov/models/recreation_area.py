"""
Data Models for Upstream Recreation.gov Provider
"""

import datetime

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import RecreationArea
from providers.base import DatabasePopulator, NullHandler
from providers.recreation_gov import PROVIDER

logger = structlog.getLogger(__name__)


class RecDotGovRecreationArea(NullHandler):
    """
    Model representing a recreation area from Recreation.gov.
    """

    RecAreaID: int | str
    OrgRecAreaID: int | str | None
    ParentOrgID: int | str | None
    RecAreaName: str | None
    RecAreaDescription: str | None
    RecAreaLongitude: float
    RecAreaLatitude: float
    Reservable: bool
    Enabled: bool
    LastUpdatedDate: datetime.date


class RecDotGovRecreationAreaData(DatabasePopulator):
    """
    Root model for a list of recreation areas.
    """

    RECDATA: list[RecDotGovRecreationArea]

    async def to_database(self, session: AsyncSession) -> None:
        """
        Convert the data to database entries.
        """
        provider_id = 1
        sync_count = 0
        async with session.begin():
            logger.info(
                "%s recreation areas detected",
                len(self.RECDATA),
                provider=PROVIDER,
            )
            for area in self.RECDATA:
                recreation_area = RecreationArea(
                    id=area.RecAreaID,
                    provider_id=provider_id,
                    name=area.RecAreaName,
                    description=area.RecAreaDescription,
                    longitude=area.RecAreaLongitude,
                    latitude=area.RecAreaLatitude,
                    reservable=area.Reservable,
                    enabled=area.Enabled,
                )
                if not area.RecAreaName:
                    continue
                await session.merge(recreation_area)
                sync_count += 1
            logger.info(
                "%s recreation areas synced",
                sync_count,
                provider=PROVIDER,
            )
            await session.commit()
