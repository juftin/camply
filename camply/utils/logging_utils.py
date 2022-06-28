"""
Logging Utilities for Pushover Variables
"""

import logging
from typing import List, Union

from camply.containers import CampgroundFacility, RecreationArea

CALENDARMOJI = "📅"
CAMPMOJI = "🏕"
TENTMOJI = "⛺️"
XMOJI = "❌"

logger = logging.getLogger(__name__)


def _generate_response_string(
    response: Union[CampgroundFacility, RecreationArea, str]
) -> str:
    """
    Generate a formatted string for logging

    Parameters
    ----------
    response: Union[CampgroundFacility]

    Returns
    -------
    str
    """
    if isinstance(response, CampgroundFacility):
        if isinstance(response.facility_id, int):
            facil = f"#{response.facility_id}"
        else:
            facil = response.facility_id
        return (
            f"⛰  {response.recreation_area} (#{response.recreation_area_id}) - "
            f"🏕  {response.facility_name} ({facil})"
        )
    elif isinstance(response, RecreationArea):
        return (
            f"⛰  {response.recreation_area}, {response.recreation_area_location} "
            f"(#{response.recreation_area_id})"
        )
    elif isinstance(response, str):
        return response
    else:
        raise NotImplementedError


def log_sorted_response(response_array: List[object]) -> None:
    """
    Log Some Statements in a Nice Sorted way

    Parameters
    ----------
    response_array: List[str]

    Returns
    -------
    None
    """
    log_array = [_generate_response_string(obj) for obj in response_array]
    sorted_logs = sorted(log_array)
    for log_response in sorted_logs:
        logger.info(log_response)


def get_emoji(obj: list) -> str:
    """
    Return the Right Emoji

    Parameters
    ----------
    obj: list

    Returns
    -------
    str
    """
    assert isinstance(obj, list)
    if len(obj) >= 1:
        return TENTMOJI
    else:
        return XMOJI


def log_camply(self: logging.Logger, message: str, *args, **kwargs) -> None:
    """
    Custom Logging Notification Level for Pushover Logging

    Between logging.ERROR and logging.CRITICAL (45)

    Parameters
    ----------
    self: logging.Logger
    message: str
        Message String
    args
    kwargs

    Returns
    -------
    None
    """
    notification_level = logging.INFO + 1
    logging.addLevelName(level=notification_level, levelName="CAMPLY")
    if self.isEnabledFor(level=notification_level):
        self._log(level=notification_level, msg=message, args=args, **kwargs)
