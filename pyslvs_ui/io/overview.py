# -*- coding: utf-8 -*-

"""Use to present workbook data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Sequence,
    Dict,
    Any,
)
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QDialog, QListWidgetItem
from .overview_ui import Ui_Dialog


class OverviewDialog(QDialog, Ui_Dialog):

    """Put all the data into this dialog!!

    User cannot change anything in this interface.
    """

    def __init__(
        self,
        parent: QWidget,
        title: str,
        storage_data: Dict[str, str],
        input_data: Sequence[Tuple[int, int]],
        path_data: Dict[str, Sequence[Tuple[float, float]]],
        collection_data: List[Tuple[Tuple[int, int], ...]],
        config_data: Dict[str, Dict[str, Any]],
        algorithm_data: List[Dict[str, Any]]
    ):
        """Data come from commit."""
        super(OverviewDialog, self).__init__(parent)
        self.setupUi(self)
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(f"Project: {title}")

        # Expression of storage data.
        for name, expr in storage_data.items():
            item = QListWidgetItem(f"[Storage] - {name}")
            item.setToolTip(expr)
            self.storage_list.addItem(item)
        self.__set_item_text(0, len(storage_data))

        # Expression of inputs variable data and Path data.
        for a, b in input_data:
            self.variables_list.addItem(f"Point{a}->Point{b}")
        for name, paths in path_data.items():
            item = QListWidgetItem(name)
            item.setToolTip(", ".join(
                f'[{i}]' for i, path in enumerate(paths) if path
            ))
            self.records_list.addItem(item)
        self.__set_item_text(1, len(input_data), len(path_data))

        # Structure collections and Triangle collections.
        for edges in collection_data:
            self.structures_list.addItem(str(edges))
        for name, data in config_data.items():
            item = QListWidgetItem(name)
            item.setToolTip(data['Expression'])
            self.triangular_iteration_list.addItem(item)
        self.__set_item_text(2, len(collection_data), len(config_data))

        # Dimensional synthesis.
        for data in algorithm_data:
            self.results_list.addItem(data['Algorithm'])
        self.__set_item_text(3, len(algorithm_data))

    def __set_item_text(self, i: int, *count: int) -> None:
        """Set the title for a specified tab."""
        text = " / ".join(str(c) for c in count)
        self.toolBox.setItemText(i, f"{self.toolBox.itemText(i)} - ({text})")
