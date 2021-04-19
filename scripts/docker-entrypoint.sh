#!/usr/bin/env bash

set -e

PRIMARY_COMMAND="${@}"

python -m pip install --upgrade pip > /dev/null 2>&1
pip install requests > /dev/null 2>&1

exec ${PRIMARY_COMMAND}
