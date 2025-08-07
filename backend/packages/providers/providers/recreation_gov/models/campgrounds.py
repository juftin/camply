"""
Data Models for Upstream Recreation.gov Provider
"""

import structlog
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Campground
from providers.base import DatabasePopulator

logger = structlog.getLogger(__name__)


class RecDotGovCampground(BaseModel):
    """
    Model representing a recreation area from Recreation.gov.
    """

    FacilityID: int | str
    ParentRecAreaID: int | str
    FacilityName: str
    FacilityDescription: str
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
        async with session.begin():
            logger.info(
                "%s campgrounds to process",
                len(self.RECDATA),
                provider="Recreation.gov",
            )
            for camp in self.RECDATA:
                campground = Campground(
                    id=camp.FacilityID,
                    recreation_area_id=camp.ParentRecAreaID,
                    name=camp.FacilityName,
                    description=camp.FacilityDescription,
                    longitude=camp.FacilityLongitude,
                    latitude=camp.FacilityLatitude,
                    reservable=camp.Reservable,
                    enabled=camp.Enabled,
                )
                await session.merge(campground)
            await session.commit()
