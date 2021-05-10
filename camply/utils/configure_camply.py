#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Camply Configuration Script
"""

import logging
from os.path import isfile

from camply.config import FileConfig

logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def check_dot_camply_file() -> bool:
    """
    Check to see if the `.camply` file already exists, and return the
    file existence status

    Returns
    -------
    bool
    """
    if isfile(FileConfig.DOT_CAMPLY_HOME_FILE) is True:
        logger.info("Skipping configuration. `.camply` file already exists: "
                    f"{FileConfig.DOT_CAMPLY_HOME_FILE}")
        return True
    else:
        return False


check_dot_camply_file()
