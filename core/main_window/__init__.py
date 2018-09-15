# -*- coding: utf-8 -*-

"""'main_window' module contains the methods of main window.

Interface classes (ordered):
+ MainWindowUiInterface (imported from core.widget.custom)
+ EntitiesMethodInterface (entities)
+ SolverMethodInterface (solver)
+ StorageMethodInterface (storage)
+ ActionMethodInterface (actions)
+ IOMethodInterface (io)
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .main import MainWindow

__all__ = ['MainWindow']
