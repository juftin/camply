FROM python:3.9-slim

COPY pyproject.toml /tmp/camply/pyproject.toml
COPY README.md /tmp/camply/README.md
COPY camply/ /tmp/camply/camply/

MAINTAINER Justin Flannery <juftin@juftin.com>
LABEL description="camply, the campsite finder"

COPY requirements/requirements-prod.txt /tmp/camply/requirements.txt

RUN python -m pip install -r /tmp/camply/requirements.txt && \
    python -m pip install /tmp/camply --no-dependencies && \
    rm -rf /tmp/camply/

ENV HOME=/home/camply
RUN mkdir ${HOME}
WORKDIR ${HOME}
ENV CAMPLY_LOG_HANDLER="PYTHON"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN _CAMPLY_COMPLETE=bash_source camply > ${HOME}/.camply-complete.bash && \
    echo "[[ ! -f ${HOME}/.camply-complete.bash ]] || source ${HOME}/.camply-complete.bash" >> ${HOME}/.bashrc

CMD ["camply", "--help"]
