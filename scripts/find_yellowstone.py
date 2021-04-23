#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Python Script to Check Yellowstone Campground Booking API for Availability
"""

import logging

try:
    from camply.providers import YellowstoneLodging
    from camply.config import YellowstoneConfig
except ModuleNotFoundError:
    # APPEND THE PATH FOR THOSE WITHOUT THIS PROJECT AT PYTHON PATH
    from os.path import abspath, join
    from pathlib import Path
    from sys import path as python_path

    camply_dir = join(Path(abspath(__file__)).parent.parent, "camply")
    python_path.append(str(camply_dir))

    from camply.providers import YellowstoneLodging
    from camply.config import YellowstoneConfig

if __name__ == "__main__":
    # Find the campsite!
    logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s [%(name)s]",
                        level=logging.INFO)
    campsite_finder = YellowstoneLodging(booking_start=YellowstoneConfig.BOOKING_START,
                                         number_of_guests=YellowstoneConfig.NUMBER_OF_GUESTS,
                                         number_of_nights=YellowstoneConfig.NUMBER_OF_NIGHTS,
                                         polling_interval=YellowstoneConfig.POLLING_INTERVAL)
    campsite_finder.continuously_check_for_availability()
