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
    state_code = "CA"
