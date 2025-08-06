"""
Camply Providers
"""

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.base import Base

if TYPE_CHECKING:
    from db.models.recreation_area import RecreationArea


class Provider(Base):
    """
    Camply Provider Model
    """

    __tablename__ = "providers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255))
    url: Mapped[str] = mapped_column(String(255))
    enabled: Mapped[bool] = mapped_column(default=True)

    recreation_areas: Mapped[list["RecreationArea"]] = relationship(
        back_populates="provider",
    )
