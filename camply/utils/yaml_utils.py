"""
YAML Utilities for Camply
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from re import compile
from typing import Any, Dict, Tuple

import yaml
from yaml import SafeLoader, load

from camply.config import SearchConfig
from camply.containers import SearchWindow
from camply.utils import make_list

logger = logging.getLogger(__name__)


def read_yaml(path: str = None):
    """
    Read a YAML File

    Load a yaml configuration file_path (path) or data object (data)
    and resolve any environment variables. The environment
    variables must be in this format to be parsed: ${VAR_NAME}.

    Parameters
    ----------
    path: str
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
    provider, provider_kwargs, search_kwargs: Tuple[str, Dict[str, object], Dict[str, object]]
        Tuple containing provider string, provider **kwargs, and search **kwargs
    """
    yaml_search = read_yaml(path=file_path)
    logger.info(f"YAML File Parsed: {Path(file_path).name}")
    provider = yaml_search.get("provider", "RecreationDotGov")
    start_date = datetime.strptime(str(yaml_search["start_date"]), "%Y-%m-%d")
    end_date = datetime.strptime(str(yaml_search["end_date"]), "%Y-%m-%d")
    nights = int(yaml_search.get("nights", 1))
    recreation_area = yaml_search.get("recreation_area", None)
    campgrounds = yaml_search.get("campgrounds", None)
    campsites = yaml_search.get("campsites", None)
    weekends_only = yaml_search.get("weekends", False)
    continuous = yaml_search.get("continuous", True)
    polling_interval = yaml_search.get(
        "polling_interval", SearchConfig.RECOMMENDED_POLLING_INTERVAL
    )
    notify_first_try = yaml_search.get("notify_first_try", False)
    notification_provider = yaml_search.get("notifications", "silent")
    search_forever = yaml_search.get("search_forever", False)
    equipment = yaml_search.get("equipment", None)
    equipment = make_list(equipment)
    if isinstance(equipment, list):
        equipment = [tuple(equip) for equip in equipment]
    offline_search = yaml_search.get("offline_search", False)
    offline_search_path = yaml_search.get("offline_search_path", None)

    search_window = SearchWindow(start_date=start_date, end_date=end_date)

    provider_kwargs = dict(
        search_window=search_window,
        recreation_area=recreation_area,
        campgrounds=campgrounds,
        campsites=campsites,
        weekends_only=weekends_only,
        nights=nights,
        equipment=equipment,
        offline_search=offline_search,
        offline_search_path=offline_search_path,
    )
    search_kwargs = dict(
        log=True,
        verbose=True,
        continuous=continuous,
        polling_interval=polling_interval,
        notify_first_try=notify_first_try,
        notification_provider=notification_provider,
        search_forever=search_forever,
    )
    return provider, provider_kwargs, search_kwargs
