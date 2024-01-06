FROM python:3.11-slim

MAINTAINER Justin Flannery <juftin@juftin.com>
LABEL description="camply, the campsite finder"

COPY requirements.txt /tmp/project/requirements.txt
RUN pip install -r /tmp/project/requirements.txt

COPY README.md /tmp/project/README.md
COPY pyproject.toml /tmp/project/pyproject.toml
COPY camply /tmp/project/camply

RUN pip install /tmp/project && \
    rm -rf /tmp/project

ENV HOME=/home/camply
RUN mkdir ${HOME}
WORKDIR ${HOME}
ENV CAMPLY_LOG_HANDLER="PYTHON"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN _CAMPLY_COMPLETE=bash_source camply > ${HOME}/.camply-complete.bash && \
    echo "[[ ! -f ${HOME}/.camply-complete.bash ]] || source ${HOME}/.camply-complete.bash" >> ${HOME}/.bashrc

CMD ["camply", "--help"]
