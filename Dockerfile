FROM python:3.9-slim

MAINTAINER Justin Flannery <juftin@juftin.com>
LABEL description="camply, the campsite finder"

COPY poetry.lock /tmp/camply/poetry.lock
COPY pyproject.toml /tmp/camply/pyproject.toml
COPY README.md /tmp/camply/README.md
COPY camply/ /tmp/camply/camply/
COPY requirements/prod-requirements.txt /tmp/camply/requirements.txt

RUN python -m pip install -r /tmp/camply/requirements.txt && \
    python -m pip install /tmp/camply --no-dependencies && \
    rm -rf /tmp/camply/

ENV HOME=/home/camply
RUN mkdir ${HOME}
WORKDIR ${HOME}
ENV CAMPLY_LOG_HANDLER="PYTHON"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN _CAMPLY_COMPLETE=bash_source camply > /root/.camply-complete.bash && \
    echo "[[ ! -f /root/.camply-complete.bash ]] || source /root/.camply-complete.bash" >> /root/.bashrc

CMD ["camply", "--help"]
