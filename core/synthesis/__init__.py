# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"synthesis" module contains synthesis functional interfaces.
"""

#['Collections']
from .Collections import *
#['NumberAndTypeSynthesis']
from .NumberAndTypeSynthesis import *
#['DimensionalSynthesis']
from .DimensionalSynthesis import *

__all__ = [
    'NumberAndTypeSynthesis',
    'Collections',
    'DimensionalSynthesis',
    'mechanismParams_4Bar',
    'mechanismParams_8Bar'
]
