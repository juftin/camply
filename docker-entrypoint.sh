#!/usr/bin/env bash

python -m pip install --upgrade pip
pip install requests
PARENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
${PARENT_DIR}/check_yellowstone.py
