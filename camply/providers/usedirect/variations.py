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


class NorthernTerritory(UseDirectProvider):
    """
    Australian NorthernTerritory
    """

    base_url = "https://northernterritoryrdr.usedirect.com"
    campground_url = "https://parkbookings.nt.gov.au"
    rdr_path = "NorthernTerritoryRDR"
    booking_path = "Web/Facilities/SearchViewUnitAvailabity.aspx"
    booking_path_params = False
    state_code = "NT"


class FloridaStateParks(UseDirectProvider):
    """
    Florida State Parks
    """

    base_url = "https://floridardr.usedirect.com"
    campground_url = "https://www.reserve.floridastateparks.org"
    rdr_path = "FloridaRDR"
    booking_path = "Web"
    state_code = "FL"


class OregonMetro(UseDirectProvider):
    """
    Oregon Metro Parks
    """

    base_url = "https://oregonrdr.usedirect.com"
    campground_url = "https://reservemetro.usedirect.com"
    rdr_path = "oregonmetrordr"
    booking_path = "MetroWeb/Facilities/SearchViewUnitAvailabity.aspx"
    booking_path_params = False
    state_code = "OR"


class ReserveOhio(UseDirectProvider):
    """
    Ohio State Parks
    """

    base_url = "https://ohiordr.usedirect.com"
    campground_url = "https://www.reserveohio.com"
    rdr_path = "ohiordr"
    booking_path = "OhioCampWeb"
    state_code = "OH"


class ReserveVAParks(UseDirectProvider):
    """
    Virginia State Parks
    """

    base_url = "https://virginiardr.usedirect.com"
    campground_url = "https://reservevaparks.com"
    rdr_path = "virginiardr"
    booking_path = "Web"
    state_code = "VA"


class AZStateParks(UseDirectProvider):
    """
    Arizona State Parks
    """

    base_url = "https://azrdr.usedirect.com"
    campground_url = "https://azstateparks.com"
    rdr_path = "azrdr"
    booking_path = "reserve"
    state_code = "AZ"


class MaricopaCountyParks(UseDirectProvider):
    """
    Maricopa County Parks
    """

    base_url = "https://maricopardr.usedirect.com"
    campground_url = "https://www.maricopacountyparks.org"
    rdr_path = "maricopardr"
    booking_path = "MaricopaWeb/Facilities/SearchViewUnitAvailabity.aspx"
    booking_path_params = False
    state_code = "AZ"


class MissouriStateParks(UseDirectProvider):
    """
    Missouri State Parks
    """

    base_url = "https://msprdr.usedirect.com"
    campground_url = "https://icampmo1.usedirect.com"
    rdr_path = "msprdr"
    booking_path = "MSPWeb"
    state_code = "MO"


class AlabamaStateParks(UseDirectProvider):
    """
    Alabama State Parks
    """

    base_url = "https://alabamardr.usedirect.com"
    campground_url = "https://www.reservealapark.com"
    rdr_path = "alabamardr"
    booking_path = "AlabamaWebHome/Facilities/SearchViewUnitAvailabity.aspx"
    booking_path_params = False
    state_code = "AL"