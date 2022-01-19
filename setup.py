#!/usr/bin/env python3

"""
Python Packaging Configuration File

Package Settings configured and inferred from setup.cfg
"""

from pathlib import Path
from typing import List

from setuptools import setup


def parse_requirements_file(filename: str) -> List[str]:
    """
    Parse a Requirements File Into Package Dependency List

    Ignore comments (on their own line or after the dependency)
    and empty lines
    """
    requirements_list = []
    try:
        with open(filename, "r", encoding="utf-8") as text_stream:
            requirements_body = text_stream.read()
    except FileNotFoundError:
        return []
    for requirement in requirements_body.splitlines():
        text_requirement = str(requirement).strip()
        if "#" in text_requirement and not text_requirement.startswith("#"):
            text_requirement = text_requirement.split("#")[0].strip()
        if text_requirement != "" and not text_requirement.startswith("#"):
            requirements_list.append(requirement)
    return requirements_list


_requirements_file = Path(__file__).resolve().parent.joinpath("requirements.txt")
_install_requires = parse_requirements_file(filename=str(_requirements_file))

setup(install_requires=_install_requires)
