"""
Camply General Utilities
"""

import logging
import sys
from datetime import date
from typing import Any, Callable, Iterable, List, Optional, Union

from camply import SearchWindow
from camply.containers.base_container import CamplyModel

logger = logging.getLogger(__name__)


def make_list(obj, coerce: Optional[Callable] = None) -> Optional[List[Any]]:
    """
    Make Anything An Iterable Instance

    Parameters
    ----------
    obj: object
    coerce: Callable

    Returns
    -------
    List[object]
    """
    if obj is None:
        return None
    elif isinstance(obj, CamplyModel):
        return [coerce(obj) if coerce is not None else obj]
    elif isinstance(obj, (set, list, tuple)):
        if coerce is True:
            return [coerce(item) for item in obj]
        else:
            return list(obj)
    else:
        return [coerce(obj) if coerce is not None else obj]


def handle_search_windows(
    start_date: Union[Iterable[str], str], end_date: Union[Iterable[str], str]
) -> Union[List[SearchWindow], SearchWindow]:
    """
    Handle Multiple Search Windows by the CLI
    """
    if isinstance(start_date, (str, date)):
        start_date = (start_date,)
        assert isinstance(end_date, (str, date))
        end_date = (end_date,)
    search_windows: List[SearchWindow] = []
    for field in [start_date, end_date]:
        if field is None or (isinstance(field, (tuple, list)) and len(field) == 0):
            logger.error("Campsite searches require a `start_date` and an `end_date`")
            sys.exit(1)
    if len(start_date) != len(end_date):
        logger.error(
            "When searching multiple date windows, you must provide the same amount "
            "of `--start-dates` as `--end-dates`"
        )
        sys.exit(1)
    for index, date_str in enumerate(start_date):
        search_windows.append(
            SearchWindow(start_date=date_str, end_date=end_date[index])
        )
    if len(search_windows) == 1:
        return search_windows[0]
    else:
        return search_windows


days_of_the_week_base = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6,
}
days_of_the_week_mapping = days_of_the_week_base.copy()
days_of_the_week_mapping.update(
    {
        "MON": 0,
        "TUE": 1,
        "TUES": 1,
        "WED": 2,
        "THU": 3,
        "THUR": 3,
        "THURS": 3,
        "FRI": 4,
        "SAT": 5,
        "SUN": 6,
    }
)
