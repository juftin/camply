#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Search Provider Configuration
"""

from typing import Dict

from camply.search import SearchRecreationDotGov, SearchYellowstone

CAMPSITE_PROVIDER: Dict[str, object] = {
    "RecreationDotGov": SearchRecreationDotGov,
    "Yellowstone": SearchYellowstone
}
