"""
API Dependencies
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.config import db

SessionDep = Annotated[AsyncSession, Depends(db.yield_session)]
