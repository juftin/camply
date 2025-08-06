"""
RecreationArea
"""

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import UUID, BigInteger, Column, ForeignKey, String
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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        nullable=False,
        default=uuid.uuid4,
    )
    provider_id: Mapped[int] = Column(
        BigInteger, ForeignKey("providers.id"), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str | None] = mapped_column(String(255))
    county: Mapped[str | None] = mapped_column(String(50))
    state: Mapped[str | None] = mapped_column(String(50))
    longitude: Mapped[float | None] = mapped_column()
    latitude: Mapped[float | None] = mapped_column()

    provider: Mapped["Provider"] = relationship(
        back_populates="recreation_areas",
    )
