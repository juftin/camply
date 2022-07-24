"""
Dynamic Logging Configuration
"""

import logging
import os
from os import getenv
from typing import Optional

from rich.logging import RichHandler


def get_log_handler(log_level: Optional[int] = None) -> logging.Handler:
    """
    Determine which logging handler should be used

    Parameters
    ----------
    log_level: Optional[int]
        Which logging level should be used. If none is provided the LOG_LEVEL environment
        variable will be used, defaulting to "INFO".

    Returns
    -------
    logging.Handler
    """
    if log_level is None:
        log_level = logging.getLevelName(getenv("LOG_LEVEL", "INFO").upper())

    rich_handler = RichHandler(
        level=log_level,
        rich_tracebacks=True,
        omit_repeated_times=False,
        show_path=False,
    )

    standard_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s [%(levelname)8s]: %(message)s")
    standard_handler.setFormatter(formatter)
    standard_handler.setLevel(log_level)

    _log_dict = {
        "rich": rich_handler,
        "python": standard_handler,
    }
    log_handler_name = os.getenv("CAMPLY_LOG_HANDLER", "rich")
    log_handler = _log_dict.get(log_handler_name.lower(), rich_handler)
    return log_handler, log_level


def set_up_logging(log_level: Optional[int] = None) -> None:
    """
    Set Up a Root Logger

    Parameters
    ----------
    log_level: Optional[int]
        Which logging level should be used. If none is provided the LOG_LEVEL environment
        variable will be used, defaulting to "INFO".
    """
    kwargs = {}
    log_handler, handler_level = get_log_handler(log_level=log_level)
    if isinstance(log_handler, RichHandler):
        kwargs["datefmt"] = "[%Y-%m-%d %H:%M:%S]"
        kwargs["format"] = "%(message)s"
        level = logging.NOTSET
    else:
        level = handler_level
    logging.basicConfig(
        level=level,
        handlers=[
            log_handler,
        ],
        **kwargs,
    )
