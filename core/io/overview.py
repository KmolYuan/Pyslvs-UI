# -*- coding: utf-8 -*-

"""Use to present workbook data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Callable, Any
from peewee import Model
from core.QtModules import (
    QWidget,
    QDialog,
    QListWidgetItem,
)
from .Ui_overview import Ui_Dialog


class WorkbookOverview(QDialog, Ui_Dialog):

    """Put all the data into this dialog!!

    User cannot change anything in this interface.
    """

    def __init__(
        self,
        commit: Model,
        decompress: Callable[[bytes], Any],
        parent: QWidget
    ):
        """Data come from commit."""
        super(WorkbookOverview, self).__init__(parent)
        self.setupUi(self)
        # Window title
        self.setWindowTitle(f"{commit.branch.name} - commit # {commit.id}")
        # Expression of main canvas.
        expr = decompress(commit.mechanism)
        if len(expr) > 3:
            item = QListWidgetItem("[Main canvas]")
            item.setToolTip(f"{expr[:30]}...")
            self.storage_list.addItem(item)
        # Expression of storage data.
        storage = decompress(commit.storage)
        for name, expr in storage:
            item = QListWidgetItem(f"[Storage] - {name}")
            item.setToolTip(expr)
            self.storage_list.addItem(item)
        self.__setItemText(0, int(len(expr) > 3) + len(storage))
        # Expression of inputs variable data.
        inputs_data = decompress(commit.inputsdata)
        for a, b in inputs_data:
            self.variables_list.addItem(f"Point{a}->Point{b}")
        # Path data.
        path_data = decompress(commit.pathdata)
        for name, paths in path_data.items():
            item = QListWidgetItem(name)
            item.setToolTip(", ".join(
                f'[{i}]' for i, path in enumerate(paths) if path
            ))
            self.records_list.addItem(item)
        self.__setItemText(1, len(inputs_data), len(path_data))
        # Structure collections.
        collection_data = decompress(commit.collectiondata)
        for edges in collection_data:
            self.structures_list.addItem(str(edges))
        # Triangle collections.
        triangle_data = decompress(commit.triangledata)
        for name, data in triangle_data.items():
            item = QListWidgetItem(name)
            item.setToolTip(data['Expression'])
            self.triangular_iteration_list.addItem(item)
        self.__setItemText(2, len(collection_data), len(triangle_data))
        # Dimensional synthesis.
        algorithm_data = decompress(commit.algorithmdata)
        for data in algorithm_data:
            self.results_list.addItem(data['Algorithm'])
        self.__setItemText(3, len(algorithm_data))

    def __setItemText(self, i: int, *count: int):
        """Set the title for a specified tab."""
        text = " / ".join(str(c) for c in count)
        self.toolBox.setItemText(i, f"{self.toolBox.itemText(i)} - ({text})")
