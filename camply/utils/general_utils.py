#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
General Utilities
"""

import logging
from os import getenv
from re import compile
from typing import List, Optional

from yaml import load, SafeLoader

from camply.containers import AvailableCampsite, CampgroundFacility, RecreationArea, SearchWindow

logger = logging.getLogger(__name__)


def make_list(obj) -> Optional[List]:
    """
    Make Anything An Iterable Instance

    Parameters
    ----------
    obj: object

    Returns
    -------
    List[object]
    """
    if obj is None:
        return None
    elif isinstance(obj, (SearchWindow, AvailableCampsite, RecreationArea, CampgroundFacility)):
        return [obj]
    elif isinstance(obj, (set, list, tuple)):
        return obj
    else:
        return [obj]


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
            for g in match:
                full_value = full_value.replace(
                    "${{{key}}}".format(key=g), getenv(key=g, default=g))
            return full_value
        return value

    safe_loader.add_constructor(tag=None, constructor=env_var_constructor)
    with open(path) as conf_data:
        return load(stream=conf_data, Loader=safe_loader)
