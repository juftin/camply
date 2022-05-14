"""
BaseProvider Base Class
"""

from abc import ABC
import logging

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
