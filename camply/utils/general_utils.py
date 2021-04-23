#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
General Utilities
"""

import logging
from typing import List

from camply.containers import AvailableCampsite, CampgroundFacility, RecreationArea, SearchWindow

logger = logging.getLogger(__name__)


def make_list(obj) -> List:
    """
    Make Anything An Iterable Instance

    Parameters
    ----------
    obj

    Returns
    -------

    """
    if obj is None:
        return None
    elif isinstance(obj, (SearchWindow, AvailableCampsite, RecreationArea, CampgroundFacility)):
        return [obj]
    elif isinstance(obj, (set, list, tuple)):
        return obj
    # elif isinstance(obj, str):
    #     return [obj]
    else:
        return [obj]
