#!/usr/bin/env bash

set -e

PRIMARY_COMMAND="${@}"

python -m pip install --upgrade pip
pip install requests

exec ${PRIMARY_COMMAND}
