# -*- coding: utf-8 -*-

from os import path

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

install_requires = ["pandas",
                    "python-dotenv",
                    "pytz",
                    "requests",
                    "tenacity"]

entry_points = {"console_scripts": ["camply = camply.utils.camply_cli:main"]}

root_directory = path.abspath(path.dirname(__file__))
with open(path.join(root_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup_kwargs = {
    "name": "camply",
    "version": "0.1.0",
    "description": "camply, the campsite finder",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
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
