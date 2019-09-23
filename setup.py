# -*- coding: utf-8 -*-

"""Compile the Cython libraries of Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from os.path import (
    abspath,
    dirname,
    join as pth_join,
)
import re
import codecs
from setuptools import setup, find_packages

here = abspath(dirname(__file__))


def read(*parts):
    with codecs.open(pth_join(here, *parts), 'r') as f:
        return f.read()


def find_version(*file_paths):
    m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", read(*file_paths), re.M)
    if m:
        return m.group(1)
    raise RuntimeError("Unable to find version string.")


version = find_version('depend', 'pyslvs', 'pyslvs', '__init__.py')
setup(
    name='pyslvs_ui',
    version=version,
    author=__author__,
    author_email=__email__,
    license=__license__,
    description="Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System.",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    url="https://github.com/KmolYuan/pyslvs",
    packages=find_packages(exclude=('depend',)),
    entry_points={'console_scripts': ['pyslvs=pyslvs_ui:main']},
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=read('requirements.txt').splitlines()
        + [f'pyslvs=={version}', 'python_solvespace'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ]
)
