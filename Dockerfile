FROM python:3.9-slim

MAINTAINER Justin Flannery <juftin@juftin.com>

COPY . /tmp/project

RUN pip install /tmp/project && \
    rm -rf /tmp/project
