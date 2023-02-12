"""
BaseProvider Base Class
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

import requests
from fake_useragent import UserAgent

from camply.config import SearchConfig
from camply.containers import CampgroundFacility

logger = logging.getLogger(__name__)


class BaseProvider(ABC):
    """
    Base Provider Class
    """

    def __init__(self):
        """
        Initialize with a session
        """
        _user_agent = UserAgent(use_external_data=False, browsers=["chrome"]).chrome
        self.session = requests.Session()
        self.headers = {"User-Agent": _user_agent}
        self.session.headers = self.headers
        self.json_headers = self.headers.copy()
        self.json_headers.update({"Content-Type": "application/json"})

    @classmethod
    def get_search_months(cls, search_days) -> List[datetime]:
        """
        Get the Unique Months that need to be Searched

        Returns
        -------
        search_months: List[datetime]
            Datetime Months to search for reservations
        """
        truncated_months = {day.replace(day=1) for day in search_days}
        if len(truncated_months) > 1:
            logger.info(
                f"{len(truncated_months)} different months selected for search, "
                f"ranging from {min(search_days)} to {max(search_days)}"
            )
            return sorted(truncated_months)
        elif len(truncated_months) == 0:
            logger.info(SearchConfig.ERROR_MESSAGE)
            raise RuntimeError(SearchConfig.ERROR_MESSAGE)
        else:
            return sorted(truncated_months)

    @abstractmethod
    def find_campgrounds(self) -> List[CampgroundFacility]:
        """
        List Recreation Areas for the provider
        """


class ProviderError(Exception):
    """
    General Provider Error
    """


class ProviderSearchError(ProviderError):
    """
    Searching Error
    """
