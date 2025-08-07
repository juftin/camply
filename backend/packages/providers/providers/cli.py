"""
Populate Database CLI
"""

import asyncio

from click import command

from providers.recreation_gov.provider import RecreationGovProvider


@command
def populate_database() -> None:
    """
    Populate the Database with Provider Data
    """
    provider = RecreationGovProvider()
    asyncio.run(provider.populate_database())


if __name__ == "__main__":
    populate_database()
