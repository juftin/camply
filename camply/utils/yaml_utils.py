"""
YAML Utilities for Camply
"""

import logging
import os
from enum import Enum
from pathlib import Path
from re import compile
from typing import Any, Dict, Optional, Tuple

import yaml
from yaml import SafeLoader, load

from camply.containers.search_model import YamlSearchFile
from camply.utils import make_list
from camply.utils.general_utils import days_of_the_week_mapping, handle_search_windows

logger = logging.getLogger(__name__)


def read_yaml(path: Optional[str] = None):
    """
    Read a YAML File

    Load a yaml configuration file_path (path) or data object (data)
    and resolve any environment variables. The environment
    variables must be in this format to be parsed: ${VAR_NAME}.

    Parameters
    ----------
    path: Optional[str]
        File Path of YAML Object to Read

    Examples
    --------
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

    def env_var_constructor(safe_loader: yaml.Loader, node: Any) -> Any:
        """
        Extracts the environment variable from the node's value

        Parameters
        ----------
        safe_loader: yaml.Loader
        node: Any
            The current node in the yaml

        Returns
        -------
        Any
            the parsed string that contains the value of the environment variable
        """
        value = safe_loader.construct_scalar(node=node)
        match = pattern.findall(string=value)
        if match:
            full_value = value
            for item in match:
                full_value = full_value.replace(
                    "${{{key}}}".format(key=item), os.getenv(key=item, default=item)
                )
            return full_value
        return value

    safe_loader.add_constructor(tag=None, constructor=env_var_constructor)
    with open(path) as conf_data:
        return load(stream=conf_data, Loader=safe_loader)


def yaml_file_to_arguments(
    file_path: str,
) -> Tuple[str, Dict[str, object], Dict[str, object]]:
    """
    Convert YAML File into A Dictionary to be used as **kwargs

    Parameters
    ----------
    file_path: str
        File Path to YAML

    Returns
    -------
    Tuple[str, Dict[str, object], Dict[str, object]]
        Tuple containing provider string, provider **kwargs, and search **kwargs
    """
    yaml_search = read_yaml(path=file_path)
    logger.info(f"YAML File Parsed: {Path(file_path).name}")
    yaml_model = YamlSearchFile(**yaml_search)
    if isinstance(yaml_model.provider, Enum):
        provider = yaml_model.provider.value
    else:
        provider = yaml_model.provider
    search_window = handle_search_windows(
        start_date=yaml_model.start_date, end_date=yaml_model.end_date
    )
    days_of_the_week = yaml_model.days
    if days_of_the_week is not None:
        lower_mapping = {
            key.lower(): value for key, value in days_of_the_week_mapping.items()
        }
        days_of_the_week = [lower_mapping[item.lower()] for item in days_of_the_week]
    equipment = make_list(yaml_model.equipment)
    if isinstance(equipment, list):
        equipment = [tuple(equip) for equip in equipment]
    provider_kwargs = {
        "search_window": search_window,
        "recreation_area": yaml_model.recreation_area,
        "campgrounds": yaml_model.campgrounds,
        "campsites": yaml_model.campsites,
        "weekends_only": yaml_model.weekends,
        "days_of_the_week": days_of_the_week,
        "nights": yaml_model.nights,
        "equipment": equipment,
        "offline_search": yaml_model.offline_search,
        "offline_search_path": yaml_model.offline_search_path,
    }
    search_kwargs = {
        "log": True,
        "verbose": True,
        "continuous": yaml_model.continuous,
        "polling_interval": yaml_model.polling_interval,
        "notify_first_try": yaml_model.notify_first_try,
        "notification_provider": yaml_model.notifications,
        "search_forever": yaml_model.search_forever,
        "search_once": yaml_model.search_once,
    }
    return provider, provider_kwargs, search_kwargs
