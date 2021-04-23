#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Search Script Example
"""
from datetime import datetime
import logging

from camply.containers import SearchWindow
from camply.providers import RecreationDotGov
from camply.search.camping_search import SearchRecreationDotGov

logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)

search_window_1 = SearchWindow(start_date=datetime(year=2021, month=6, day=1),
                               end_date=datetime(year=2021, month=6, day=30))
rec_dot_gov = RecreationDotGov()
camping_finder = SearchRecreationDotGov(search_window=search_window_1,
                                        recreation_area=2725,
                                        weekends_only=False)
matches = camping_finder.search_matching_campsites_available()
df = camping_finder._assemble_availabilities(matches, log=True, verbose=True)
