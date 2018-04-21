# -*- coding: utf-8 -*-

"""'pyslvs_topologic' module contains
number synthesis and type synthesis libraries.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .number import NumberSynthesis
from .topologic import topo, Graph
from .triangulation import vpoints_configure

__all__ = [
    'NumberSynthesis',
    'topo',
    'Graph',
    'vpoints_configure',
]
