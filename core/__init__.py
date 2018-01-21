# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"core" module will load necessaries when startup.
"""

#['INFO', 'args', 'Pyslvs_Splash']
from .info import *
from .server import startRep
ImportTest = "All modules are loaded."
try:
    from .main import MainWindow
except ImportError as e:
    MainWindow = None
    ImportTest = str(e)

__all__ = [
    'ImportTest',
    'INFO',
    'args',
    'startRep',
    'MainWindow',
    'Pyslvs_Splash'
]
