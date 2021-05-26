FROM python:3.8-slim

MAINTAINER Justin Flannery <juftin@juftin.com>
LABEL version="0.1.3"
LABEL description="camply, the campsite finder"

COPY . /tmp/camply
RUN cd /tmp/camply/ && python /tmp/camply/setup.py install && rm -rf /tmp/camply/

ENV HOME=/home/camply
RUN mkdir ${HOME}
WORKDIR ${HOME}

CMD camply
