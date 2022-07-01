"""
Dynamic Logging Configuration
"""

import logging
import os
from os import getenv

from rich.logging import RichHandler

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


def set_up_logging() -> None:
    """
    Set Up a Root Logger
    """
    kwargs = {}
    if isinstance(log_handler, RichHandler):
        kwargs["datefmt"] = "[%Y-%m-%d %H:%M:%S]"
        kwargs["format"] = "%(message)s"
        level = logging.NOTSET
    else:
        level = log_level
    logging.basicConfig(
        level=level,
        handlers=[
            log_handler,
        ],
        **kwargs,
    )
