FROM python:3.9-slim as python-base

FROM python-base as builder

ENV POETRY_VERSION=1.2.1
RUN python -m pip install --upgrade pip wheel
RUN python -m pip install poetry==${POETRY_VERSION}

COPY poetry.lock /tmp/camply/poetry.lock
COPY pyproject.toml /tmp/camply/pyproject.toml
COPY README.md /tmp/camply/README.md
COPY camply/ /tmp/camply/camply/

RUN cd /tmp/camply/ && poetry export -f requirements.txt --ansi --without-hashes --extras all -o /tmp/camply/requirements.txt

FROM python-base as final

MAINTAINER Justin Flannery <juftin@juftin.com>
LABEL description="camply, the campsite finder"

COPY --from=builder /tmp/camply/ /tmp/camply/

RUN python -m pip install -r /tmp/camply/requirements.txt && \
    python -m pip install /tmp/camply --no-dependencies && \
    rm -rf /tmp/camply/

RUN mkdir /home/camply
WORKDIR /home/camply
ENV CAMPLY_LOG_HANDLER="PYTHON"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN _CAMPLY_COMPLETE=bash_source camply > /root/.camply-complete.bash && \
    echo "[[ ! -f /root/.camply-complete.bash ]] || source /root/.camply-complete.bash" >> /root/.bashrc

CMD ["camply", "--help"]
