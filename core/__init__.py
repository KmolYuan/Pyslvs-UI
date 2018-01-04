# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang [pyslvs@gmail.com]

from .info.info import INFO, args
from .server.zmq_rep import startRep
try:
    from PyQt5.QtWidgets import QApplication
    from .main import MainWindow
    from .info.about import Pyslvs_Splash
    ImportTest = "All modules are loaded."
except ImportError as e:
    QApplication = None
    MainWindow = None
    Pyslvs_Splash = None
    ImportTest = str(e)
