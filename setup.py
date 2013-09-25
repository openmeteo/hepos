#!/usr/bin/env python

import sys
import textwrap

from setuptools import setup, find_packages
from pkg_resources import parse_version


setup(
    name="hepos",
    version="0.1.0",
    license="GPL3",
    description="Greek co-ordinate transformations using the HEPOS algorithm",
    author="Antonis Christofides",
    author_email="anthony@itia.ntua.gr",
    packages=find_packages(),
    test_suite="hepos.tests",
    install_requires=[
        "pyproj >= 1.8",
    ],
)
