# -*- coding: utf-8 -*-

"""Use to present project data."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, Sequence, Mapping, Any
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QDialog, QListWidgetItem
from qtpy.QtGui import QPixmap
from .overview_ui import Ui_Dialog

_Paths = Sequence[Sequence[Tuple[float, float]]]
_Pairs = Sequence[Tuple[int, int]]


class OverviewDialog(QDialog, Ui_Dialog):
    """Put all the data into this dialog!!

    User cannot change anything in this interface.
    """

    def __init__(
        self,
        parent: QWidget,
        title: str,
        main_expr: str,
        storage_data: Mapping[str, str],
        input_data: Sequence[Tuple[int, int]],
        path_data: Mapping[str, _Paths],
        collection_data: Sequence[_Pairs],
        config_data: Mapping[str, Mapping[str, Any]],
        algorithm_data: Sequence[Mapping[str, Any]],
        background_path: str
    ):
        """Data come from commit."""
        super(OverviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle(f"Project: {title}")

        # Expression of storage data
        self.main_expr.setText(main_expr)
        for name, expr in storage_data.items():
            item = QListWidgetItem(f"[{name}]: {expr}")
            item.setToolTip(expr)
            self.storage_list.addItem(item)
        size = len(storage_data)
        if main_expr != "M[]":
            size += 1
        self.__set_item_text(0, size)
        # Expression of inputs variable data and Path data
        for a, b in input_data:
            self.variables_list.addItem(f"Point{a}->Point{b}")
        for name, paths in path_data.items():
            item = QListWidgetItem(name)
            item.setToolTip(", ".join(
                f'[{i}]' for i, path in enumerate(paths) if path
            ))
            self.records_list.addItem(item)
        self.__set_item_text(1, len(input_data), len(path_data))
        # Structure collections and Triangle collections
        for edges in collection_data:
            self.structures_list.addItem(str(edges))
        for name, data in config_data.items():
            item = QListWidgetItem(name)
            item.setToolTip(data['expression'])
            self.triangular_iteration_list.addItem(item)
        self.__set_item_text(2, len(collection_data), len(config_data))
        # Dimensional synthesis
        for data in algorithm_data:
            self.results_list.addItem(data['algorithm'])
        self.__set_item_text(3, len(algorithm_data))
        # Background image
        self.image_path.setText(background_path)
        self.__set_item_text(4, 1 if background_path else 0)
        self.background_preview.setPixmap(QPixmap(background_path))

    def __set_item_text(self, i: int, *count: int) -> None:
        """Set the title for a specified tab."""
        text = " / ".join(str(c) for c in count)
        self.tab_box.setItemText(i, f"{self.tab_box.itemText(i)} - ({text})")
