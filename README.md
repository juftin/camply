<p align="center">
  <img src="https://raw.githubusercontent.com/juftin/camply/camply/docs/static/camply.svg" 
    width="400" height="400" alt="camply">
</p>

`camply`, the campsite finder, is a tool to help you book an online campground. Finding reservations
at sold out campgrounds can be tough. That's where `camply` comes in. It scrapes the APIs of Booking
Services like https://recreation.gov (which works on thousands of campgrounds across the USA) to
continuously check for cancellations and availabilities to pop up. Once a campsite becomes
available, `camply` sends you a notification to book your spot!

[![Version](https://img.shields.io/badge/camply-0.1.0-orange)](https://github.com/juftin/camply)
[![Testing Status](https://github.com/juftin/camply/actions/workflows/pytest.yaml/badge.svg?branch=camply)](https://github.com/juftin/camply/actions/workflows/pytest.yaml)
[![Python Versions](https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8%20|%203.9-blue)](https://pypi.python.org/pypi/camply/)

## Important Notice

`camply` is still under active development and is not fully ready. Once this project is fully ready
code will be released to a `main` branch. If you'd like to contribute to the project please reach
out.

## Table of Contents

- [Important Notice](#important-notice)
- [Usage](#usage)
  * [Command Line Usage](#command-line-usage)
    + [campsites](#-campsites-)
    + [recreation-areas](#-recreation-areas-)
    + [campgrounds](#-campgrounds-)
    + [configure](#-configure-)
  * [Examples](#examples)
    + [Searching for a Campsite](#searching-for-a-campsite)
    + [Generating the config file for notifications](#generating-the-config-file-for-notifications)
    + [Continuously Searching For A Campsite](#continuously-searching-for-a-campsite)
    + [Look for weekend campsite availabilities](#look-for-weekend-campsite-availabilities)
    + [Look for a campsite inside of Yellowstone](#look-for-a-campsite-inside-of-yellowstone)
    + [Look for Recreation Areas to Search](#look-for-recreation-areas-to-search)
    + [Look for specific campgrounds within a recreation area](#look-for-specific-campgrounds-within-a-recreation-area)
    + [Look for specific campgrounds that match a query string](#look-for-specific-campgrounds-that-match-a-query-string)
    + [YAML Config Campsite Search](#yaml-config-campsite-search)
  * [Finding Recreation Areas and Campgrounds without Using the Command Line](#finding-recreation-areas-and-campgrounds-without-using-the-command-line)
  * [Object Oriented Usage](#object-oriented-usage)
    + [Object-Oriented Campsite Search:](#object-oriented-campsite-search-)
- [Dependencies](#dependencies)

## Usage

### Command Line Usage

When installed, `camply`'s command line utility can be invoked with the command, `camply`. The CLI
tool accepts four sub-arguments: `campsites`, `recreation-areas`, `campgrounds`, and `configure`

```text
❯ camply
2021-05-11 20:39:01,327 [  CAMPLY]: camply, the campsite finder ⛺️
usage: camply [-h] [--version] {campsites,recreation-areas,campgrounds,configure} ...

Welcome to camply, the campsite finder. Finding reservations at these sold out campgrounds can be
tough. That's where camply comes in. It scrapes the APIs of Booking Services like
https://recreation.gov (which works on thousands of campgrounds across the USA) to continuously check
for cancellations and availabilities to pop up. Once a campsite becomes available, camply sends you a
notification to book your spot!

positional arguments:
  {campsites,recreation-areas,campgrounds,configure}
    campsites           Find Available Campsites using Search Criteria
    recreation-areas    Search for Recreation Areas and list them.
    campgrounds         Search for Campgrounds (inside of Recreation Areas) and list them
    configure           Set up camply configuration file with an interactive console

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

#### `campsites`

Find Available Campsites using Search Criteria

##### Arguments:

* `--rec-area-id`: `RECREATION_AREA_ID`
    + Add Recreation Areas (comprised of campgrounds) by ID
* `--campground`: `CAMPGROUND_LIST`
    + Add individual Campgrounds by ID
* `--start-date`: `START_DATE`
    + `YYYY-MM-DD`: Start of Search window. You will be arriving this day
* `--end-date`: `END_DATE`
    + `YYYY-MM-DD`: End of Search window. You will be leaving the following day
* `--weekends`
    + Only search for weekend bookings (Fri/Sat)
* `--provider`: `PROVIDER`
    + Camping Search Provider. Options available are
      'Yellowstone' and 'RecreationDotGov'. Defaults to
      'RecreationDotGov'
* `--continuous`
    + Continuously check for a campsite to become available.
* `--polling-interval`: `POLLING_INTERVAL`
    + If `--continuous` is activated, how often to wait in between checks (in minutes). Defaults to
      10, cannot be less than 5
* `--notifications`: `NOTIFICATIONS`
    + Types of notifications to receive. Options available are `email`, `pushover`, or
      `silent`. Defaults to `silent` - which just logs messages to console
* `--notify-first-try`
    + Whether to send a non-silent notification if a matching campsite is found on the first try.
      Defaults to false.
* `--search-forever`
    + Continuous search on steroids. This method continues to search after the first availability
      has been found. The one caveat is that it will never notify about the same identical campsite
      forthe same date.

#### `recreation-areas`

Search for Recreation Areas. Recreation Areas are places like National Parks and National Forests
that can contain one or many campgrounds.

##### Arguments:

* `--search` `SEARCH`
    + Search for Campgrounds or Recreation Areas by search string
* `--state` `STATE`
    + Filter by state code: `--state CO`

#### `campgrounds`

Search for Campgrounds. Campgrounds are facilities inside of Recreation Areas that contain
campsites. Most 'Campgrounds' are traditional blocks of campsites, others are facilities like fire
towers that might only contain a single 'campsite'

##### Arguments:

* `--search` `SEARCH`
    + Search for Campgrounds or Recreation Areas by search string
* `--state` `STATE`
    + Filter by state code: `--state CO`
* `--rec-area-id`: `RECREATION_AREA_ID`
    + Add Recreation Areas (comprised of campgrounds) by ID
* `--campground`: `CAMPGROUND_LIST`
    + Add individual Campgrounds by ID

#### `configure`

`configure` takes no arguments, just type `camply configure` to get started with setting
notification variables.

### Examples

#### Searching for a Campsite

```shell
camply campsites \
    --rec-area-id 2725 \
    --start-date 2021-06-10 \
    --end-date 2021-06-17
```

#### Generating the config file for notifications

```shell
camply configure
```

#### Continuously Searching For A Campsite

This version runs until found a match is found. It also sends a notification via `pushover`.
Alternate notification methods are `email` and `silent` (default).

```text
camply campsites \
    --rec-area-id 2725 \
    --start-date 2021-07-01 \
    --end-date 2021-07-31 \
    --continuous \
    --notifications pushover
```

#### Look for weekend campsite availabilities

This below search looks across larger periods of time, but only if a campground is available to book
on a Friday or Saturday night (`--weekends`). It also uses the `--polling-interval` argument which
checks every 5 minutes instead of the default 10 minutes.

```shell
camply campsites \
    --rec-area-id 2991 \
    --start-date 2021-05-01 \
    --end-date 2021-07-31 \
    --weekends \
    --continuous \
    --notifications email \
    --polling-interval 5
```

#### Look for a campsite inside of Yellowstone

Yellowstone doesn't use https://recreation.gov to manage its campgrounds, instead it uses its own
proprietary system. In order to search the Yellowstone API for campsites, make sure to pass
the `--provider "yellowstone"` argument. This flag disables `--rec-area-id` and `--campground`
arguments. Notice how `camply` throws a warning: `"Found matching campsites on the first try!
Switching to Silent Notifications..."`. When camply is told to run `--continuous` and it finds
matching sites on the first try, it just logs the campsites quietly. To bypass this behavior, pass
the `--notify-first-try` argument

```shell
camply campsites \
    --provider yellowstone \
    --start-date 2021-06-09 \
    --end-date 2021-06-16 \
    --continuous
```

#### Look for Recreation Areas to Search

This search lists recreation areas. It accepts `--search` and `--state` arguments

```shell
camply recreation-areas --search "Yosemite National Park"
```

#### Look for specific campgrounds within a recreation area

This search lists campgrounds attached to a recreation area id `--rec-area-id`. It also
accepts `--search` and `--state` arguments.

```shell
camply campgrounds --rec-area-id 2991
```

#### Look for specific campgrounds that match a query string

The below search looks for Fire Lookout Towers to stay in inside of California.

```shell
camply campgrounds --search "Fire Tower Lookout" --state CA
```

#### YAML Config Campsite Search

`campsite_searches/glacier_in_may.yaml`:

```yaml
glacier_month_of_june:
    enabled:         True
    recreation_area: 2725
    start_date:      2021-06-09
    end_date:        2021-06-16
```

### Finding Recreation Areas and Campgrounds without Using the Command Line

You can uncover campground and recreation area IDs just by using the https://recreation.gov search
functionality. Use the below example for a campground within Glacier National Park.

First, perform your search on https://recreation.gov
<p>
<img src="docs/static/recreation_dot_gov.png" width="500" alt="recreation_dot_gov search">
</p>

The above search will take you to a URL like this:
https://www.recreation.gov/search?q=Glacier%20National%20Park&entity_id=2725&entity_type=recarea.
Taking a closer look at the URL components you can see that Glacier National Park has the Recreation
Area ID #2725.

Searching deeper you might mind a place like Fish Creek Campground at a URL
like https://www.recreation.gov/camping/campgrounds/232493. Here, we can see that this campground
has a Campground ID of #232493 (and it also sits inside of Recreation Area ID #2725)

### Object Oriented Usage

#### Object-Oriented Campsite Search:

```python
from datetime import datetime
import logging
from typing import List

from camply.containers import AvailableCampsite, SearchWindow
from camply.search import SearchRecreationDotGov

logging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",
                    level=logging.INFO)

month_of_june = SearchWindow(start_date=datetime(year=2021, month=6, day=1),
                             end_date=datetime(year=2021, month=6, day=30))
camping_finder = SearchRecreationDotGov(search_window=month_of_june,
                                        recreation_area=2725,  # Glacier Ntl Park
                                        weekends_only=False)
matches: List[AvailableCampsite] = camping_finder.get_matching_campsites(log=True, verbose=True,
                                                                         continuous=False)
```

The above script returns a list of any matching `AvailableCampsite` objects:

```python
[
    AvailableCampsite(campsite_id='5391',
                      booking_date=datetime.datetime(2021, 6, 13, 0, 0),
                      campsite_site_name='B37',
                      campsite_loop_name='Loop B',
                      campsite_type='STANDARD NONELECTRIC',
                      campsite_occupancy=(0, 8),
                      campsite_use_type='Overnight',
                      availability_status='Available',
                      recreation_area='Glacier National Park, MT',
                      recreation_area_id='2725',
                      facility_name='Fish Creek Campground',
                      facility_id='232493',
                      booking_url='https://www.recreation.gov/camping/campsites/5391')
]
```

## Dependencies

I've tried to build this module pretty simply. Everything is built on Python 3. This particular
project was built in Python `3.8.X`, but any version of Python 3 should suffice. Currently, there
are four required packages, the underlying code has been implemented to be friendly across a wide
range of supported package versions.

- [requests](https://docs.python-requests.org/en/master/)
    - The `requests` package is used to fetch data from the APIs of Camping Booking Providers
- [pandas](https://pandas.pydata.org/)
    - The `pandas` package is to group and aggregate across large data sets of campsites,
      campgrounds, and recreation areas.
- [pyyaml](https://pyyaml.org/wiki/PyYAML)
    - The `pyyaml` package is used to parse YAML files for campsite search configurations
- [tenacity](https://tenacity.readthedocs.io/en/latest/)
    - The `tenacity` package is used for retrying data fetches from some APIs. This retrying
      methodology handles exceptions allowing for API downtime and facilitating exponential backoff.
- [python-dotenv](https://github.com/theskumar/python-dotenv)
    - The `python-dotenv` ¬package reads key-value pairs from a `.env` file and can set them as
      environment variables.

___________
___________

<br/>
<br/>
<br/>


[<p align="center" ><img src="https://raw.githubusercontent.com/juftin/juftin/master/static/juftin.png" width="120" height="120"  alt="juftin logo"> </p>](https://github.com/juftin)

