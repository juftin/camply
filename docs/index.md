# camply

<div align="center">
<a href="https://github.com/juftin/camply">
  <img src="https://raw.githubusercontent.com/juftin/camply/main/docs/_static/camply.svg"
    width="400" height="400" alt="camply">
</a>
</div>

**`camply`**, the campsite finder ⛺️, is a tool to help you book a campsite online. Finding
reservations at sold out campgrounds can be tough. That's where camply comes in. It searches
thousands of campgrounds across the ~~USA~~ world via the APIs of booking services like
[recreation.gov](https://recreation.gov). It continuously checks for cancellations and
availabilities to pop up - once a campsite becomes available, camply sends you a notification
to book your spot!

---

---

[![PyPI](https://img.shields.io/pypi/v/camply?color=blue&label=⛺️camply)](https://github.com/juftin/camply)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camply)](https://pypi.python.org/pypi/camply/)
[![Docker Image Version](https://img.shields.io/docker/v/juftin/camply?color=blue&label=docker&logo=docker)](https://hub.docker.com/r/juftin/camply)
[![Testing Status](https://github.com/juftin/camply/actions/workflows/tests.yaml/badge.svg?branch=main)](https://github.com/juftin/camply/actions/workflows/tests.yaml)
[![GitHub License](https://img.shields.io/github/license/juftin/camply?color=blue&label=License)](https://github.com/juftin/camply/blob/main/LICENSE)
[![Black Codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)]()
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-lightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![Gitmoji](https://img.shields.io/badge/gitmoji-%20😜%20😍-FFDD67.svg)](https://gitmoji.dev)
[![Discord Chat](https://img.shields.io/static/v1?label=chat&message=discord&color=blue&logo=discord)](https://discord.gg/qZDr78kKvB)

## Table of Contents

-   [Installation](installation.md)
    -   [PyPI](installation.md#pypi)
    -   [Docker](installation.md#docker)
-   [Providers](providers.md)
    -   [RecreationDotGov](providers.md#recreationgov)
    -   [Yellowstone](providers.md#yellowstone)
    -   [GoingToCamp](providers.md#goingtocamp)
    -   [RecDotGov Tours + Tickets + Timed Entry](providers.md#recreationgov-tickets-tours-timed-entry)
-   [Command Line Usage](command_line_usage.md)
    -   [Simple Examples](command_line_usage.md#simple-examples)
    -   [providers](command_line_usage.md#providers)
    -   [campsites](command_line_usage.md#campsites)
    -   [recreation-areas](command_line_usage.md#recreation-areas)
    -   [campgrounds](command_line_usage.md#campgrounds)
    -   [configure](command_line_usage.md#configure)
    -   [test-notifications](command_line_usage.md#test-notifications)
    -   [list-campsites](command_line_usage.md#list-campsites)
    -   [tui](command_line_usage.md#tui)
    -   [Examples](command_line_usage.md#examples)
        -   [Searching for a Campsite](command_line_usage.md#searching-for-a-campsite)
        -   [Searching for a Campsite by Campground ID](command_line_usage.md#searching-for-a-campsite-by-campground-id)
        -   [Searching for a Specific Campsite by ID](command_line_usage.md#searching-for-a-specific-campsite-by-id)
        -   [Continuously Searching for A Campsite](command_line_usage.md#continuously-searching-for-a-campsite)
        -   [Searching Across Multiple Time Windows](command_line_usage.md#searching-across-multiple-time-windows)
        -   [Continue Looking After The First Match Is Found](command_line_usage.md#continue-looking-after-the-first-match-is-found)
        -   [Send a Push Notification](command_line_usage.md#send-a-push-notification)
        -   [Send a Text Message](command_line_usage.md#send-a-text-message)
        -   [Send a Notification to Different Services](command_line_usage.md#send-a-notification-to-different-services)
        -   [Searching for Specific Weekdays](command_line_usage.md#searching-for-specific-weekdays)
        -   [Send a Notification Using Apprise-Compatible Services](command_line_usage.md#send-a-notification-using-apprise-compatible-services)
        -   [Look for Weekend Campsite Availabilities](command_line_usage.md#look-for-weekend-campsite-availabilities)
        -   [Look for Consecutive Nights at the Same Campsite](command_line_usage.md#look-for-consecutive-nights-at-the-same-campsite)
        -   [Look for a Campsite Inside of Yellowstone](command_line_usage.md#look-for-a-campsite-inside-of-yellowstone)
        -   [Look for a Campsite from GoingToCamp](command_line_usage.md#look-for-a-campsite-from-goingtocamp)
        -   [Searching GoingToCamp Using Equipment](command_line_usage.md#searching-goingtocamp-using-equipment)
        -   [Look for a Campsite Across Multiple Recreation areas](command_line_usage.md#look-for-a-campsite-across-multiple-recreation-areas)
        -   [Using a YAML Configuration file to search for campsites](command_line_usage.md#using-a-yaml-configuration-file-to-search-for-campsites)
        -   [Searching for a Campsite That Fits Your Equipment](command_line_usage.md#searching-for-a-campsite-that-fits-your-equipment)
        -   [Saving the Results of a Search](command_line_usage.md#saving-the-results-of-a-search)
        -   [Search for Recreation Areas by Query String](command_line_usage.md#search-for-recreation-areas-by-query-string)
        -   [Look for Specific Campgrounds Within a Recreation Area](command_line_usage.md#look-for-specific-campgrounds-within-a-recreation-area)
        -   [Look for Specific Campgrounds by Query String](command_line_usage.md#look-for-specific-campgrounds-by-query-string)
        -   [Searching for Tickets and Timed Entries](command_line_usage.md#searching-for-tickets-and-timed-entries)
            -   [Tickets + Tours](command_line_usage.md#tickets-tours)
            -   [Timed Entry](command_line_usage.md#timed-entry)
            -   [Using the Daily Providers](command_line_usage.md#using-the-daily-providers)
        -   [Search ReserveCalifornia](command_line_usage.md#search-reservecalifornia)
        -   [Run camply as a CRON Job](command_line_usage.md#run-camply-as-a-cron-job)
-   [How to Run Camply](how_to_run.md#how-to-run-camply)
    -   [Run Modes](how_to_run.md#run-modes)
        -   [non-continuous](how_to_run.md#non-continuous)
        -   [continuous](how_to_run.md#continuous)
        -   [search-forever](how_to_run.md#search-forever)
        -   [search-once](how_to_run.md#search-once)
    -   [Running in Docker](how_to_run.md#running-in-docker)
        -   [Environment Variables](how_to_run.md#environment-variables)
-   [Finding Recreation Areas IDs and Campground IDs To Search Without Using the Command Line](command_line_usage.md#finding-recreation-areas-ids-and-campground-ids-to-search-without-using-the-command-line)
-   [Object-Oriented Usage (Python)](python.md)
    -   [Search for a Recreation.gov Campsite](python.md#search-for-a-recreationgov-campsite)
    -   [Continuously Search for Recreation.gov Campsites](python.md#continuously-search-for-recreationgov-campsites)
-   [Dependencies](dependencies.md)

<br/>

Recreation data provided by [**Recreation.gov**](https://ridb.recreation.gov/)

---

---

<br/>

[<p align="center" ><img src="https://raw.githubusercontent.com/juftin/juftin/main/static/juftin.png" width="120" height="120"  alt="juftin logo"> </p>](https://github.com/juftin)
