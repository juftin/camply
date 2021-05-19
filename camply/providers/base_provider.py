#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
BaseProvider Base Class
"""

from abc import ABC
import logging

logger = logging.getLogger(__name__)


class BaseProvider(ABC):
    """
    Base Provider Class
    """
