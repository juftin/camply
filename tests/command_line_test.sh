#!/usr/bin/env bash

set -ex

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
