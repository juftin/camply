"""
Reserve America Web Searching Utilities
"""

import logging
from abc import ABC
from datetime import datetime
from typing import Union

# TODO: Update ReserveAmericaConfig as needed
# TODO: Add and create other classes as needed
from camply.providers.base_provider import BaseProvider

logger = logging.getLogger(__name__)


class ReserveAmerica(BaseProvider, ABC):
    """
    Python Class for Reserve America Web Searching
    """

    def __init__(self):
        """
        Initialize the ReserveAmericaBase class.
        """
        super().__init__()
        # TODO: Initialize session/cookies

    def get_reserveamerica_data(
        self, campground_id: int, month: datetime
    ) -> Union[dict, list]:
        """
        Find Campsite Availability Data

        Parameters
        ----------
        campground_id: int
            Campground ID pulled off URLs on ReserveAmerica.com
        month: datetime
            datetime object, results will be filtered to month

        Returns
        -------
        Union[dict, list]
        """

    # TODO return availability, see search_reserveamerica.py for more details
