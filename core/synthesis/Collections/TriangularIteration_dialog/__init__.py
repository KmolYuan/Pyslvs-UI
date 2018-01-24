# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"TriangularIteration_dialog" module contains the dialog of this page.
""" 

from .collections import (
    CollectionsDialog,
    mechanismParams_4Bar,
    mechanismParams_8Bar
)
from .constraints import ConstraintsDialog
from .customs import CustomsDialog
from .targets import TargetsDialog, list_texts, combo_texts
from .solutions import SolutionsDialog

__all__ = [
    'CollectionsDialog',
    'ConstraintsDialog',
    'CustomsDialog',
    'TargetsDialog',
    'SolutionsDialog',
    'mechanismParams_4Bar',
    'mechanismParams_8Bar',
    'list_texts',
    'combo_texts',
]


