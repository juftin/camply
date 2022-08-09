"""
Camply General Utilities
"""

import logging
from typing import Callable, List, Optional

from camply.containers.base_container import CamplyModel

logger = logging.getLogger(__name__)


def make_list(obj, coerce: Optional[Callable] = None) -> Optional[List]:
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
