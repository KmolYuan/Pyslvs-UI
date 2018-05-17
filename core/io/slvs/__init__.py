# -*- coding: utf-8 -*-

"""'slvs' module contains IO support functions of Solvespace format."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .read import slvs_layouts
from .write import slvs_output

__all__ = [
    'slvs_layouts',
    'slvs_output',
]
