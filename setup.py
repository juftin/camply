# -*- coding: utf-8 -*-
from setuptools import setup

packages = ["camply",
            "camply.config",
            "camply.notifications",
            "camply.providers",
            "camply.providers.recreation_dot_gov",
            "camply.providers.xanterra",
            "camply.search",
            "camply.utils"]

package_data = {"": ["*"]}

install_requires = ["PyYAML>=3.12",
                    "pandas>=0.22.0",
                    "python-dotenv>=0.6.0",
                    "pytz>=2016.1",
                    "requests>=2.9.0",
                    "tenacity>=3.6.0"]

entry_points = {"console_scripts": ["camply = camply.utils.camply_cli:main"]}

camply_long_description = ("camply is a Campsite Reservation Finder️. Finding reservations at "
                           "sold out campgrounds can be tough. That's where camply comes in. "
                           "It scrapes the APIs of Booking Services like "
                           "https://recreation.gov (which works on thousands of campgrounds across "
                           "the USA) to continuously check for cancellations and availabilities to "
                           "pop up. Once a campsite becomes available, camply sends you a "
                           "notification to book your spot!")

setup_kwargs = {
    "name": "camply",
    "version": "0.1.0",
    "description": "camply, the campsite finder",
    "long_description": camply_long_description,
    "author": "Justin Flannery",
    "author_email": "juftin@juftin.com",
    "maintainer": "Justin Flannery",
    "maintainer_email": "juftin@juftin.com",
    "url": "https://github.com/juftin/camply",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.6",
}

setup(**setup_kwargs)
