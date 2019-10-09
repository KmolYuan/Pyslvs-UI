# -*- coding: utf-8 -*-

"""Pack the distribution of Pyslvs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

import re
from os.path import join as pth_join
from setuptools import setup, find_packages


def read(*parts):
    with open(pth_join(*parts), 'r') as f:
        return f.read()


def find_version(*file_paths):
    m = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", read(*file_paths), re.M)
    if m:
        return m.group(1)
    raise RuntimeError("Unable to find version string.")


version = find_version('pyslvs', 'pyslvs', '__init__.py')
setup(
    name='pyslvs_ui',
    version=version,
    author=__author__,
    author_email=__email__,
    license=__license__,
    description="An open source planar linkage mechanism simulation and mechanical synthesis system.",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    url="https://github.com/KmolYuan/Pyslvs-UI",
    packages=find_packages(),
    package_data={'pyslvs_ui': ['py.typed']},
    entry_points={'console_scripts': ['pyslvs=pyslvs_ui:main']},
    zip_safe=False,
    python_requires=">=3.7",
    options={'bdist_wheel': {'python_tag': 'cp37.cp38'}},
    install_requires=read('requirements.txt').splitlines() + [f'pyslvs=={version}'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Environment :: X11 Applications :: Qt",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ]
)
