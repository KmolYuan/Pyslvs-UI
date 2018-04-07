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
from typing import (
    List,
    Callable,
    Any,
)
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
        if len(expr) > 3:
            item = QListWidgetItem("[Main canvas]")
            item.setToolTip("{}...".format(expr[:30]))
            self.storage_list.addItem(item)
        """Expression of storage data."""
        storage = decompress(commit.storage)
        for name, expr in storage:
            item = QListWidgetItem("[Storage] - {}".format(name))
            item.setToolTip(expr)
            self.storage_list.addItem(item)
        self.__setItemText(0, int(len(expr) > 3) + len(storage))
        """Expression of inputs variable data."""
        inputsdata = decompress(commit.inputsdata)
        for expr in inputsdata:
            self.variables_list.addItem("Point{}->{}->{}".format(*expr))
        """Path data."""
        pathdata = decompress(commit.pathdata)
        for name, paths in pathdata.items():
            item = QListWidgetItem(name)
            item.setToolTip(", ".join(
                '[{}]'.format(i) for i, path in enumerate(paths) if path
            ))
            self.records_list.addItem(item)
        self.__setItemText(1, len(inputsdata), len(pathdata))
        """Structure collections."""
        collectiondata = decompress(commit.collectiondata)
        for edges in collectiondata:
            self.structures_list.addItem(str(edges))
        """Triangle collections."""
        triangledata = decompress(commit.triangledata)
        for name, data in triangledata.items():
            item = QListWidgetItem(name)
            item.setToolTip(data['Expression'])
            self.triangular_iteration_list.addItem(item)
        self.__setItemText(2, len(collectiondata), len(triangledata))
        """Dimensional synthesis."""
        algorithmdata = decompress(commit.algorithmdata)
        for data in algorithmdata:
            self.results_list.addItem(data['Algorithm'])
        self.__setItemText(3, len(algorithmdata))
    
    def __setItemText(self, i: int, *count: List[int]):
        """Set the title for a specified tab."""
        self.toolBox.setItemText(i, "{} - ({})".format(
            self.toolBox.itemText(i),
            " / ".join(str(c) for c in count)
        ))
