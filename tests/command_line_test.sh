#!/usr/bin/env bash

set -ex

camply --debug recreation-areas --search "Yosemite National Park"
camply --debug campgrounds --rec-area 2991
camply --debug campgrounds --search "Fire Tower Lookout" --state CA
camply --debug campsites --rec-area 2991 --start-date 2023-09-15 --end-date 2023-09-17
camply --debug campsites --campground 252037 --start-date 2023-09-15 --end-date 2023-09-17
camply --debug campsites --yaml-config tests/yaml/example_search.yaml
camply --debug campsites --campground 232045 --start-date 2023-07-15 --end-date 2023-10-01 --nights 5
camply --debug campsites --provider yellowstone --start-date 2023-10-10 --end-date 2023-10-16
camply --debug campsites --campsite 40107 --start-date 2023-09-15 --end-date 2023-09-17
camply --debug campgrounds --campsite 40107
camply --debug campsites --yaml-config tests/yaml/example_campsite_search.yaml

camply \
  --debug \
  campsites \
  --provider yellowstone \
  --start-date 2023-09-01 \
  --end-date 2023-09-14 \
  --campground YLYF:RV

camply \
    --debug \
    campsites \
    --rec-area 2018 \
    --start-date 2023-09-09 \
    --end-date 2023-09-17 \
    --nights 3 \
    --equipment RV 25 \

camply \
  --debug \
  campsites \
  --campsite 84865 \
  --campsite 84001 \
  --start-date 2023-09-27 \
  --end-date 2023-09-28

camply --debug campsites \
  --start-date 2023-10-01 \
  --end-date 2023-10-02 \
  --campground 234779

camply --debug campgrounds --provider Yellowstone
camply --provider Yellowstone campgrounds --debug

camply \
  --debug \
  campsites \
  --campground 232064 \
  --start-date 2023-09-01 \
  --end-date 2023-10-01 \
  --offline-search \
  --offline-search-path test_file.json

camply \
  --debug \
  campsites \
  --campground 232064 \
  --start-date 2023-09-01 \
  --end-date 2023-10-01 \
  --offline-search \
  --offline-search-path test_file.json

rm test_file.json

camply \
  --debug \
  campsites \
  --campground 232064 \
  --start-date 2023-09-01 \
  --end-date 2023-10-01 \
  --offline-search \
  --offline-search-path test_file.pickle

camply \
  --debug \
  campsites \
  --campground 232064 \
  --start-date 2023-09-01 \
  --end-date 2023-10-01 \
  --offline-search \
  --offline-search-path test_file.pickle

camply \
  --debug \
  --provider goingtocamp \
  recreation-areas

camply \
  --debug \
  recreation-areas \
  --provider goingtocamp \

camply \
  --debug \
  recreation-areas \
  --provider goingtocamp \

camply \
  --debug \
  equipment-types \
  --rec-area 1 \
  --provider goingtocamp \

# Rec area: Long Point Region
# Campground: Waterford North Conservation Area
# Equipment: 1 tent
camply \
  --debug \
  --provider goingtocamp \
  campsites \
  --rec-area 1 \
  --start-date 2023-09-01 \
  --end-date 2023-09-02 \
  --equipment-id -32768 \
  --campground -2147483643 \

rm test_file.pickle
