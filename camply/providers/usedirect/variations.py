"""
Usedirect specific variations
"""

from camply.providers.usedirect import UseDirectProvider


class ReserveCalifornia(UseDirectProvider):
    """
    ReserveCalifornia
    """

    base_url = "https://calirdr.usedirect.com"
    campground_url = "https://www.reservecalifornia.com"


class NorthernTerritory(UseDirectProvider):
    """
    Australian NorthernTerritory
    """

    base_url = "https://northernterritoryrdr.usedirect.com"
    campground_url = "https://parkbookings.nt.gov.au"
    rdr_path = "NorthernTerritoryRDR"
