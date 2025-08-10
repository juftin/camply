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
            (cls.recreation_area_name == exact, 0),
            (cls.campground_name == exact, 0),
            (cls.recreation_area_name.like(prefix), 1),
            (cls.campground_name.like(prefix), 1),
            (cls.recreation_area_name.like(substring), 2),
            (cls.campground_name.like(substring), 2),
            else_=3,  # safety net
            value=None,
        ).label("match_score")

        # -------------- ENTITY TYPE SCORE --------------
        entity_score = case(
            (cls.entity_type == "RecreationArea", 0),
            (cls.entity_type == "Campground", 5),
            else_=10,
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
            .order_by(total_score, cls.provider_name)  # deterministic tie-break
            .limit(limit)
        )
        # -------------- EXECUTE STATEMENT --------------
        result = await session.execute(stmt)
        raise ValueError(result)
        rows = result.scalars().unique().all()
        return rows
