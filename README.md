<p align="center">
  <img src="docs/static/camply.svg" width="400" height="400"  alt="camply">
</p>

### Command Line Campsite Search:

```shell
❯ camply --find-availabilities \
    --rec-area-id 2725 \
    --start-date 2021-06-01 \
    --end-date 2021-06-30
   
2021-04-23 21:57:36,645 [    INFO]: 30 dates selected for search, ranging from 2021-06-01 to 2021-06-30
2021-04-23 21:57:36,645 [    INFO]: Retrieving Facility Information for Recreation Area ID: 2725.
2021-04-23 21:57:37,281 [    INFO]: 4 camping facilities found
2021-04-23 21:57:37,281 [    INFO]: ⛰  Glacier National Park, MT (#2725) - 🏕  Apgar Group Sites (#234669)
2021-04-23 21:57:37,281 [    INFO]: ⛰  Glacier National Park, MT (#2725) - 🏕  Fish Creek Campground (#232493)
2021-04-23 21:57:37,281 [    INFO]: ⛰  Glacier National Park, MT (#2725) - 🏕  Many Glacier Campground (#251869)
2021-04-23 21:57:37,281 [    INFO]: ⛰  Glacier National Park, MT (#2725) - 🏕  St. Mary Campground (#232492)
2021-04-23 21:57:37,281 [    INFO]: Searching across 4 campgrounds
2021-04-23 21:57:37,281 [    INFO]: Searching Apgar Group Sites, Glacier National Park, MT (234669) for availability: June, 2021
2021-04-23 21:57:38,063 [    INFO]: 	⛺️	1 sites found in June
2021-04-23 21:57:38,878 [    INFO]: Searching Many Glacier Campground, Glacier National Park, MT (251869) for availability: June, 2021
2021-04-23 21:57:39,720 [    INFO]: 	❌	0 sites found in June
2021-04-23 21:57:40,527 [    INFO]: Searching Fish Creek Campground, Glacier National Park, MT (232493) for availability: June, 2021
2021-04-23 21:57:41,552 [    INFO]: 	⛺️	2 sites found in June
2021-04-23 21:57:42,984 [    INFO]: Searching St. Mary Campground, Glacier National Park, MT (232492) for availability: June, 2021
2021-04-23 21:57:44,640 [    INFO]: 	❌	0 sites found in June
2021-04-23 21:57:44,640 [    INFO]: ⛺️ ⛺️ ⛺️ ⛺️ 3 Campsites Matching Search Preferences
2021-04-23 21:57:44,644 [    INFO]: 📅 Tue, June 01 🏕 2 sites
2021-04-23 21:57:44,646 [    INFO]: 	⛰️  Glacier National Park, MT  🏕  Apgar Group Sites: ⛺ 1 sites
2021-04-23 21:57:44,646 [    INFO]: 		🔗 https://www.recreation.gov/camping/campsites/77065
2021-04-23 21:57:44,646 [    INFO]: 	⛰️  Glacier National Park, MT  🏕  Fish Creek Campground: ⛺ 1 sites
2021-04-23 21:57:44,647 [    INFO]: 		🔗 https://www.recreation.gov/camping/campsites/5456
2021-04-23 21:57:44,647 [    INFO]: 📅 Mon, June 07 🏕 1 sites
2021-04-23 21:57:44,648 [    INFO]: 	⛰️  Glacier National Park, MT  🏕  Fish Creek Campground: ⛺ 1 sites
2021-04-23 21:57:44,648 [    INFO]: 		🔗 https://www.recreation.gov/camping/campsites/5441
```

### YAML Config Campsite Search

`campsite_searches/glacier_in_may.yaml`:

```yaml
glacier_month_of_june:
    enabled:         True
    recreation_area: 2725
    start_date:      2021-06-09
    end_date:        2021-06-16
```

```shell
❯ camply --find-availabilities \
    --config-file campsite_searches/glacier_in_may.yaml
    
2021-04-23 22:04:46,365 [    INFO]: 30 dates selected for search, ranging from 2021-06-01 to 2021-06-30
2021-04-23 22:04:46,365 [    INFO]: Retrieving Facility Information for Recreation Area ID: 2725.
2021-04-23 22:04:46,781 [    INFO]: 4 camping facilities found
2021-04-23 22:04:46,781 [    INFO]: ⛰  Glacier National Park, MT (#2725) - 🏕  Apgar Group Sites (#234669)
2021-04-23 22:04:46,781 [    INFO]: ⛰  Glacier National Park, MT (#2725) - 🏕  Fish Creek Campground (#232493)
2021-04-23 22:04:46,781 [    INFO]: ⛰  Glacier National Park, MT (#2725) - 🏕  Many Glacier Campground (#251869)
2021-04-23 22:04:46,781 [    INFO]: ⛰  Glacier National Park, MT (#2725) - 🏕  St. Mary Campground (#232492)
2021-04-23 22:04:46,782 [    INFO]: Searching across 4 campgrounds
2021-04-23 22:04:46,782 [    INFO]: Searching Apgar Group Sites, Glacier National Park, MT (234669) for availability: June, 2021
2021-04-23 22:04:47,148 [    INFO]: 	⛺️	1 sites found in June
2021-04-23 22:04:48,487 [    INFO]: Searching Many Glacier Campground, Glacier National Park, MT (251869) for availability: June, 2021
2021-04-23 22:04:49,094 [    INFO]: 	❌	0 sites found in June
2021-04-23 22:04:49,596 [    INFO]: Searching Fish Creek Campground, Glacier National Park, MT (232493) for availability: June, 2021
2021-04-23 22:04:50,362 [    INFO]: 	⛺️	2 sites found in June
2021-04-23 22:04:51,593 [    INFO]: Searching St. Mary Campground, Glacier National Park, MT (232492) for availability: June, 2021
2021-04-23 22:04:52,516 [    INFO]: 	❌	0 sites found in June
2021-04-23 22:04:52,517 [    INFO]: ⛺️ ⛺️ ⛺️ ⛺️ 3 Campsites Matching Search Preferences
2021-04-23 22:04:52,520 [    INFO]: 📅 Tue, June 01 🏕 2 sites
2021-04-23 22:04:52,522 [    INFO]: 	⛰️  Glacier National Park, MT  🏕  Apgar Group Sites: ⛺ 1 sites
2021-04-23 22:04:52,522 [    INFO]: 		🔗 https://www.recreation.gov/camping/campsites/77065
2021-04-23 22:04:52,522 [    INFO]: 	⛰️  Glacier National Park, MT  🏕  Fish Creek Campground: ⛺ 1 sites
2021-04-23 22:04:52,522 [    INFO]: 		🔗 https://www.recreation.gov/camping/campsites/5456
2021-04-23 22:04:52,522 [    INFO]: 📅 Mon, June 07 🏕 1 sites
2021-04-23 22:04:52,523 [    INFO]: 	⛰️  Glacier National Park, MT  🏕  Fish Creek Campground: ⛺ 1 sites
2021-04-23 22:04:52,524 [    INFO]: 		🔗 https://www.recreation.gov/camping/campsites/5441
```

### Object-Oriented Campsite Search:

```python
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
```

___________
___________

<br/>
<br/>
<br/>

<p align="center">
<img src="docs/static/juftin.png" width="100" height="100"  alt="juftin logo">
</p>

###### Cool stuff happens in Denver, CO [<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Flag_of_Denver%2C_Colorado.svg/800px-Flag_of_Denver%2C_Colorado.svg.png" width="25" alt="Denver">](https://denver-devs.slack.com/)