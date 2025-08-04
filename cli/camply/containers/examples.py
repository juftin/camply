"""
Example Containers
"""

import datetime

from camply.containers.data_containers import AvailableCampsite

example_campsite = AvailableCampsite(
    campsite_id=100,
    booking_date=datetime.datetime(2023, 9, 1),
    booking_end_date=datetime.datetime(2023, 9, 2),
    booking_nights=1,
    campsite_site_name="Test Campsite Name",
    campsite_loop_name="A1",
    campsite_type="Test",
    campsite_occupancy=(1, 5),
    campsite_use_type="Test",
    availability_status="Available",
    recreation_area="Test Recreation Area",
    recreation_area_id=20,
    facility_name="Test Campground",
    facility_id=50,
    booking_url="https://youtu.be/eBGIQ7ZuuiU",
    permitted_equipment=[],
    campsite_attributes=[],
)
