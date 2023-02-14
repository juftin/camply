"""
Dynamic Logging Configuration
"""

import logging
from os import getenv
from typing import Optional, Tuple, Union

from rich.logging import RichHandler

LOG_HANDLER = getenv("CAMPLY_LOG_HANDLER", "rich").lower()


def get_log_handler(
    log_level: Optional[int] = None,
) -> Tuple[logging.Handler, Union[int, str]]:
    """
    Determine which logging handler should be used

    Parameters
    ----------
    log_level: Optional[int]
        Which logging level should be used. If none is provided the LOG_LEVEL environment
        variable will be used, defaulting to "INFO".

    Returns
    -------
    Tuple[logging.Handler, Union[int, str]]
    """
    if log_level is None:
        log_level = logging.getLevelName(getenv("LOG_LEVEL", "INFO").upper())
    rich_handler = RichHandler(
        level=log_level,
        rich_tracebacks=True,
        omit_repeated_times=False,
        show_path=False,
    )
    python_handler = logging.StreamHandler()
    python_formatter = logging.Formatter("%(asctime)s [%(levelname)8s]: %(message)s")
    python_handler.setFormatter(python_formatter)
    python_handler.setLevel(log_level)
    _log_dict = {
        "rich": rich_handler,
        "python": python_handler,
    }
    if getenv("PYTEST_CURRENT_TEST", None) is not None:
        handler = "python"
    else:
        handler = LOG_HANDLER
    log_handler: logging.Handler = _log_dict.get(handler, rich_handler)
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
    log_handler, level_to_log = get_log_handler(log_level=log_level)
    logging.root.handlers = [log_handler]
    if isinstance(log_handler, RichHandler):
        rich_formatter = logging.Formatter(
            datefmt="[%Y-%m-%d %H:%M:%S]", fmt="%(message)s"
        )
        logging.root.handlers[0].setFormatter(rich_formatter)
        level_to_log = logging.NOTSET
    logging.root.setLevel(level_to_log)
