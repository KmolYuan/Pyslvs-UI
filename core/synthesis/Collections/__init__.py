# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"Collections" module contains the result from type synthesis and triangular iteration by users.
"""

from .main_widget import Collections
from .TriangularIteration_dialog import mechanismParams_4Bar, mechanismParams_8Bar

__all__ = ['Collections', 'mechanismParams_4Bar', 'mechanismParams_8Bar']
