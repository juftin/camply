FROM python:3.8-slim-buster
COPY . /home/camply
RUN cd /home/camply/ && python setup.py install
CMD camply