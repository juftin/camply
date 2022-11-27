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
[![Discord Chat](https://img.shields.io/static/v1?label=chat&message=discord&color=blue&logo=discord)](https://discord.gg/qZDr78kKvB)

## [Check Out The Docs](https://juftin.com/camply/)

## Installing

Install camply via pip:

```
pip install camply
```

## Documentation

Head over to the [camply documentation](https://juftin.com/camply/) to see what you can do!

```commandline
camply --help

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

## Contributing

Camply doesn't support your favorite campsite booking provider yet? Consider
[contributing](https://juftin.com/camply/contributing/) 😉.


## Table of Contents

- [Installation](docs/installation.md)
    * [PyPI](docs/installation.md#pypi)
    * [Docker](docs/installation.md#docker)
- [Command Line Usage](docs/command_line_usage.md)
    * [campsites](docs/command_line_usage.md#campsites)
    * [recreation-areas](docs/command_line_usage.md#recreation-areas)
    * [campgrounds](docs/command_line_usage.md#campgrounds)
    * [configure](docs/command_line_usage.md#configure)
    * [Examples](docs/command_line_usage.md#examples)
        + [Searching for a Campsite](docs/command_line_usage.md#searching-for-a-campsite)
        + [Searching for a Campsite by Campground ID](docs/command_line_usage.md#searching-for-a-campsite-by-campground-id)
        + [Searching for a Specific Campsite by ID](docs/command_line_usage.md#searching-for-a-specific-campsite-by-id)
        + [Continuously Searching for A Campsite](docs/command_line_usage.md#continuously-searching-for-a-campsite)
        + [Continue Looking After The First Match Is Found](docs/command_line_usage.md#continue-looking-after-the-first-match-is-found)
        + [Send a Push Notification](docs/command_line_usage.md#send-a-push-notification)
        + [Send a Text Message](docs/command_line_usage.md#send-a-text-message)
        + [Send a Notification to Different Services](docs/command_line_usage.md#send-a-notification-to-different-services)
        + [Look for Weekend Campsite Availabilities](docs/command_line_usage.md#look-for-weekend-campsite-availabilities)
        + [Look for Consecutive Nights at the Same Campsite](docs/command_line_usage.md#look-for-consecutive-nights-at-the-same-campsite)
        + [Look for a Campsite Inside of Yellowstone](docs/command_line_usage.md#look-for-a-campsite-inside-of-yellowstone)
        + [Look for a Campsite Across Multiple Recreation areas](docs/command_line_usage.md#look-for-a-campsite-across-multiple-recreation-areas)
        + [Using a YAML Configuration file to search for campsites](docs/command_line_usage.md#using-a-yaml-configuration-file-to-search-for-campsites)
        + [Searching for a Campsite That Fits Your Equipment](docs/command_line_usage.md#searching-for-a-campsite-that-fits-your-equipment)
        + [Saving the Results of a Search](docs/command_line_usage.md#saving-the-results-of-a-search)
        + [Search for Recreation Areas by Query String](docs/command_line_usage.md#search-for-recreation-areas-by-query-string)
        + [Look for Specific Campgrounds Within a Recreation Area](docs/command_line_usage.md#look-for-specific-campgrounds-within-a-recreation-area)
        + [Look for Specific Campgrounds by Query String](docs/command_line_usage.md#look-for-specific-campgrounds-by-query-string)
- [Finding Recreation Areas IDs and Campground IDs To Search Without Using the Command Line](docs/command_line_usage.md#finding-recreation-areas-ids-and-campground-ids-to-search-without-using-the-command-line)
- [Object-Oriented Usage (Python)](docs/python.md)
    * [Search for a Recreation.gov Campsite](docs/python.md#search-for-a-recreationgov-campsite)
    * [Continuously Search for Recreation.gov Campsites](docs/python.md#continuously-search-for-recreationgov-campsites)
- [Running in Docker](docs/docker.md)
- [Dependencies](docs/dependencies.md)
- [Contributing](docs/contributing.md)

<br/>

Recreation data provided by [**Recreation.gov**](https://ridb.recreation.gov/)

___________
___________

<br/>

[<p align="center" ><img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120"  alt="juftin logo"> </p>](https://github.com/juftin)
