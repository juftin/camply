"""
Data Models for Upstream Recreation.gov Provider
"""

import datetime

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from db.data.providers import RecreationDotGov
from db.models import RecreationArea
from providers.base import NullHandler
from providers.recreation_gov.models.address import AddressPopulator

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


class RecDotGovRecreationAreaData(AddressPopulator):
    """
    Root model for a list of recreation areas.
    """

    RECDATA: list[RecDotGovRecreationArea]

    async def to_database(self, session: AsyncSession) -> None:
        """
        Convert the data to database entries.
        """
        sync_count = 0
        async with session.begin():
            logger.info(
                "%s recreation areas detected",
                len(self.RECDATA),
                provider=RecreationDotGov.name,
            )
            for area in self.RECDATA:
                country = None
                city = None
                state = None
                address = self.ADDRESSES.get(area.RecAreaID)
                if address:
                    city = address.City
                    # TODO(@juftin): Resolve this once Recreation.gov fixes their API
                    state = address.PostalCode
                    country = address.AddressCountryCode
                recreation_area = RecreationArea(
                    id=area.RecAreaID,
                    provider_id=RecreationDotGov.id,
                    name=area.RecAreaName,
                    description=area.RecAreaDescription,
                    city=city,
                    state=state,
                    country=country,
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
                provider=RecreationDotGov.name,
            )
            await session.commit()
