"""
Recreation.gov Web Searching Utilities
"""

import logging
from typing import List, Union
from urllib import parse

logger = logging.getLogger(__name__)


def generate_url(
    scheme: str,
    netloc: str,
    path: str = "",
    params: str = "",
    query: str = "",
    fragment: str = "",
):
    """
    Build a URL

    Parameters
    ----------
    scheme: str
        URL scheme specifier
    netloc: str
        Network location part
    path: str
        Hierarchical path
    params: str
        Parameters for last path element
    query: str
        Query component
    fragment: str
        Fragment identifier

    Returns
    -------
    url: str
        Compiled URL
    """
    url_components = {
        "scheme": scheme,
        "netloc": netloc,
        "path": path,
        "params": params,
        "query": query,
        "fragment": fragment,
    }
    return parse.urlunparse(components=tuple(url_components.values()))


def filter_json(json: dict, filters: Union[str, List[str]]) -> object:
    """
    Extension Method to Dictionaries, allows easy filtering

    Parameters
    ----------
    json
    filters

    Returns
    -------
    filtered_object: object
        Resulting JSON Filtered Object
    """
    if not isinstance(filters, list):
        filters = [filters]
    object_layers = {0: json}
    try:
        for index, filter_layer in enumerate(filters):
            layer_index = index + 1
            object_layers[layer_index] = object_layers[index][filter_layer]
            del object_layers[index]
    except KeyError as key_error:
        error_message = (
            f"Unable to find matching JSON Filtering | {key_error} | {filters}"
        )
        logger.error(error_message)
        raise KeyError from key_error
    return object_layers[len(filters)]
