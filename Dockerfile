FROM python:3.8-slim

MAINTAINER Justin Flannery <justin.flannery@livongo.com>
LABEL version="0.1.0"
LABEL description="camply, the campsite finder"

COPY . /home/camply
RUN cd /home/camply/ && python setup.py install

CMD camply