#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Search Script Example
"""

from datetime import datetime
import logging

from camply.containers import SearchWindow
from camply.search import SearchRecreationDotGov

logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)

month_of_june = SearchWindow(start_date=datetime(year=2021, month=6, day=1),
                             end_date=datetime(year=2021, month=6, day=30))
camping_finder = SearchRecreationDotGov(search_window=month_of_june,
                                        recreation_area=2725,  # Glacier Ntl Park
                                        weekends_only=False)
matches = camping_finder.search_matching_campsites_available(log=True, verbose=True)
