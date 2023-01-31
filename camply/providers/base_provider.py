"""
BaseProvider Base Class
"""

import logging
from abc import ABC
from datetime import datetime
from typing import List

from camply.config import SearchConfig

logger = logging.getLogger(__name__)


class BaseProvider(ABC):  # noqa: B024
    """
    Base Provider Class
    """

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


class ProviderError(Exception):
    """
    General Provider Error
    """


class ProviderSearchError(ProviderError):
    """
    Searching Error
    """
