"""
Populate Database CLI
"""

import asyncio

import click
import rich.traceback

from providers.recreation_gov.provider import RecreationGovProvider

rich.traceback.install(
    show_locals=False,
    suppress=[click, asyncio],
)


@click.command
def populate_database() -> None:
    """
    Populate the Database with Provider Data
    """
    provider = RecreationGovProvider()
    asyncio.run(provider.populate_database())


if __name__ == "__main__":
    populate_database()
