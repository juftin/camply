"""
Search
"""

from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base

if TYPE_CHECKING:
    pass


class Search(Base):
    """
    Campground Model
    """

    __tablename__ = "search"

    entity_type: Mapped[str] = mapped_column(
        String(128),
    )
    provider_name: Mapped[str] = mapped_column(
        String(128),
    )
    recreation_area_name: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )
    recreation_area_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )
    campground_name: Mapped[str] = mapped_column(
        String(128),
        index=True,
    )
    campground_id: Mapped[str] = mapped_column(
        String(128),
    )
