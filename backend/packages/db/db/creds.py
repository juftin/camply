"""
Database Connections
"""

from enum import Enum
from pathlib import Path
from typing import Any, Optional

import platformdirs
import sqlalchemy.engine
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


class DatabaseDrivers(str, Enum):
    """
    Database drivers
    """

    SQLITE = "sqlite+aiosqlite"


DEFAULT_SQLITE_FILE = Path(platformdirs.user_data_dir(appname="camply")) / "camply.db"


class DatabaseCredentials(BaseSettings):
    """
    Database credentials
    """

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_prefix="CAMPLY_DB_",
        case_sensitive=False,
    )

    DRIVERNAME: DatabaseDrivers = DatabaseDrivers.SQLITE
    USERNAME: str = "camply"
    PASSWORD: Optional[str] = None
    HOST: Optional[str] = f"/{DEFAULT_SQLITE_FILE}"
    PORT: Optional[int] = None
    DATABASE: str = "camply"

    @property
    def url(self) -> sqlalchemy.engine.URL:
        """
        Get the database URL
        """
        return sqlalchemy.engine.URL.create(
            drivername=str(self.DRIVERNAME.value),
            username=(
                self.USERNAME if self.DRIVERNAME != DatabaseDrivers.SQLITE else None
            ),
            password=(
                self.PASSWORD if self.DRIVERNAME != DatabaseDrivers.SQLITE else None
            ),
            host=self.HOST,
            port=(self.PORT if self.DRIVERNAME != DatabaseDrivers.SQLITE else None),
            database=(
                self.DATABASE if self.DRIVERNAME != DatabaseDrivers.SQLITE else None
            ),
        )

    def create_async_engine(self, **kwargs: Any) -> AsyncEngine:
        """
        Get the SQLAlchemy engine
        """
        if self.DRIVERNAME == DatabaseDrivers.SQLITE:
            sqlite_file = Path(self.HOST.replace("//", "/"))
            sqlite_file.parent.mkdir(parents=True, exist_ok=True)
        return create_async_engine(
            str(self.url),
            **kwargs,
        )
