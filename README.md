<div align="center">
<a href="https://github.com/juftin/camply">
  <img src="https://raw.githubusercontent.com/juftin/camply/main/docs/source/_static/camply.svg"
    width="400" height="400" alt="camply">
</a>
</div>

`camply`, the campsite finder ⛺️, is a tool to help you book a campground online. Finding
reservations at sold out campgrounds can be tough. That's where camply comes in. It searches the
APIs of booking services like https://recreation.gov (which indexes thousands of campgrounds across
the USA) to continuously check for cancellations and availabilities to pop up. Once a campsite
becomes available, camply sends you a notification to book your spot!

___________
___________

[![PyPI](https://img.shields.io/pypi/v/camply?color=blue&label=⛺️camply)](https://github.com/juftin/camply)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camply)](https://pypi.python.org/pypi/camply/)
[![Docker Image Version](https://img.shields.io/docker/v/juftin/camply?color=blue&label=docker&logo=docker)](https://hub.docker.com/r/juftin/camply)
[![Testing Status](https://github.com/juftin/camply/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/juftin/camply/actions/workflows/tests.yaml)
[![GitHub License](https://img.shields.io/github/license/juftin/camply?color=blue&label=License)](https://github.com/juftin/camply/blob/main/LICENSE)
[![Black Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)]()


## [Check Out The Docs](https://juftin.com/camply/)

## Table of Contents

- [Installation](#installation)
    * [PyPI](#pypi)
    * [Docker](#docker)
    * [Building Locally](#building-locally)
- [Command Line Usage](#command-line-usage)
    * [campsites](#campsites)
    * [recreation-areas](#recreation-areas)
    * [campgrounds](#campgrounds)
    * [configure](#configure)
    * [Examples](#examples)
        + [Searching for a Campsite](#searching-for-a-campsite)
        + [Searching for a Campsite by Campground ID](#searching-for-a-campsite-by-campground-id)
        + [Searching for a Specific Campsite by ID](#searching-for-a-specific-campsite-by-id)
        + [Continuously Searching for A Campsite](#continuously-searching-for-a-campsite)
        + [Continue Looking After The First Match Is Found](#continue-looking-after-the-first-match-is-found)
        + [Send a Push Notification](#send-a-push-notification)
        + [Send a Text Message](#send-a-text-message)
        + [Send a Notification to Different Services](#send-a-notification-to-different-services)
        + [Look for Weekend Campsite Availabilities](#look-for-weekend-campsite-availabilities)
        + [Look for Consecutive Nights at the Same Campsite](#look-for-consecutive-nights-at-the-same-campsite)
        + [Look for a Campsite Inside of Yellowstone](#look-for-a-campsite-inside-of-yellowstone)
        + [Look for a Campsite Across Multiple Recreation areas](#look-for-a-campsite-across-multiple-recreation-areas)
        + [Using a YAML Configuration file to search for campsites](#using-a-yaml-configuration-file-to-search-for-campsites)
        + [Searching for a Campsite That Fits Your Equipment](#searching-for-a-campsite-that-fits-your-equipment)
        + [Saving the Results of a Search](#saving-the-results-of-a-search)
        + [Search for Recreation Areas by Query String](#search-for-recreation-areas-by-query-string)
        + [Look for Specific Campgrounds Within a Recreation Area](#look-for-specific-campgrounds-within-a-recreation-area)
        + [Look for Specific Campgrounds by Query String](#look-for-specific-campgrounds-by-query-string)
- [Finding Recreation Areas IDs and Campground IDs To Search Without Using the Command Line](#finding-recreation-areas-ids-and-campground-ids-to-search-without-using-the-command-line)
- [Object-Oriented Usage (Python)](#object-oriented-usage-python)
    * [Search for a Recreation.gov Campsite](#search-for-a-recreationgov-campsite)
    * [Continuously Search for Recreation.gov Campsites](#continuously-search-for-recreationgov-campsites)
- [Running in Docker](#running-in-docker)
- [Dependencies](#dependencies)

## Installation

### PyPI

Camply is hosted on PyPI, you can download it directly from tools like
pip and pipx.

```shell
pip install camply
```

If you're using camply on your command line - it's recommended that you use a tool
like [pipx](https://github.com/pypa/pipx) to easily manage the application in an isolated
virtual environment.

```shell
pipx install camply
```

[PyPI Link](https://pypi.python.org/pypi/camply/)

### Docker

```shell
docker pull juftin/camply
```

[Docker Hub Link](https://hub.docker.com/r/juftin/camply)

**_see [Running in Docker](#running-in-docker) below._

## Command Line Usage

When installed, `camply`'s command line utility can be invoked with the command, `camply`. The CLI
tool accepts one of four sub-arguments: `campsites`, `recreation-areas`, `campgrounds`,
and `configure`.

```text
❯ camply --help

Usage: camply [OPTIONS] COMMAND [ARGS]...

  Welcome to camply, the campsite finder.

  Finding reservations at sold out campgrounds can be tough. That's where
  camply comes in. It searches the APIs of booking services like
  https://recreation.gov (which indexes thousands of campgrounds across the
  USA) to continuously check for cancellations and availabilities to pop up.
  Once a campsite becomes available, camply sends you a notification to book
  your spot!

  visit the camply documentation at https://github.com/juftin/camply

Options:
  --version             Show the version and exit.
  --provider TEXT       Camping Search Provider. Options available are
                        'Yellowstone' and 'RecreationDotGov'. Defaults to
                        'RecreationDotGov', not case-sensitive.
  --debug / --no-debug  Enable extra debugging output
  --help                Show this message and exit.

Commands:
  campgrounds       Search for Campgrounds (inside of Recreation Areas)...
  campsites         Find available Campsites using search criteria
  configure         Set up camply configuration file with an interactive...
  recreation-areas  Search for Recreation Areas and list them
```

### campsites

Search for a campsite within camply. Campsites are returned based on the search criteria provided.
Campsites contain properties like booking date, site type (tent, RV, cabin, etc), capacity, price,
and a link to make the booking. Required parameters include `--start-date`, `--end-date`,
`--rec-area` / `--campground` / `--campsite`. Constant searching functionality can be enabled with
`--continuous` and notifications via Email, Pushover, Pushbullet, and Telegram can be enabled using
`--notifications`.

#### Arguments

* `--rec-area`: `RECREATION_AREA_ID`
    + Add Recreation Areas (comprised of campgrounds) by ID.
      [**_example_](#searching-for-a-campsite)
* `--campground`: `CAMPGROUND_ID`
    + Add individual Campgrounds by ID.
      [**_example_](#searching-for-a-campsite-by-campground-id)
* `--campsite`: `CAMPSITE_ID`
    + Add individual Campsites by ID.
      [**_example_](#searching-for-a-specific-campsite-by-id)
* `--start-date`: `START_DATE`
    + `YYYY-MM-DD`: Start of Search window. You will be arriving this day.
      [**_example_](#searching-for-a-campsite)
* `--end-date`: `END_DATE`
    + `YYYY-MM-DD`: End of Search window. You will be checking out this day..
      [**_example_](#searching-for-a-campsite)
* `--weekends`
    + Only search for weekend bookings (Fri/Sat nights).
      [**_example_](#look-for-weekend-campsite-availabilities)
* `--nights`
    + Search for campsite stays with consecutive nights. Defaults to 1 which returns all campsites
      found.
      [**_example_](#look-for-consecutive-nights-at-the-same-campsite)
* `--provider`: `PROVIDER`
    + Camping Search Provider. Options available are 'Yellowstone' and 'RecreationDotGov'. Defaults
      to 'RecreationDotGov', not case-sensitive.
      [**_example_](#look-for-a-campsite-inside-of-yellowstone)
* `--continuous`
    + Continuously check for a campsite to become available, and quit once at least one campsite is
      found.
      [**_example_](#continuously-searching-for-a-campsite)
* `--search-forever`
    + If `--continuous` is activated, this method continues to search after the first availability
      has been found. The one caveat is that it will never notify about the same identical campsite
      for the same booking date.
      [**_example_](#continue-looking-after-the-first-match-is-found)
* `--notifications`: `NOTIFICATIONS`
    + If `--continuous` is activated, types of notifications to receive. Options available
      are`email`, `pushover`, `pushbullet`, `telegram`, or `silent`. Defaults to `silent` - which just logs
      messages to console.
      [**_example_](#send-a-push-notification)
* `--equipment`
    + Search for campsites compatible with your camping equipment. This argument accepts two
      options, the equipment name and its length If you don't want to filter based on length provide
      a length of 0. Accepted equipment names include `Tent`, `RV`. `Trailer`, `Vehicle` and are
      not case-sensitive.
      [**_example_](#searching-for-a-campsite-that-fits-your-equipment)
* `--notify-first-try`
    + If `--continuous` is activated, whether to send all non-silent notifications if more than 5
      matching campsites are found on the first try. Defaults to false which only sends the first5.
      [**_example_](#continuously-searching-for-a-campsite)
* `--polling-interval`: `POLLING_INTERVAL`
    + If `--continuous` is activated, how often to wait in between checks (in minutes). Defaults to
      10, cannot be less than 5.
      [**_example_](#look-for-weekend-campsite-availabilities)
* `--yaml-config`
    + Rather than provide arguments to the command line utility, instead pass a file path to a YAML
      configuration file. See the documentation for more information on how to structure your
      configuration file.
      [**_example_](#using-a-yaml-configuration-file-to-search-for-campsites)

```shell
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18
```

### recreation-areas

Search for Recreation Areas and their IDs. Recreation Areas are places like National Parks and
National Forests that can contain one or many campgrounds.

#### Arguments:

* `--search` `SEARCH`
    + Search for Campgrounds or Recreation Areas by search string.
* `--state` `STATE`
    + Filter by US state code.

```shell
camply recreation-areas --search "Yosemite National Park"
```

**_see the [examples](#search-for-recreation-areas-by-query-string) for more information_

### campgrounds

Search for Campgrounds and their IDs. Campgrounds are facilities inside of Recreation Areas that
contain campsites. Most 'campgrounds' are areas made up of multiple campsites, others are facilities
like fire towers or cabins that might only contain a single 'campsite' to book.

#### Arguments:

* `--search` `SEARCH`
    + Search for Campgrounds or Recreation Areas by search string.
* `--state` `STATE`
    + Filter by US state code.
* `--rec-area`: `RECREATION_AREA_ID`
    + Add Recreation Areas (comprised of campgrounds) by ID.
* `--campground`: `CAMPGROUND_ID`
    + Add individual Campgrounds by ID.

```shell
camply campgrounds --search "Fire Tower Lookout" --state CA
```

**_see the [examples](#look-for-specific-campgrounds-by-query-string) for more information_

### configure

Set up `camply` configuration file with an interactive console

In order to send notifications through `camply` you must set up some authorization values. Whether
you need to set up [Pushover notifications](https://pushover.net)
, [PushBullet](https://www.pushbullet.com/#settings/account), [Telegram](https://core.telegram.org/bots),
or Email messages, everything can be done through the `configure` command. The end result is a file called
[`.camply`](docs/examples/example.camply) in your home folder. See
the [Running in Docker](#running-in-docker) section to see how you can use environment variables
instead of a config file.

```shell
camply configure
```

### Examples

Read through the examples below to get a better understanding of `camply`, its features, and the
functionality of the different arguments provided to the CLI.

#### Searching for a Campsite

The below search looks for campsites inside of Recreation Area ID #2725 (Glacier National Park)
between 2023-07-10 and 2023-07-17. The search will be performed once and any results will be logged
to the console. camply searches for campsites inside of search windows in increments of one night.
`--start-date` and `--end-date` define the bounds of the search window, you will be leaving the day
after `--end-date`.

```shell
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18
```

#### Searching for a Campsite by Campground ID

The below search looks for across three campgrounds (all inside Glacier National Park)
between 2023-07-10 and 2023-07-17. Multiple Campgrounds (and Recreation Areas too) can be found by
supplying the arguments more than once.

```shell
camply campsites \
    --campground 232493 \
    --campground 251869 \
    --campground 232492 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18
```

#### Searching for a Specific Campsite by ID

Sometimes you have a favorite campsite inside your favorite campground. To search for just a
specific campsite (and not just all campsites within a campground) you can give its ID to `camply`
with the `--campsite` argument. For example, site `R035` in Many Glacier Campground, MT is close to
a trailhead. Its URL
is [https://www.recreation.gov/camping/campsites/98363](https://www.recreation.gov/camping/campsites/98363)
, here we can see that it's ID is `98363`. You can search for one or many campsites by ID by
supplying the `--campsite` argument. You can provide the `--campsite` argument once or multiple
times to search for different campsites. Note, `--campsite` arguments override any `--rec-area`
or `--campground` parameters provided.

```shell
camply campsites \
    --campsite 98363 \
    --start-date 2023-07-10 \
    --end-date 2023-07-18
```

#### Continuously Searching for A Campsite

Sometimes you want to look for campgrounds until an eventual match is found. The below snippet will
search for matching campsites until it finds a match. It also sends a notification via `pushover`
once matches are found. Alternate notification methods are `email`, `pushbullet`, `telegram`, and `silent` (
default).

__Important Note__: When `camply` is told to run `--continuous` with non-silent notifications set up
and it finds more than 5 matching campsites on the first try, it will only send notifications for
the first 5 campsites. This is to prevent thousands of campsites flooding your notifications. It's
always encouraged to perform an initial online search before setting up a `camply` search. To bypass
this behavior and send all notifications, pass the `--notify-first-try` argument.

```shell
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-12 \
    --end-date 2023-07-13 \
    --continuous \
    --notifications pushover \
    --notify-first-try
```

#### Continue Looking After The First Match Is Found

Sometimes you want to search for all possible matches up until your arrival date. No problem. Add
the `--search-forever` and `camply` won't stop sending notifications after the first match is found.
One important note, `camply` will save and store all previous notifications when `--search-forever`
is enabled, so it won't notify you about the exact same campsite availability twice. This can be
problematic when certain campsites become available more than once.

```shell
camply campsites \
    --rec-area 2725 \
    --start-date 2023-07-01 \
    --end-date 2023-08-01 \
    --continuous \
    --notifications pushover \
    --search-forever
```

#### Send a Push Notification

camply supports notifications via `Pushbullet`, `Pushover`, `Telegram`, and `Email`. Pushbullet is a great
option because it's
a [free and easy service to sign up for](https://www.pushbullet.com/#settings/account)
and it supports notifications across different devices and operating systems. Similar to `Pushover`,
`Pushbullet` requires that you create an account and an API token, and share that token with camply
through a [configuration file](docs/examples/example.camply) (via the `camply configure`
command) or though environment variables (`PUSHBULLET_API_TOKEN`).

```shell
camply campsites \
    --rec-area 2991 \
    --start-date 2023-09-10 \
    --end-date 2023-09-21 \
    --continuous \
    --notifications pushbullet
```

#### Send a Text Message

If you want to sign up for a [Twilio](https://www.twilio.com/try-twilio) account, camply also supports
sending text messages via SMS. You can set up your Twilio configuration via `camply configure`. You will need
to set the following config values for Twilio: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`,
`TWILIO_SOURCE_NUMBER`, `TWILIO_DEST_NUMBERS`.

Sending text messages via Twilio also requires the `twilio` extras:

```
pip install camply[twilio]
```

```shell
camply campsites \
    --rec-area 2991 \
    --start-date 2023-09-10 \
    --end-date 2023-09-21 \
    --continuous \
    --notifications twilio
```

#### Send a Notification to Different Services

camply supports notifications from different providers. To send notifications to multiple providers
you can pass the --notifications parameter multiple times. YAML config entries also
accept an array as well.

```shell
camply campsites \
    --rec-area 2991 \
    --start-date 2023-09-10 \
    --end-date 2023-09-21 \
    --continuous \
    --notifications email \
    --notifications pushover
```

#### Look for Weekend Campsite Availabilities

This below search looks across larger periods of time, but only if a campground is available to book
on a Friday or Saturday night (`--weekends`). It also uses the `--polling-interval` argument which
checks every 5 minutes instead of the default 10 minutes.

```shell
camply campsites \
    --rec-area 2991 \
    --start-date 2023-05-01 \
    --end-date 2023-08-01 \
    --weekends \
    --continuous \
    --notifications email \
    --polling-interval 5
```

#### Look for Consecutive Nights at the Same Campsite

A lot of times you need to search for consecutive nights at the same campsite. By default, any and
all campsites with a single nights booking are returned by camply. To search for campsites with
consecutive night stays, pass the `--nights` argument.

Note, the `--nights` argument handles issues with improper search parameters. For example, if you
set the `--weekends` parameter the maximum number of consecutive nights possible is 2. If you supply
more than this your `--nights` parameter will be overwritten to 2.

```shell
camply campsites \
    --rec-area 2991 \
    --start-date 2023-05-01 \
    --end-date 2023-08-01 \
    --nights 4
```

#### Look for a Campsite Inside of Yellowstone

Yellowstone doesn't use https://recreation.gov to manage its campgrounds, instead it uses its own
proprietary system. In order to search the Yellowstone API for campsites, make sure to pass
the `--provider "yellowstone"` argument. This flag disables `--rec-area` argument.

To learn more about using `camply` to find campsites at Yellowstone, check out
this [discussion](https://github.com/juftin/camply/discussions/15#discussioncomment-783657).

```shell
camply campsites \
    --provider yellowstone \
    --start-date 2023-07-09 \
    --end-date 2023-07-17 \
    --continuous
```

#### Look for a Campsite Across Multiple Recreation areas

You don't have to confine your search to a single Recreation or Campground ID. Adding multiple
arguments to the command line will search across multiple IDs. Keep in mind that any `--campground`
arguments will overwrite all `--rec-area` arguments.

```shell
camply campsites \
    --rec-area 2991 \
    --rec-area 1074 \
    --start-date 2023-07-09 \
    --end-date 2023-07-17 \
    --nights 5
```

#### Using a YAML Configuration file to search for campsites

Sometimes, using a YAML configuration file is easier to manage all of your search options. See the
below [YAML example file](docs/examples/example_search.yaml) and corresponding camply command:

```yaml
provider:         RecreationDotGov  # RecreationDotGov IF NOT PROVIDED
recreation_area: # (LIST OR SINGLE ENTRY)
  - 2991  # Yosemite National Park, CA (All Campgrounds)
  - 1074  # Sierra National Forest, CA (All Campgrounds)
campgrounds:      null  # ENTIRE FIELD CAN BE OMITTED IF NOT USED - (LIST OR SINGLE ENTRY)
campsites:        null   # OVERRIDES CAMPGROUNDS / RECREATION AREA - (LIST OR SINGLE ENTRY)
start_date:       2023-09-12  # YYYY-MM-DD
end_date:         2023-09-13  # YYYY-MM-DD
weekends:         false  # FALSE BY DEFAULT
nights:           1  # 1 BY DEFAULT
continuous:       true  # DEFAULTS TO TRUE
polling_interval: 5  # DEFAULTS TO 10 , CAN'T BE LESS THAN 5
notifications:    email  # (silent, email, pushover, pushbullet, and telegram), DEFAULTS TO `silent`
search_forever:   true  # FALSE BY DEFAULT
notify_first_try: false  # FALSE BY DEFAULT
equipment:        null # Array of Equipment Search Lists - DEFAULTS TO `null`
offline_search: false    # FALSE BY DEFAULT
offline_search_path: camply_campsites.json # Defaults to `camply_campsites.json`
```

```shell
camply campsites --yaml-config example_search.yaml
```

#### Searching for a Campsite That Fits Your Equipment

Camply can help you filter campsites to fit your specific equipment, like a Trailer or an RV.
Most likely, you care that the campsite fits the length of your RV so you can specify that as well.
To search for specific equipment and its length provide the `--equipment` option with two arguments,
the equipment name and the equipment length. If you don't want to filter based on length provide a
length of zero. If you provide multiple `--equipment` options, sites matching any of your search
equipment will be returned.

Current supported equipment names are `Vehicle`, `Tent`, `RV`, and `Trailer`. Be careful when
filtering on `Tents` and `Vehicle` length, sometimes Recreation.gov doesn't provide that information,
it is safer to set length to 0.

```shell
camply campsites \
    --rec-area 2991 \
    --start-date 2023-07-09 \
    --end-date 2023-07-17 \
    --nights 5 \
    --equipment RV 25
```

Here's what the above search would look like on a YAML Config:

```yaml
recreation_area:
    - 2991
start_date:       2023-07-09
end_date:         2023-07-17
nights:           5
equipment:
    - [RV, 25]
```

Finally, here's a search that accommodates trailers of all lengths:

```shell
camply campsites \
    --rec-area 2991 \
    --start-date 2023-07-09 \
    --end-date 2023-07-17 \
    --nights 5 \
    --equipment Trailer 0
```

#### Saving the Results of a Search

In some cases, you might want to save all the campsites found during one
search and load them into a new search, so you don't receive duplicate notifications.
This can be achieved by passing the `--offline-search` flag. By default, camply will save
the results in a file called `camply_campsites.json`.

Optionally, you can also path the `--offline-search-path` flag to specify a certain file
path to save the results as. When a file path with a `.json` extension is passed
camply will export the results as a JSON file. When the `.pkl` or `.pickle` extension is
used, camply will use a serialized Pickle file.

```shell
camply \
  campsites \
  --campground 232064 \
  --start-date 2023-09-01 \
  --end-date 2023-10-01 \
  --continuous \
  --offline-search
```

```shell
camply \
  campsites \
  --campground 232064 \
  --start-date 2023-09-01 \
  --end-date 2023-10-01 \
  --continuous \
  --offline-search \
  --offline-search-path campsites.pkl
```

#### Search for Recreation Areas by Query String

Just need to find what your local Recreation Area ID number is? This simple command allows you to
search and list recreation areas. It accepts `--search` and `--state` arguments.

```shell
camply recreation-areas --search "Yosemite National Park"
```

#### Look for Specific Campgrounds Within a Recreation Area

Need to get even more specific and search for a particular campground? This search lists campgrounds
attached to a recreation area id `--rec-area`. It also accepts `--search` and `--state`
arguments.

```shell
camply campgrounds --rec-area 2991
```

#### Look for Specific Campgrounds by Query String

The below search looks for Fire Lookout Towers to stay in inside of California.

```shell
camply campgrounds --search "Fire Tower Lookout" --state CA
```

## Finding Recreation Areas IDs and Campground IDs To Search Without Using the Command Line

You can uncover campground and recreation area IDs just by using the https://recreation.gov search
functionality. Use the below example for a campground within Glacier National Park.

First, perform your search on https://recreation.gov.

<div>
<img src="https://raw.githubusercontent.com/juftin/camply/main/docs/source/_static/recreation_dot_gov.png"
    width="500" alt="recreation_dot_gov search">
</div>

The above search will take you to a URL like this:
https://www.recreation.gov/search?q=Glacier%20National%20Park&entity_id=2725&entity_type=recarea.
Taking a closer look at the URL components you can see that Glacier National Park has the Recreation
Area ID #2725.

Searching deeper into campgrounds inside of Glacier National Park you might find Fish Creek
Campground at a URL like https://www.recreation.gov/camping/campgrounds/232493. Here, we can see
that this campground has a Campground ID of #232493.

## Object-Oriented Usage (Python)

### Search for a Recreation.gov Campsite

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

### Continuously Search for Recreation.gov Campsites

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

## Running in Docker

Here's an example of a detached container searching in the background (notice the `-d` flag, the
container will run detached).

```shell
docker run -d \
  --name camply-detached-example \
  --env PUSHOVER_PUSH_TOKEN=${PUSHOVER_PUSH_TOKEN} \
  --env PUSHOVER_PUSH_USER=${PUSHOVER_PUSH_USER} \
  --env TZ="America/Denver" \
  juftin/camply \
  camply campsites \
      --rec-area 2991 \
      --start-date 2023-08-01 \
      --end-date 2023-09-01 \
      --continuous \
      --notifications pushover
```

The docker image accepts the following environment variables:

- Pushover Notifications
    * `PUSHOVER_PUSH_USER`
- Email Notifications
    * `EMAIL_TO_ADDRESS`
    * `EMAIL_USERNAME`
    * `EMAIL_PASSWORD`
    * `EMAIL_FROM_ADDRESS` (defaults to "camply@juftin.com")
    * `EMAIL_SUBJECT_LINE` (defaults to "camply Notification")
    * `EMAIL_SMTP_SERVER` (defaults to "smtp.gmail.com")
    * `EMAIL_SMTP_PORT` (defaults to 465)
- Optional Environment Variables
    * `LOG_LEVEL` (sets logging level, defaults to "INFO")
    * `PUSHOVER_PUSH_TOKEN` (Personal Pushover App Token)
    * `RIDB_API_KEY` (Personal API Key
      for [Recreation.gov API](https://ridb.recreation.gov/profile))
    * `TZ` ([TZ Database Name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) for
      logging, defaults to UTC)

Alternatively, if you have already run `camply configure` locally, you can share
your [`.camply`](docs/examples/example.camply) file inside the docker container.

```shell
docker run \
  --name camply-file-share-example \
  --env TZ="America/Denver" \
  --volume ${HOME}/.camply:/home/camply/.camply \
  juftin/camply \
  camply campsites \
      --provider yellowstone \
      --start-date 2023-07-22 \
      --end-date 2023-07-27 \
      --continuous \
      --notifications email
```

To manage multiple searches (with different notification preferences) I like to use YAML
configuration files:

```shell
docker run -d \
  --name camply-email-example \
  --env TZ="America/Denver" \
  --env EMAIL_TO_ADDRESS=${EMAIL_TO_ADDRESS} \
  --env EMAIL_USERNAME=${EMAIL_USERNAME} \
  --env EMAIL_PASSWORD=${EMAIL_PASSWORD} \
  --volume example_search.yaml:/home/camply/example_search.yaml \
  juftin/camply:latest \
  camply campsites \
      --yaml-config /home/camply/example_search.yaml
```

A [docker-compose example](docs/examples/docker-compose.yaml) of the above YAML Config is also
available.

## Dependencies

`camply` is compatible with any Python version >= `3.6`. Currently, there are eight required
dependencies:

- [click](https://docs.python-requests.org/en/master/)
    - The `click` package is used to leverage it's simple Command Line Interface
      API for camply
- [requests](https://docs.python-requests.org/en/master/)
    - The `requests` package is used to fetch data from the APIs of Camping Booking Providers.
- [pandas](https://pandas.pydata.org/)
    - The `pandas` package is to group and aggregate across large data sets of campsites,
      campgrounds, and recreation areas.
- [tenacity](https://tenacity.readthedocs.io/en/latest/)
    - The `tenacity` package is used for retrying data searches on the underlying campsite APIs.
      This retrying methodology handles exceptions allowing for API downtime and facilitating
      exponential backoff.
- [rich](https://github.com/textualize/rich)
    - Colorizing the CLI
- [python-dotenv](https://github.com/theskumar/python-dotenv)
    - The `python-dotenv` package reads key-value pairs from a `.env` file and can set them as
      environment variables - this helps with the `.camply` configuration file.
- [pydantic](https://github.com/samuelcolvin/pydantic)
    - The `pydantic` package performs data validation against API responses and assists with fancy
      data containers for `camply` objects.
- [PyYAML](https://pyyaml.org/)
    - PyYAML is a YAML parsing library - this helps with the YAML file campsite searches.

<br/>

Recreation data provided by [**Recreation.gov**](https://ridb.recreation.gov/)

___________
___________

<br/>

[<p align="center" ><img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120"  alt="juftin logo"> </p>](https://github.com/juftin)
