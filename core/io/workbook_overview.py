# -*- coding: utf-8 -*-

"""Use to present workbook data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QWidget,
    QDialog,
    QListWidgetItem,
)
from typing import Callable, Any
from .Ui_workbook_overview import Ui_Dialog

class WorkbookOverview(QDialog, Ui_Dialog):
    
    """Put all the data into this dialog!!
    
    User cannot change anything in this interface.
    """
    
    def __init__(self, parent: QWidget, commit, decompress: Callable[[str], Any]):
        """Data come from commit."""
        super(WorkbookOverview, self).__init__(parent)
        self.setupUi(self)
        """Window title"""
        self.setWindowTitle("{} - commit #{}".format(
            commit.branch.name,
            commit.id
        ))
        """Expression of main canvas."""
        expr = decompress(commit.mechanism)
        item = QListWidgetItem("[Main canvas]")
        item.setToolTip("{}...".format(expr[:50]))
        self.storage_list.addItem(item)
        """Expression of storage data."""
        for name, expr in decompress(commit.storage):
            item = QListWidgetItem("[Storage] - {}".format(name))
            item.setToolTip(expr)
            self.storage_list.addItem(item)
        """Expression of inputs variable data."""
        for expr in decompress(commit.inputsdata):
            self.variables_list.addItem("Point{}->{}->{}".format(*expr))
        """Path data."""
        for name, paths in decompress(commit.pathdata).items():
            item = QListWidgetItem(name)
            item.setToolTip(", ".join(
                '[{}]'.format(i) for i, path in enumerate(paths) if path
            ))
            self.records_list.addItem(item)
        """Structure collections."""
        for edges in decompress(commit.collectiondata):
            self.structures_list.addItem(str(edges))
        """Triangle collections."""
        for name, data in decompress(commit.triangledata).items():
            item = QListWidgetItem(name)
            item.setToolTip(data['Expression'])
            self.triangular_iteration_list.addItem(item)
        """Dimensional synthesis."""
        for data in decompress(commit.algorithmdata):
            self.results_list.addItem(data['Algorithm'])
