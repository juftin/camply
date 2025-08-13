"""
Data Models for Upstream Recreation.gov Provider
"""

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.data.providers import RecreationDotGov
from db.models import Campground, RecreationArea
from providers.base import NullHandler
from providers.recreation_gov.models.address import AddressPopulator

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


class RecDotGovCampgroundData(AddressPopulator):
    """
    Root model for a list of campgrounds.
    """

    RECDATA: list[RecDotGovCampground]

    async def to_database(self, session: AsyncSession) -> None:
        """
        Convert the data to database entries.
        """
        sync_count = 0
        async with session.begin():
            logger.info(
                "%s facilities detected",
                len(self.RECDATA),
                provider=RecreationDotGov.name,
            )
            id_query = select(RecreationArea.id).where(
                RecreationArea.provider_id == RecreationDotGov.id
            )
            id_result = await session.execute(id_query)
            existing_recreation_area_ids = set(id_result.scalars())
            for camp in self.RECDATA:
                if camp.FacilityTypeDescription != "Campground":
                    continue
                country = None
                city = None
                state = None
                address = self.ADDRESSES.get(camp.FacilityID)
                if address:
                    city = address.City
                    state = address.AddressStateCode
                    country = address.AddressCountryCode
                campground = Campground(
                    id=camp.FacilityID,
                    recreation_area_id=camp.ParentRecAreaID,
                    provider_id=RecreationDotGov.id,
                    name=camp.FacilityName,
                    description=camp.FacilityDescription,
                    city=city,
                    state=state,
                    country=country,
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
                provider=RecreationDotGov.name,
            )
            await session.commit()
