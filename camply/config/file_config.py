"""
File Configuration Helpers for camply
"""

import pathlib


class FileConfig:
    """
    Easy file configuration helper class
    """

    _this_file = pathlib.Path(__file__)
    _config_dir = _this_file.parent

    SOURCE_CODE_DIR = _config_dir.parent
    PROJECT_DIR = SOURCE_CODE_DIR.parent
