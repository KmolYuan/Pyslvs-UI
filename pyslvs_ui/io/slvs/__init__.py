# -*- coding: utf-8 -*-

"""'slvs' module contains IO support functions of Solvespace format."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .read import SlvsParser
from .frame import slvs_frame
from .part import slvs_part, boundary_loop

__all__ = [
    'SlvsParser',
    'slvs_frame',
    'slvs_part',
    'boundary_loop',
]
