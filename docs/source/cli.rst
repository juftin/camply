##################
camply CLI
##################

.. code-block:: console

    ❯ camply
    2022-04-27 00:48:04,415 [  CAMPLY]: camply, the campsite finder ⛺️
    Usage: camply [OPTIONS] COMMAND [ARGS]...

      Welcome to camply, the campsite finder.

      Finding reservations at sold out campgrounds can be tough. That's where
      camply comes in. It searches the APIs of booking services like
      https://recreation.gov (which indexes thousands of campgrounds across the
      USA) to continuously check for cancellations and availabilities to pop up.
      Once a campsite becomes available, camply sends you a notification to book
      your spot!

      visit the camply documentation at https://github.com/juftin/camply

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      campgrounds       Search for Campgrounds (inside of Recreation Areas)...
      campsites         Find available Campsites using search criteria
      configure         Set up camply configuration file with an interactive...
      recreation-areas  Search for Recreation Areas and list them

    2022-04-27 00:48:04,416 [  CAMPLY]: Exiting camply 👋


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

.. click:: camply.cli:camply_command_line
   :prog: camply
   :nested: full