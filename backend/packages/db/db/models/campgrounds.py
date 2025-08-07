"""
Campground
"""

import datetime
from functools import partial
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.providers import RecreationArea


class Campground(Base):
    """
    Campground Model
    """

    __tablename__ = "campgrounds"

    id: Mapped[str] = mapped_column(
        String(128),
        primary_key=True,
        nullable=False,
    )
    recreation_area_id: Mapped[str] = mapped_column(
        String, ForeignKey("recreation_areas.id"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(String(255))
    county: Mapped[str | None] = mapped_column(String(50))
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

    recreation_area: Mapped["RecreationArea"] = relationship(
        back_populates="campgrounds",
    )
