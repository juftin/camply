"""
Data Models for Upstream Recreation.gov Provider
"""

import datetime

import structlog
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import RecreationArea
from providers.base import DatabasePopulator

logger = structlog.getLogger(__name__)


class RecDotGovRecreationArea(BaseModel):
    """
    Model representing a recreation area from Recreation.gov.
    """

    RecAreaID: int | str
    OrgRecAreaID: int | str | None
    ParentOrgID: int | str | None
    RecAreaName: str
    RecAreaDescription: str
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
        async with session.begin():
            logger.info(
                "%s recreation areas to process",
                len(self.RECDATA),
                provider="Recreation.gov",
            )
            for area in self.RECDATA:
                recreation_area = RecreationArea(
                    id=area.RecAreaID,
                    provider_id=1,
                    name=area.RecAreaName,
                    description=area.RecAreaDescription,
                    longitude=area.RecAreaLongitude,
                    latitude=area.RecAreaLatitude,
                    reservable=area.Reservable,
                    enabled=area.Enabled,
                )
                await session.merge(recreation_area)
            await session.commit()
