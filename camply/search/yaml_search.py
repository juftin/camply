#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Search Script Example
"""

from datetime import datetime
from glob import glob
import logging
from os.path import abspath, join
from pathlib import Path
from typing import Union

from camply.containers import SearchWindow
from camply.search import SearchRecreationDotGov, SearchYellowstone
from camply.utils import read_yml

logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

camply_dir = Path(abspath(__file__)).parent.parent
search_dir = join(camply_dir, "campsite_searches")

yml_files = glob(join(search_dir, "**/*.yml"),
                 recursive=True)
yaml_files = glob(join(search_dir, "**/*.yaml"),
                  recursive=True)
config_files = yml_files + yaml_files

SEARCH_FINDER = {
    "RecreationDotGov": SearchRecreationDotGov,
    "YellowstoneLodging": SearchYellowstone
}

for file_path in config_files:
    file_yaml = read_yml(file_path)
    for search_name, entry in file_yaml.items():
        provider = entry.get("provider", "RecreationDotGov")
        search_window = SearchWindow(
            start_date=datetime.strptime(str(entry["start_date"]), "%Y-%m-%d"),
            end_date=datetime.strptime(str(entry["end_date"]), "%Y-%m-%d"))
        recreation_area = entry.get("recreation_area", None)
        campgrounds = entry.get("campgrounds", None)
        weekends_only = entry.get("weekends", False)
        lower_provider_finder = {key.lower(): value for key, value in SEARCH_FINDER.items()}
        try:
            campground_searcher: Union[SearchRecreationDotGov, SearchYellowstone] = \
                SEARCH_FINDER[provider]
        except KeyError as ke:
            error_message = f"That Provider is Not Implemented: {ke}"
            logger.error(error_message)
            raise NotImplementedError(error_message)
        # noinspection PyCallingNonCallable
        campsite_finder = campground_searcher(
            search_window=search_window,
            recreation_area=recreation_area,
            campgrounds=campgrounds,
            weekends_only=weekends_only)
        matches = campsite_finder.get_matching_campsites(log=True, verbose=True)