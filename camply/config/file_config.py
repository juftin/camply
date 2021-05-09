#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Project Configuration for Yellowstone Variables
"""

from os.path import abspath, join
from pathlib import Path


class FileConfig(object):
    """
    File Path Storage Class
    """

    _file_config_file = Path(abspath(__file__))
    _config_dir = _file_config_file.parent

    CAMPLY_DIRECTORY = _config_dir.parent
    ROOT_DIRECTORY = CAMPLY_DIRECTORY.parent
    DOT_ENV_FILE = join(ROOT_DIRECTORY, ".env")
