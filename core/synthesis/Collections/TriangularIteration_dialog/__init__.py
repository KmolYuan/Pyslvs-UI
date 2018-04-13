# -*- coding: utf-8 -*-

"""'TriangularIteration_dialog' module contains
the dialog of this tab.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .collections import CollectionsDialog
from .constraints import ConstraintsDialog, list_items
from .customs import CustomsDialog
from .targets import TargetsDialog, list_texts
from .solutions import SolutionsDialog

__all__ = [
    'CollectionsDialog',
    'ConstraintsDialog',
    'CustomsDialog',
    'TargetsDialog',
    'SolutionsDialog',
    'list_texts',
    'list_items',
]


