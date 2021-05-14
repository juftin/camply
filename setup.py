# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["camply",
            "camply.config",
            "camply.notifications",
            "camply.providers",
            "camply.providers.recreation_dot_gov",
            "camply.providers.xanterra",
            "camply.search",
            "camply.utils"]

package_data = {"": ["*"]}

install_requires = ["pandas",
                    "python-dotenv",
                    "pytz",
                    "requests",
                    "tenacity"]

entry_points = \
    {'console_scripts': ['camply = camply.utils.camply_cli:main']}

long_description = '<p align="center">\n  <img src="https://raw.githubusercontent.com/juftin/camply/camply/docs/static/camply.svg" \n    width="400" height="400" alt="camply">\n</p>\n\n`camply`, the campsite finder, is a tool to help you book an online campground. Finding reservations\nat sold out campgrounds can be tough. That\'s where `camply` comes in. It scrapes the APIs of Booking\nServices like https://recreation.gov (which works on thousands of campgrounds across the USA) to\ncontinuously check for cancellations and availabilities to pop up. Once a campsite becomes\navailable, `camply` sends you a notification to book your spot!\n\n[![Version](https://img.shields.io/badge/camply-0.1.0-orange)](https://github.com/juftin/camply)\n[![Testing Status](https://github.com/juftin/camply/actions/workflows/pytest.yaml/badge.svg?branch=camply)](https://github.com/juftin/camply/actions/workflows/pytest.yaml)\n[![Python Versions](https://img.shields.io/badge/python-3.6%20|%203.7%20|%203.8%20|%203.9-blue)](https://pypi.python.org/pypi/camply/)\n\n## Important Notice\n\n`camply` is still under active development and is not fully ready. Once this project is fully ready\ncode will be released to a `main` branch. If you\'d like to contribute to the project please reach\nout.\n\n## Table of Contents\n\n- [Important Notice](#important-notice)\n- [Usage](#usage)\n    * [Command Line Usage](#command-line-usage)\n        + [campsites](#-campsites-)\n        + [recreation-areas](#-recreation-areas-)\n        + [campgrounds](#-campgrounds-)\n        + [configure](#-configure-)\n    * [Examples](#examples)\n        + [Searching for a Campsite](#searching-for-a-campsite)\n        + [Generating the config file for notifications](#generating-the-config-file-for-notifications)\n        + [Continuously Searching For A Campsite](#continuously-searching-for-a-campsite)\n        + [Look for weekend campsite availabilities](#look-for-weekend-campsite-availabilities)\n        + [Look for a campsite inside of Yellowstone](#look-for-a-campsite-inside-of-yellowstone)\n        + [Look for Recreation Areas to Search](#look-for-recreation-areas-to-search)\n        + [Look for specific campgrounds within a recreation area](#look-for-specific-campgrounds-within-a-recreation-area)\n        + [Look for specific campgrounds that match a query string](#look-for-specific-campgrounds-that-match-a-query-string)\n    * [Finding Recreation Areas and Campgrounds without Using the Command Line](#finding-recreation-areas-and-campgrounds-without-using-the-command-line)\n    * [Object Oriented Usage](#object-oriented-usage)\n        + [Object-Oriented Campsite Search:](#object-oriented-campsite-search-)\n- [Dependencies](#dependencies)\n\n## Installation and Execution\n\n### PyPi\n\n```shell\npip install camply\n```\n\n### Building Locally\n\n```shell\ngit clone https://github.com/juftin/camply.git\ncd camply\npython setup.py install\n```\n\n### Docker\n\nOfficial Docker Image Coming Soon - build locally for now.\n\n```shell\ngit clone https://github.com/juftin/camply.git\ncd camply\ndocker build --tag camply:latest .\n```\n\nHere\'s an example of a detached container searching in the background:\n\n```shell\ndocker run -d --rm \\\n  --name camply \\\n  --env PUSHOVER_PUSH_TOKEN=${PUSHOVER_PUSH_TOKEN} \\\n  --env PUSHOVER_PUSH_USER=${PUSHOVER_PUSH_USER} \\\n  camply:latest \\\n  camply campsites \\\n      --rec-area-id 2991 \\\n      --start-date 2021-08-01 \\\n      --end-date 2021-08-31 \\\n      --continuous \\\n      --notifications pushover\n```\n\n## Usage\n\n### Command Line Usage\n\nWhen installed, `camply`\'s command line utility can be invoked with the command, `camply`. The CLI\ntool accepts four sub-arguments: `campsites`, `recreation-areas`, `campgrounds`, and `configure`\n\n```text\n❯ camply\n2021-05-11 20:39:01,327 [  CAMPLY]: camply, the campsite finder ⛺️\nusage: camply [-h] [--version] {campsites,recreation-areas,campgrounds,configure} ...\n\nWelcome to camply, the campsite finder. Finding reservations at these sold out campgrounds can be\ntough. That\'s where camply comes in. It scrapes the APIs of Booking Services like\nhttps://recreation.gov (which works on thousands of campgrounds across the USA) to continuously check\nfor cancellations and availabilities to pop up. Once a campsite becomes available, camply sends you a\nnotification to book your spot!\n\npositional arguments:\n  {campsites,recreation-areas,campgrounds,configure}\n    campsites           Find Available Campsites using Search Criteria\n    recreation-areas    Search for Recreation Areas and list them.\n    campgrounds         Search for Campgrounds (inside of Recreation Areas) and list them\n    configure           Set up camply configuration file with an interactive console\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --version             show program\'s version number and exit\n```\n\n#### `campsites`\n\nFind Available Campsites using Search Criteria\n\n##### Arguments:\n\n* `--rec-area-id`: `RECREATION_AREA_ID`\n    + Add Recreation Areas (comprised of campgrounds) by ID\n* `--campground`: `CAMPGROUND_LIST`\n    + Add individual Campgrounds by ID\n* `--start-date`: `START_DATE`\n    + `YYYY-MM-DD`: Start of Search window. You will be arriving this day\n* `--end-date`: `END_DATE`\n    + `YYYY-MM-DD`: End of Search window. You will be leaving the following day\n* `--weekends`\n    + Only search for weekend bookings (Fri/Sat)\n* `--provider`: `PROVIDER`\n    + Camping Search Provider. Options available are\n      \'Yellowstone\' and \'RecreationDotGov\'. Defaults to\n      \'RecreationDotGov\'\n* `--continuous`\n    + Continuously check for a campsite to become available.\n* `--polling-interval`: `POLLING_INTERVAL`\n    + If `--continuous` is activated, how often to wait in between checks (in minutes). Defaults to\n      10, cannot be less than 5\n* `--notifications`: `NOTIFICATIONS`\n    + Types of notifications to receive. Options available are `email`, `pushover`, or\n      `silent`. Defaults to `silent` - which just logs messages to console\n* `--notify-first-try`\n    + Whether to send a non-silent notification if a matching campsite is found on the first try.\n      Defaults to false.\n* `--search-forever`\n    + Continuous search on steroids. This method continues to search after the first availability\n      has been found. The one caveat is that it will never notify about the same identical campsite\n      forthe same date.\n\n#### `recreation-areas`\n\nSearch for Recreation Areas. Recreation Areas are places like National Parks and National Forests\nthat can contain one or many campgrounds.\n\n##### Arguments:\n\n* `--search` `SEARCH`\n    + Search for Campgrounds or Recreation Areas by search string\n* `--state` `STATE`\n    + Filter by state code: `--state CO`\n\n#### `campgrounds`\n\nSearch for Campgrounds. Campgrounds are facilities inside of Recreation Areas that contain\ncampsites. Most \'Campgrounds\' are traditional blocks of campsites, others are facilities like fire\ntowers that might only contain a single \'campsite\'\n\n##### Arguments:\n\n* `--search` `SEARCH`\n    + Search for Campgrounds or Recreation Areas by search string\n* `--state` `STATE`\n    + Filter by state code: `--state CO`\n* `--rec-area-id`: `RECREATION_AREA_ID`\n    + Add Recreation Areas (comprised of campgrounds) by ID\n* `--campground`: `CAMPGROUND_LIST`\n    + Add individual Campgrounds by ID\n\n#### `configure`\n\n`configure` takes no arguments, just type `camply configure` to get started with setting\nnotification variables.\n\n### Examples\n\n#### Searching for a Campsite\n\nThe below search looks for campsites inside of Receration Area ID #2725 (Glacier National Park)\nbetween 2021-06-10 and 2021-06-17. The search will be performed once and any results will be logged\nto the console.\n\n```shell\ncamply campsites \\\n    --rec-area-id 2725 \\\n    --start-date 2021-06-10 \\\n    --end-date 2021-06-17\n```\n\n#### Generating the config file for notifications\n\nIn order to send notifications through camply you must set up some authorization values. Whether you\nneed to set up pushover notifications (your pushover account can be set up at https://pushover.net)\nor Email messages, everything can be done thorught the `configure` command. The end result is a file\ncalled `.camply` in your home folder.\n\n```shell\ncamply configure\n```\n\n#### Continuously Searching For A Campsite\n\nThis version runs until found a match is found. It also sends a notification via `pushover`.\nAlternate notification methods are `email` and `silent` (default).\n\nImportant Note: When camply is told to run `--continuous` and it finds matching sites on the first\ntry, it just logs the campsites silently and exits. It\'s always encouraged to perform an initial\nonline search before setting up a camply search. To bypass this behavior and send notifications,\npass the `--notify-first-try` argument\n\n```text\ncamply campsites \\\n    --rec-area-id 2725 \\\n    --start-date 2021-07-01 \\\n    --end-date 2021-07-31 \\\n    --continuous \\\n    --notifications pushover\n```\n\n#### Continue Looking After The First Match Is Found\n\nSometimes you want to search for all possible matches up until your arrival date. No problem. Add\nthe `--search-forever` and Camply won\'t stop sending notifications after the first match is found.\nOne important note, Camply will save and store all previous notifications when `--search-forever` is\nenabled, so it won\'t notify you about the exact same campsite availability twice. This can be\nproblematic when certain campsites become available more than once.\n\n```text\ncamply campsites \\\n    --rec-area-id 2725 \\\n    --start-date 2021-07-01 \\\n    --end-date 2021-07-31 \\\n    --continuous \\\n    --notifications pushover \\\n    --search-forever\n```\n\n#### Look for weekend campsite availabilities\n\nThis below search looks across larger periods of time, but only if a campground is available to book\non a Friday or Saturday night (`--weekends`). It also uses the `--polling-interval` argument which\nchecks every 5 minutes instead of the default 10 minutes.\n\n```shell\ncamply campsites \\\n    --rec-area-id 2991 \\\n    --start-date 2021-05-01 \\\n    --end-date 2021-07-31 \\\n    --weekends \\\n    --continuous \\\n    --notifications email \\\n    --polling-interval 5\n```\n\n#### Look for a campsite inside of Yellowstone\n\nYellowstone doesn\'t use https://recreation.gov to manage its campgrounds, instead it uses its own\nproprietary system. In order to search the Yellowstone API for campsites, make sure to pass\nthe `--provider "yellowstone"` argument. This flag disables `--rec-area-id` and `--campground`\narguments.\n\n```shell\ncamply campsites \\\n    --provider yellowstone \\\n    --start-date 2021-06-09 \\\n    --end-date 2021-06-16 \\\n    --continuous\n```\n\n#### Look for Recreation Areas to Search\n\nJust need to find what your local Recreation Area ID number is? This simple command allows you to\nsearch and list recreation areas. It accepts `--search` and `--state` arguments.\n\n```shell\ncamply recreation-areas --search "Yosemite National Park"\n```\n\n#### Look for specific campgrounds within a recreation area\n\nNeed to get even more specific and search for a particular campground? This search lists campgrounds\nattached to a recreation area id `--rec-area-id`. It also accepts `--search` and `--state`\narguments.\n\n```shell\ncamply campgrounds --rec-area-id 2991\n```\n\n#### Look for specific campgrounds that match a query string\n\nThe below search looks for Fire Lookout Towers to stay in inside of California.\n\n```shell\ncamply campgrounds --search "Fire Tower Lookout" --state CA\n```\n\n### Finding Recreation Areas and Campgrounds without Using the Command Line\n\nYou can uncover campground and recreation area IDs just by using the https://recreation.gov search\nfunctionality. Use the below example for a campground within Glacier National Park.\n\nFirst, perform your search on https://recreation.gov\n<p>\n<img src="docs/static/recreation_dot_gov.png" width="500" alt="recreation_dot_gov search">\n</p>\n\nThe above search will take you to a URL like this:\nhttps://www.recreation.gov/search?q=Glacier%20National%20Park&entity_id=2725&entity_type=recarea.\nTaking a closer look at the URL components you can see that Glacier National Park has the Recreation\nArea ID #2725.\n\nSearching deeper you might mind a place like Fish Creek Campground at a URL\nlike https://www.recreation.gov/camping/campgrounds/232493. Here, we can see that this campground\nhas a Campground ID of #232493 (and it also sits inside of Recreation Area ID #2725)\n\n### Object Oriented Usage\n\n#### Object-Oriented Campsite Search:\n\n```python\nfrom datetime import datetime\nimport logging\nfrom typing import List\n\nfrom camply.containers import AvailableCampsite, SearchWindow\nfrom camply.search import SearchRecreationDotGov\n\nlogging.basicConfig(format="%(asctime)s [%(levelname)8s]: %(message)s",\n                    level=logging.INFO)\n\nmonth_of_june = SearchWindow(start_date=datetime(year=2021, month=6, day=1),\n                             end_date=datetime(year=2021, month=6, day=30))\ncamping_finder = SearchRecreationDotGov(search_window=month_of_june,\n                                        recreation_area=2725,  # Glacier Ntl Park\n                                        weekends_only=False)\nmatches: List[AvailableCampsite] = camping_finder.get_matching_campsites(log=True, verbose=True,\n                                                                         continuous=False)\n```\n\nThe above script returns a list of any matching `AvailableCampsite` objects:\n\n```python\n[\n    AvailableCampsite(campsite_id=\'5391\',\n                      booking_date=datetime.datetime(2021, 6, 13, 0, 0),\n                      campsite_site_name=\'B37\',\n                      campsite_loop_name=\'Loop B\',\n                      campsite_type=\'STANDARD NONELECTRIC\',\n                      campsite_occupancy=(0, 8),\n                      campsite_use_type=\'Overnight\',\n                      availability_status=\'Available\',\n                      recreation_area=\'Glacier National Park, MT\',\n                      recreation_area_id=\'2725\',\n                      facility_name=\'Fish Creek Campground\',\n                      facility_id=\'232493\',\n                      booking_url=\'https://www.recreation.gov/camping/campsites/5391\')\n]\n```\n\n## Dependencies\n\nI\'ve tried to build this module pretty simply. Everything is built on Python 3. This particular\nproject was built in Python `3.8.X`, but any version of Python 3 should suffice. Currently, there\nare four required packages, the underlying code has been implemented to be friendly across a wide\nrange of supported package versions.\n\n- [requests](https://docs.python-requests.org/en/master/)\n    - The `requests` package is used to fetch data from the APIs of Camping Booking Providers\n- [pandas](https://pandas.pydata.org/)\n    - The `pandas` package is to group and aggregate across large data sets of campsites,\n      campgrounds, and recreation areas.\n- [tenacity](https://tenacity.readthedocs.io/en/latest/)\n    - The `tenacity` package is used for retrying data fetches from some APIs. This retrying\n      methodology handles exceptions allowing for API downtime and facilitating exponential backoff.\n- [python-dotenv](https://github.com/theskumar/python-dotenv)\n    - The `python-dotenv` ¬package reads key-value pairs from a `.env` file and can set them as\n      environment variables.\n\n___________\n___________\n\n<br/>\n<br/>\n<br/>\n\n\n[<p align="center" ><img src="https://raw.githubusercontent.com/juftin/juftin/master/static/juftin.png" width="120" height="120"  alt="juftin logo"> </p>](https://github.com/juftin)\n\n',

setup_kwargs = {
    "name": "camply",
    "version": "0.1.0",
    "description": "camply, the campsite finder",
    "long_description": long_description,
    "author": "Justin Flannery",
    "author_email": "juftin@juftin.com",
    "maintainer": "Justin Flannery",
    "maintainer_email": "juftin@juftin.com",
    "url": "https://github.com/juftin/camply",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.6",
}

setup(**setup_kwargs)
