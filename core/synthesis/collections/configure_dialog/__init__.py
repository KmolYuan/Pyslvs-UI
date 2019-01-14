# -*- coding: utf-8 -*-

"""'configure_dialog' module contains
the dialog of this tab.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from .collections import CollectionsDialog
from .customs import CustomsDialog
from .targets import TargetsDialog, list_texts, list_items
from .solutions import SolutionsDialog

__all__ = [
    'CollectionsDialog',
    'CustomsDialog',
    'TargetsDialog',
    'SolutionsDialog',
    'list_texts',
    'list_items',
]
