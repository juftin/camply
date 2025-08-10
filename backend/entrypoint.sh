#!/usr/bin/env bash

set -e

cd /app/packages/db
alembic upgrade head

populate-database

exec "${@}"
