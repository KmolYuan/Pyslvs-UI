# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang [pyslvs@gmail.com]

"""
"TriangularIteration_dialog" module contains the dialog of this page.
""" 

from .collections import (
    CollectionsDialog,
    mechanismParams_4Bar,
    mechanismParams_8Bar
)
from .constrains import ConstrainsDialog
from .targets import TargetsDialog
from .solutions import SolutionsDialog

__all__ = [
    'CollectionsDialog',
    'ConstrainsDialog',
    'TargetsDialog',
    'SolutionsDialog',
    'mechanismParams_4Bar',
    'mechanismParams_8Bar',
]
