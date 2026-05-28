"""
Base Provider Configuration
"""

from abc import ABC, abstractmethod
from datetime import date

import httpx
import structlog
from pydantic import BaseModel, field_validator
from sqlalchemy import Insert, delete, insert, literal, null, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import concat

from db.models import Campground, Provider, RecreationArea, Search
from providers.dto import CampsiteDTO

logger = structlog.getLogger()


class BaseProvider(ABC):
    """
    Base Class for Providers
    """

    def __init__(self) -> None:
        """
        Initialize the base provider.
        """
        try:
            from fake_useragent import UserAgent

            self.user_agent = UserAgent(browsers=["chrome"]).random
        except Exception:
            self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        self.async_client = httpx.AsyncClient(headers=self.headers)

    @abstractmethod
    async def find_availabilities(
        self,
        park_id: str,
        start_date: date,
        end_date: date,
    ) -> list[CampsiteDTO]:
        """
        Find campsite availabilities for the target park and dates.
        """

    @abstractmethod
    async def sync_metadata(self) -> None:
        """
        Background task to update the 'Search' and 'Campground'
        tables with the latest info from the provider.
        """

    @property
    def headers(self) -> dict[str, str]:
        """
        Headers for the provider requests.
        """
        return {"User-Agent": self.user_agent}

    @abstractmethod
    async def populate_database(self) -> None:
        """
        Populate the database with data from the provider.
        """

    @property
    @abstractmethod
    def provider(self) -> Provider:
        """
        Return the provider instance.
        """

    @property
    def search_rec_area_statement(self) -> Insert:
        """
        SQL statement to search recreation areas.
        """
        rec_areas = insert(Search).from_select(
            names=[
                Search.id,
                Search.entity_type,
                Search.provider_id,
                Search.provider_name,
                Search.recreation_area_id,
                Search.recreation_area_name,
                Search.campground_id,
                Search.campground_name,
            ],
            select=select(
                concat(
                    "RecreationArea",
                    "/",
                    self.provider.id,
                    "/",
                    RecreationArea.id,
                    "/",
                ).label("id"),
                literal("RecreationArea").label("entity_type"),
                literal(self.provider.id).label("provider_id"),
                literal(self.provider.name).label("provider_name"),
                RecreationArea.id.label("recreation_area_id"),
                func.lower(RecreationArea.name).label("recreation_area_name"),
                null().label("campground_id"),
                null().label("campground_name"),
            ).where(RecreationArea.provider_id == self.provider.id),
        )
        return rec_areas

    @property
    def search_campground_statement(self) -> Insert:
        """
        SQL statement to search campgrounds.
        """
        campgrounds = insert(Search).from_select(
            names=[
                Search.id,
                Search.entity_type,
                Search.provider_id,
                Search.provider_name,
                Search.recreation_area_id,
                Search.recreation_area_name,
                Search.campground_id,
                Search.campground_name,
            ],
            select=select(
                concat(
                    "Campground",
                    "/",
                    self.provider.id,
                    "/",
                    RecreationArea.id,
                    "/",
                    Campground.id,
                ).label("id"),
                literal("Campground").label("entity_type"),
                literal(self.provider.id).label("provider_id"),
                literal(self.provider.name).label("provider_name"),
                RecreationArea.id.label("recreation_area_id"),
                func.lower(RecreationArea.name).label("recreation_area_name"),
                Campground.id.label("campground_id"),
                func.lower(Campground.name).label("campground_name"),
            )
            .select_from(
                Campground.__table__.outerjoin(
                    RecreationArea,
                    Campground.recreation_area_id == RecreationArea.id,
                )
            )
            .where(Campground.provider_id == self.provider.id),
        )
        return campgrounds

    async def populate_search_table(self, session: AsyncSession) -> None:
        """
        Populate the search table with campground and recreation area data.
        """
        logger.info(
            "Populating search table",
            provider=self.provider.name,
        )
        async with session.begin():
            await session.execute(
                delete(Search).where(Search.provider_name == self.provider.name)
            )
            await session.execute(self.search_rec_area_statement)
            await session.execute(self.search_campground_statement)
            await session.commit()

    @classmethod
    @abstractmethod
    def get_rec_area_url(cls, rec_area_id: str) -> str:
        """
        Get the URL for a recreation area.
        """

    @classmethod
    @abstractmethod
    def get_campground_url(cls, campground_id: str) -> str:
        """
        Get the URL for a campground.
        """


class NullHandler(BaseModel):
    """
    Empty String to Null Handler
    """

    @field_validator("*", mode="before")
    @classmethod
    def convert_to_none(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        else:
            return v


class DatabasePopulator(ABC, BaseModel):
    """
    Class that supports populating the database with data.
    """

    @abstractmethod
    async def to_database(self, session: AsyncSession) -> None:
        """
        Populate the database with the data.
        """
