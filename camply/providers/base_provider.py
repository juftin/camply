"""
BaseProvider Base Class
"""

import logging
from abc import ABC

logger = logging.getLogger(__name__)


class BaseProvider(ABC):
    """
    Base Provider Class
    """


class ProviderError(Exception):
    """
    General Provider Error
    """


class ProviderSearchError(ProviderError):
    """
    Searching Error
    """
