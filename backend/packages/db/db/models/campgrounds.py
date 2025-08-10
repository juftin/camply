"""
Campground
"""

import datetime
from functools import partial
from typing import TYPE_CHECKING, Optional

from sqlalchemy import (
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.providers import Provider
    from db.models.recreation_area import RecreationArea


class Campground(Base):
    """
    Campground Model
    """

    __tablename__ = "campgrounds"

    id: Mapped[str] = mapped_column(
        String(128),
        primary_key=True,
    )
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("providers.id"), primary_key=True
    )
    recreation_area_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(String(32768))
    country: Mapped[str | None] = mapped_column(String(50))
    state: Mapped[str | None] = mapped_column(String(50))
    longitude: Mapped[float | None] = mapped_column()
    latitude: Mapped[float | None] = mapped_column()
    reservable: Mapped[bool] = mapped_column(default=True)
    enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc),
        server_default=func.CURRENT_TIMESTAMP(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        default=partial(datetime.datetime.now, tz=datetime.timezone.utc),
        server_default=func.CURRENT_TIMESTAMP(),
        onupdate=func.CURRENT_TIMESTAMP(),
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["recreation_area_id", "provider_id"],
            ["recreation_areas.id", "recreation_areas.provider_id"],
        ),
    )

    provider: Mapped["Provider"] = relationship(
        "Provider",
        foreign_keys=[provider_id],
    )
    recreation_area: Mapped[Optional["RecreationArea"]] = relationship(
        "RecreationArea",
        foreign_keys=[recreation_area_id, provider_id],
        viewonly=True,
    )
