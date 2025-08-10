"""
Search
"""

from sqlalchemy import (
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class Search(Base):
    """
    Campground Model
    """

    __tablename__ = "search"

    id: Mapped[str] = mapped_column(
        String(128),
        primary_key=True,
    )
    entity_type: Mapped[str] = mapped_column(
        String(128),
    )
    provider_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    provider_name: Mapped[str] = mapped_column(
        String(128),
    )
    recreation_area_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )
    recreation_area_name: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )
    campground_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )
    campground_name: Mapped[str | None] = mapped_column(
        String(128),
        index=True,
        nullable=True,
    )
