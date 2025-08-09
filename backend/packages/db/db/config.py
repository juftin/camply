"""
Database Connections
"""

from enum import Enum
from typing import Any, AsyncGenerator, ClassVar

import sqlalchemy.engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseDrivers(str, Enum):
    """
    Database drivers
    """

    POSTGRES = "postgresql+psycopg"


class DatabaseConfig(BaseSettings):
    """
    Database Configuration
    """

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="CAMPLY_DB_",
        case_sensitive=False,
    )

    DRIVERNAME: DatabaseDrivers = DatabaseDrivers.POSTGRES
    USERNAME: str = "camply"
    PASSWORD: str = "camply"
    HOST: str = "localhost"
    PORT: int = 5432
    DATABASE: str = "camply"

    @property
    def url(self) -> sqlalchemy.engine.URL:
        """
        Get the database URL
        """
        return sqlalchemy.engine.URL.create(
            drivername=str(self.DRIVERNAME.value),
            username=self.USERNAME,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT,
            database=self.DATABASE,
        )

    def create_async_engine(self, **kwargs: Any) -> AsyncEngine:
        """
        Get the SQLAlchemy engine
        """
        return create_async_engine(
            self.url,
            **kwargs,
        )

    def get_session_maker(self, **kwargs: Any) -> async_sessionmaker[AsyncSession]:
        """
        Get an async session maker for the database
        """
        return async_sessionmaker(
            self.create_async_engine(**kwargs),
            class_=AsyncSession,
            autocommit=False,
            expire_on_commit=False,
            autoflush=False,
        )

    def get_session(self, **kwargs: Any) -> AsyncSession:
        """
        Get an async session for the database
        """
        async_session_maker = self.get_session_maker(**kwargs)
        return async_session_maker()

    async def yield_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Yield an async session for the database
        """
        async with self.get_session() as session:
            yield session


db = DatabaseConfig()
