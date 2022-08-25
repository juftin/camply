"""
BaseProvider Base Class
"""

import logging

logger = logging.getLogger(__name__)


class BaseProvider:
    """
    Base Provider Class

    This should ideally be an AbstractBaseClass
    """


class ProviderError(Exception):
    """
    General Provider Error
    """


class ProviderSearchError(ProviderError):
    """
    Searching Error
    """
