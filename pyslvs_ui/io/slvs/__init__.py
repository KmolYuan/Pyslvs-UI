# -*- coding: utf-8 -*-

"""'slvs' module contains IO support functions of Solvespace format."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .read import SlvsParser
from .frame import slvs2_frame
from .part import slvs2_part, boundary_loop
