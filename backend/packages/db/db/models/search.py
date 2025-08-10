"""
Search
"""

from typing import Self

from sqlalchemy import (
    Integer,
    String,
    case,
    or_,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
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

    @classmethod
    async def algorithm(
        cls, session: AsyncSession, term: str, *, limit: int = 25
    ) -> list[Self]:
        """
        Search the Search table given a search term.
        """
        term_lc = term.lower()
        # -------------- SEARCH TERM PREPARATION --------------
        exact = term_lc
        prefix = f"{term_lc}%"
        substring = f"%{term_lc}%"
        # -------------- MATCH QUALITY SCORE --------------
        match_score = case(
            (cls.recreation_area_name == exact, 100),
            (cls.campground_name == exact, 100),
            (cls.recreation_area_name.like(prefix), 75),
            (cls.campground_name.like(prefix), 75),
            (cls.recreation_area_name.like(substring), 50),
            (cls.campground_name.like(substring), 50),
            else_=0,
            value=None,
        ).label("match_score")

        # -------------- ENTITY TYPE SCORE --------------
        entity_score = case(
            (cls.entity_type == "RecreationArea", 100),
            (cls.entity_type == "Campground", 50),
            else_=0,
        ).label("entity_score")
        total_score = (entity_score + match_score).label("total_score")
        # -------------- FINAL STATEMENT --------------
        stmt = (
            select(cls, total_score)
            .where(
                or_(
                    cls.recreation_area_name.like(substring),
                    cls.campground_name.like(substring),
                )
            )
            .order_by(
                total_score.desc(), cls.provider_name
            )
            .limit(limit)
        )
        # -------------- EXECUTE STATEMENT --------------
        result = await session.execute(stmt)
        rows: list[Self] = result.scalars().all()  # type: ignore[assignment]
        return rows
