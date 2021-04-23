#!/usr/bin/env bash

set -e

DOCKER_HELPER="docker-helper.sh"
SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
source "${SCRIPTS_DIR}/${DOCKER_HELPER}"

run_camply_app "yellowstone-camping" "python scripts/find_yellowstone.py" "-d"
