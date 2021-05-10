#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Yellowstone Variables
"""

from os.path import abspath, isfile, join
from pathlib import Path


class FileConfig(object):
    """
    File Path Storage Class
    """
    HOME_PATH = abspath(Path.home())
    DOT_CAMPLY_HOME_FILE = join(HOME_PATH, ".camply")
    _file_config_file = Path(abspath(__file__))
    _config_dir = _file_config_file.parent

    CAMPLY_DIRECTORY = _config_dir.parent
    ROOT_DIRECTORY = CAMPLY_DIRECTORY.parent

    if isfile(DOT_CAMPLY_HOME_FILE):
        DOT_CAMPLY_FILE = DOT_CAMPLY_HOME_FILE
    else:
        DOT_CAMPLY_FILE = join(ROOT_DIRECTORY, ".camply")
