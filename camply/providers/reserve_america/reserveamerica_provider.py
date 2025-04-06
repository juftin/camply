"""
Reserve America Web Searching Utilities
"""

import logging
from abc import ABC

# TODO: Update ReserveAmericaConfig as needed
# TODO: Add and create other classes as needed
from camply.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class ReserveAmericaBase(BaseProvider, ABC):
    """
    Python Class for Reserve America Web Searching
    """

    # TODO: Implement __init__ method
    # TODO: Implement find_campgrounds method
