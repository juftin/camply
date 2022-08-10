FROM python:3.9-slim

MAINTAINER Justin Flannery <juftin@juftin.com>
LABEL description="camply, the campsite finder"

COPY pyproject.toml /tmp/camply/pyproject.toml
COPY camply/ /tmp/camply/camply/
COPY README.md /tmp/camply/README.md
RUN cd /tmp/camply/ && python -m pip install /tmp/camply/ && rm -rf /tmp/camply/

ENV HOME=/home/camply
RUN mkdir ${HOME}
WORKDIR ${HOME}
ENV CAMPLY_LOG_HANDLER="PYTHON"

CMD camply
