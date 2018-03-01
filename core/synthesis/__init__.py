# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"synthesis" module contains synthesis functional interfaces.
"""

from .Collections import Collections, CollectionsDialog
from .NumberAndTypeSynthesis import NumberAndTypeSynthesis
from .DimensionalSynthesis import DimensionalSynthesis

__all__ = [
    'NumberAndTypeSynthesis',
    'Collections',
    'CollectionsDialog',
    'DimensionalSynthesis'
]
