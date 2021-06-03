#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
YAML Utilities for Camply
"""

from datetime import datetime
import logging
import os
from pathlib import Path
from re import compile
from typing import Dict, Tuple

from yaml import load, SafeLoader

from camply.config import SearchConfig
from camply.containers import SearchWindow

logger = logging.getLogger(__name__)


def read_yml(path: str = None):
    """
    Load a yaml configuration file_path (path) or data object (data)
    and resolve any environment variables. The environment
    variables must be in this format to be parsed: ${VAR_NAME}.
    Parameters
    ----------
    path: str
        File Path of YAML Object to Read

    Examples
    ----------
    database:
        host: ${HOST}
        port: ${PORT}
        ${KEY}: ${VALUE}
    app:
        log_path: "/var/${LOG_PATH}"
        something_else: "${AWESOME_ENV_VAR}/var/${A_SECOND_AWESOME_VAR}"
    """
    path = os.path.abspath(path)
    pattern = compile(r".*?\${(\w+)}.*?")

    safe_loader = SafeLoader
    safe_loader.add_implicit_resolver(tag=None, regexp=pattern, first=None)

    def env_var_constructor(safe_loader: object, node: object):
        """
        Extracts the environment variable from the node's value
        :param yaml.Loader safe_loader: the yaml loader
        :param node: the current node in the yaml
        :return: the parsed string that contains the value of the environment
        variable
        """
        value = safe_loader.construct_scalar(node=node)
        match = pattern.findall(string=value)
        if match:
            full_value = value
            for item in match:
                full_value = full_value.replace(
                    "${{{key}}}".format(key=item), os.getenv(key=item, default=item))
            return full_value
        return value

    safe_loader.add_constructor(tag=None, constructor=env_var_constructor)
    with open(path) as conf_data:
        return load(stream=conf_data, Loader=safe_loader)


def yaml_file_to_arguments(file_path: str) -> Tuple[str, Dict[str, object], Dict[str, object]]:
    """
    Convert YAML File into A Dictionary to be used as **kwargs

    Parameters
    ----------
    file_path: str
        File Path to YAML

    Returns
    -------
    provider, provider_kwargs, search_kwargs: Tuple[str, Dict[str, object], Dict[str, object]]
        Tuple containing provider string, provider **kwargs, and search **kwargs
    """
    yaml_search = read_yml(path=file_path)
    logger.info(f"YML File Parsed: {Path(file_path).name}")
    provider = yaml_search.get("provider", "RecreationDotGov")
    start_date = datetime.strptime(str(yaml_search["start_date"]), "%Y-%m-%d")
    end_date = datetime.strptime(str(yaml_search["end_date"]), "%Y-%m-%d")
    recreation_area = yaml_search.get("recreation_area", None)
    campgrounds = yaml_search.get("campgrounds", None)
    weekends_only = yaml_search.get("weekends", False)
    continuous = yaml_search.get("continuous", True)
    polling_interval = yaml_search.get("polling_interval",
                                       SearchConfig.RECOMMENDED_POLLING_INTERVAL)
    notify_first_try = yaml_search.get("notify_first_try", False)
    notification_provider = yaml_search.get("notifications", "silent")
    search_forever = yaml_search.get("search_forever", False)

    search_window = SearchWindow(start_date=start_date, end_date=end_date)

    provider_kwargs = dict(search_window=search_window,
                           recreation_area=recreation_area,
                           campgrounds=campgrounds,
                           weekends_only=weekends_only)
    search_kwargs = dict(
        log=True, verbose=True,
        continuous=continuous,
        polling_interval=polling_interval,
        notify_first_try=notify_first_try,
        notification_provider=notification_provider,
        search_forever=search_forever)
    return provider, provider_kwargs, search_kwargs
