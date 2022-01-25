#!/usr/bin/env bash

set -ex

camply recreation-areas --search "Yosemite National Park"
camply campgrounds --rec-area 2991
camply campgrounds --search "Fire Tower Lookout" --state CA
camply campsites --rec-area 2991 --start-date 2022-09-15 --end-date 2022-09-17
camply campsites --campground 252037 --start-date 2022-09-15 --end-date 2022-09-17
camply campsites --yml-config tests/yml/example_search.yml
camply campsites --campground 232045 --start-date 2022-07-15 --end-date 2022-10-01 --nights 5
camply campsites --provider yellowstone --start-date 2022-10-10 --end-date 2022-10-16
camply campsites --campsite 40107 --start-date 2022-09-15 --end-date 2022-09-17
camply campgrounds --campsite 40107
