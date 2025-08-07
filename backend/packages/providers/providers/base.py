"""
Base Provider Configuration
"""

from abc import ABC, abstractmethod

import httpx
from pydantic import BaseModel
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


class DatabasePopulator(ABC, BaseModel):
    """
    Class that supports populating the database with data.
    """

    @abstractmethod
    async def to_database(self, session: AsyncSession) -> None:
        """
        Populate the database with the data.
        """
