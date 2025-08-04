# Object-Oriented Usage (Python)

## Search for a Recreation.gov Campsite

```python
from datetime import datetime
import logging
from typing import List

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchRecreationDotGov

logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)

month_of_june = SearchWindow(start_date=datetime(year=2022, month=6, day=1),
                             end_date=datetime(year=2022, month=6, day=30))
camping_finder = SearchRecreationDotGov(search_window=month_of_june,
                                        recreation_area=2725,  # Glacier Ntl Park
                                        weekends_only=False,
                                        nights=1)
matches: List[AvailableCampsite] = camping_finder.get_matching_campsites(log=True, verbose=True,
                                                                         continuous=False)
```

The above script returns a list of any matching `AvailableCampsite` pydantic objects:

```python
[
    AvailableCampsite(campsite_id="5391",
                      booking_date=datetime.datetime(2022, 6, 13, 0, 0),
                      campsite_site_name="B37",
                      campsite_loop_name="Loop B",
                      campsite_type="STANDARD NONELECTRIC",
                      campsite_occupancy=(0, 8),
                      campsite_use_type="Overnight",
                      availability_status="Available",
                      recreation_area="Glacier National Park, MT",
                      recreation_area_id="2725",
                      facility_name="Fish Creek Campground",
                      facility_id="232493",
                      booking_url="https://www.recreation.gov/camping/campsites/5391")
]
```

## Continuously Search for Recreation.gov Campsites

You'll notice that the `get_matching_campsites` function takes accepts parameter values very similar
to the commandline arguments.

```python
from datetime import datetime
import logging

from camply.containers import SearchWindow
from camply.search import SearchRecreationDotGov

logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)

month_of_june = SearchWindow(start_date=datetime(year=2022, month=6, day=1),
                             end_date=datetime(year=2022, month=6, day=30))
camping_finder = SearchRecreationDotGov(search_window=month_of_june,
                                        recreation_area=[2991, 1074],  # Multiple Rec Areas
                                        weekends_only=False,
                                        nights=3)
camping_finder.get_matching_campsites(log=True, verbose=True,
                                      continuous=True,
                                      polling_interval=5,
                                      notification_provider="pushover",
                                      search_forever=True,
                                      notify_first_try=False)
```
