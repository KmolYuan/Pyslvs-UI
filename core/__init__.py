# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"core" module will load necessaries when startup.
"""

#['INFO', 'ARGUMENTS', 'Pyslvs_Splash']
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
    'ARGUMENTS',
    'startRep',
    'MainWindow',
    'Pyslvs_Splash'
]
