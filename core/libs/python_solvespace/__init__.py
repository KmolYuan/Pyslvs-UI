# -*- coding: utf-8 -*-

"""'python_solvespace' module is a wrapper of
Python binding Solvespace solver libraries.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .planarSolving import (
    slvsProcess,
    SlvsException
)

__all__ = [
    'slvsProcess',
    'SlvsException',
]
