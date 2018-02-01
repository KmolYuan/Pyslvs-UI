# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang [pyslvs@gmail.com]

"""
"TriangularIteration_dialog" module contains the dialog of this page.
""" 

from .collections import CollectionsDialog
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
    'list_texts',
    'combo_texts',
]


