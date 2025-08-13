"""
Providers
"""

from db.data.providers import RecreationDotGov
from providers.base import BaseProvider
from providers.recreation_gov.provider import RecreationGovProvider

PROVIDERS: dict[int, type[BaseProvider]] = {
    RecreationDotGov.id: RecreationGovProvider,
}

__all__ = ["PROVIDERS"]
