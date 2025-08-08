"""
Base Provider Configuration
"""

from abc import ABC, abstractmethod

import httpx
from pydantic import BaseModel, field_validator
from sqlalchemy.ext.asyncio import AsyncSession


class BaseProvider(ABC):
    """
    Base Class for Providers
    """

    def __init__(self) -> None:
        """
        Initialize the base provider.
        """
        self.async_client = httpx.AsyncClient(headers=self.headers)

    @property
    def headers(self) -> dict[str, str]:
        """
        Headers for the provider requests.
        """
        return {}

    @abstractmethod
    async def populate_database(self) -> None:
        """
        Populate the database with data from the provider.
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
