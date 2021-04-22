#!/usr/bin/env bash

function log_bash_event() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    TIMESTAMP=$(date +"%F %T,000")
  else
    TIMESTAMP=$(date +"%F %T,%3N")
  fi

  if [[ ${1} == "info" ]]; then
    echo "${TIMESTAMP} [    INFO]: ${2}"
  elif [[ ${1} == "error" ]]; then
    echo "${TIMESTAMP} [   ERROR]: ${2}"
  elif [[ ${2} == "" ]]; then
    echo "${TIMESTAMP} [    INFO]: ${1}"
  else
    echo "${TIMESTAMP} [   ${1}]: ${2}"
  fi
}

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
ROOT_DIE=$(dirname ${SCRIPTS_DIR})

source ${YELLOWSTONE_CAMPING_DIR}/yellowstone-camping.env

DOCKER_CONTAINER_NAME="yellowstone-camping"

log_bash_event info "Running Campsite Finder Inside of Detached Docker Container: ${DOCKER_CONTAINER_NAME}"

docker stop ${DOCKER_CONTAINER_NAME} || true > /dev/null 2>&1

docker run -d --rm \
  --name "yellowstone-camping" \
  --env BOOKING_DATE_START=${BOOKING_DATE_START} \
  --env NUMBER_OF_GUESTS=${NUMBER_OF_GUESTS} \
  --env NUMBER_OF_NIGHTS=${NUMBER_OF_NIGHTS} \
  --env POLLING_INTERVAL=${POLLING_INTERVAL} \
  --env PUSHOVER_PUSH_TOKEN=${PUSHOVER_PUSH_TOKEN} \
  --env PUSHOVER_PUSH_USER=${PUSHOVER_PUSH_USER} \
  --env PYTHONPATH="${PYTHONPATH}:/home/yellowstone-camping/" \
  --env TZ=${TIMEZONE_DB_NAME} \
  --volume ${YELLOWSTONE_CAMPING_DIR}:"/home/yellowstone-camping/" \
  --workdir "/home/yellowstone-camping/" \
  --entrypoint "/home/yellowstone-camping/scripts/docker-entrypoint.sh" \
  python:3.8-slim-buster \
  python scripts/find_availabilities.py

log_bash_event info "[ATTENTION]"
log_bash_event info "Attaching to ${DOCKER_CONTAINER_NAME} logs."
log_bash_event info "EXITING THE LOGS DOES NOT STOP THE CAMPSITE SEARCH"
log_bash_event info "Use the following command to kill the search: docker stop ${DOCKER_CONTAINER_NAME}"

docker logs -f ${DOCKER_CONTAINER_NAME}
