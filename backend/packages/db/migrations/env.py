"""
Alembic Migration Environment Configuration
"""

import asyncio
import logging

from alembic import context
from alembic.config import Config
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import AsyncEngine

from db.config import db
from db.models import Base

config: Config = context.config
target_metadata = Base.metadata

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s]: %(message)s",
)


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    context.configure(
        url=db.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_migrations(connection: Connection) -> None:
    """
    Perform migrations using the provided connection.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online_async() -> None:
    """
    Run migrations in 'online' mode (Async).
    """
    engine: AsyncEngine = db.create_async_engine()
    async with engine.connect() as connection:
        await connection.run_sync(do_migrations)


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """
    asyncio.run(run_migrations_online_async())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
