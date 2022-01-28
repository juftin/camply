##################
camply CLI
##################

.. code-block:: console

    ❯ camply

    2022-01-27 20:04:31,725 [  CAMPLY]: camply, the campsite finder ⛺️
    usage: camply [-h] [--version] {campsites,recreation-areas,campgrounds,configure} ...

    Welcome to camply, the campsite finder. Finding reservations at sold out campgrounds can be tough. That's where camply comes in. It searches the APIs of booking services like https://recreation.gov
    (which indexes thousands of campgrounds across the USA) to continuously check for cancellations and availabilities to pop up. Once a campsite becomes available, camply sends you a notification to book
    your spot!

    positional arguments:
    {campsites,recreation-areas,campgrounds,configure}
    campsites           Find available Campsites using search criteria
    recreation-areas    Search for Recreation Areas and list them
    campgrounds         Search for Campgrounds (inside of Recreation Areas) and list them
    configure           Set up camply configuration file with an interactive console

    optional arguments:
    -h, --help            show this help message and exit
    --version             show program's version number and exit

    visit the camply documentation at https://github.com/juftin/camply
    2022-01-27 20:04:31,729 [  CAMPLY]: Exiting camply 👋

******************
Installation
******************

To use camply, first install it using pip:

.. code-block:: console

    pip install camply

Run via Docker
==============

.. code-block:: console

    docker pull juftin/camply

.. code-block:: console

    docker run \
        juftin/camply:latest \
        camply recreation-areas search --state CO

******************
Documentation
******************

.. argparse::
   :module: camply.utils.camply_cli
   :func: _get_parser_object
   :prog: camply
