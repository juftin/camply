"""
RecreationArea
"""

import datetime
from functools import partial
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.providers import Provider


class RecreationArea(Base):
    """
    Recreation Area Model
    """

    __tablename__ = "recreation_areas"

    id: Mapped[str] = mapped_column(
        String(128),
        primary_key=True,
        nullable=False,
    )
    provider_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("providers.id"), primary_key=True
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

    provider: Mapped["Provider"] = relationship(
        back_populates="recreation_areas",
    )
