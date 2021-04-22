#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Common National Parks Config
"""

from typing import List


class GlacierNationalPark(object):
    """
    Config Storage for Common Campsites / Collections
    """
    CAMPGROUND_GLACIER_FISH_CREEK: int = 232493
    CAMPGROUND_GLACIER_MANY_GLACIER: int = 251869
    CAMPGROUND_GLACIER_APGAR: int = 234669
    CAMPGROUND_GLACIER_ST_MARY: int = 232492

    COLLECTION_GLACIER_NATIONAL_PARK: List[int] = [
        CAMPGROUND_GLACIER_APGAR,
        CAMPGROUND_GLACIER_ST_MARY,
        CAMPGROUND_GLACIER_MANY_GLACIER,
        CAMPGROUND_GLACIER_FISH_CREEK
    ]

    RECREATION_AREA_GLACIER_NATIONAL_PARK = 130


class NationalParks(GlacierNationalPark):
    """
    Config Storage for Common Campsites / Collections
    """
    pass
