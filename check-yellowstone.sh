#!/usr/bin/env bash

YELLOWSTONE_CAMPING_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
source ${YELLOWSTONE_CAMPING_DIR}/yellowstone-camping.env

docker run --rm \
  --name "yellowstone-camping" \
  --volume ${YELLOWSTONE_CAMPING_DIR}:"/home/yellowstone-camping/" \
  --env BOOKING_DATE_START=${BOOKING_DATE_START} \
  --env NUMBER_OF_GUESTS=${NUMBER_OF_GUESTS} \
  --env NUMBER_OF_NIGHTS=${NUMBER_OF_NIGHTS} \
  --env POLLING_INTERVAL=${POLLING_INTERVAL} \
  --env PUSHOVER_PUSH_TOKEN=${PUSHOVER_PUSH_TOKEN} \
  --env PUSHOVER_PUSH_USER=${PUSHOVER_PUSH_USER} \
  --workdir "/home/yellowstone-camping/" \
  --entrypoint "/home/yellowstone-camping/docker-entrypoint.sh" \
  python:3.8-slim-buster \
  python check_yellowstone.py
