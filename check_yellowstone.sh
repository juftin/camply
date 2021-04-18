#!/usr/bin/env bash

docker run -d --rm \
  --name "yellowstone-camping" \
  --volume ${PWD}:"/home/yellowstone-camping/" \
  --workdir "/home/yellowstone-camping/" \
  --entrypoint "/home/yellowstone-camping/docker-entrypoint.sh" \
  --env-file "${PWD}/.env" \
  python:3.8.3
