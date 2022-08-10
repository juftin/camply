FROM python:3.9-slim

MAINTAINER Justin Flannery <juftin@juftin.com>
LABEL description="camply, the campsite finder"

COPY . /tmp/camply
RUN cd /tmp/camply/ && python /tmp/camply/setup.py install && rm -rf /tmp/camply/

ENV HOME=/home/camply
RUN mkdir ${HOME}
WORKDIR ${HOME}

ENV CAMPLY_LOG_HANDLER="PYTHON"

CMD camply
