# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"core" module will load necessaries when startup.
"""

from .info import (
    ARGUMENTS,
    INFO,
    PyslvsSplash
)
from .main import MainWindow

__all__ = [
    'MainWindow',
    'ARGUMENTS',
    'INFO',
    'PyslvsSplash',
]
