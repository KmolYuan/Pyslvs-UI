# -*- coding: utf-8 -*-

"""Use to present workbook data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QWidget,
    QDialog,
)
from .Ui_workbook_overview import Ui_Dialog

class WorkbookOverview(QDialog, Ui_Dialog):
    
    """Put all the data into this dialog!!
    
    User cannot change anything in this interface.
    """
    
    def __init__(self, parent: QWidget, commit):
        """Data come from commit."""
        super(WorkbookOverview, self).__init__(parent)
        self.setupUi(self)
