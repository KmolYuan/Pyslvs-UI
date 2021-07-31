# -*- coding: utf-8 -*-

"""'collections' module contains
the result from type synthesis and triangular iteration by users.
"""

from __future__ import annotations

__all__ = [
    'Collections',
    'StructureWidget',
    'ConfigureWidget',
    'CollectionsDialog',
]
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING, List, Tuple, Sequence, Dict, Any
from qtpy.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from qtpy.QtGui import QIcon, QPixmap
from .structure_widget import StructureWidget
from .configure_widget import ConfigureWidget
from .dialogs import CollectionsDialog

if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase


class Collections(QWidget):
    """Just a widget contains a sub tab widget."""

    def __init__(self, parent: MainWindowBase):
        """Create two widget page and using main window to make their parent."""
        super(Collections, self).__init__(parent)
        layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget(self)
        layout.addWidget(self.tab_widget)
        self.setWindowIcon(QIcon(QPixmap("icons:collections.png")))
        self.structure_widget = StructureWidget(parent)
        self.configure_widget = ConfigureWidget(
            self.structure_widget.add_collection,
            parent
        )
        self.tab_widget.addTab(
            self.structure_widget,
            self.structure_widget.windowIcon(),
            "Structures"
        )
        self.tab_widget.addTab(
            self.configure_widget,
            self.configure_widget.windowIcon(),
            "Configuration"
        )
        self.structure_widget.configure_btn.clicked.connect(
            lambda: self.tab_widget.setCurrentIndex(1)
        )
        self.structure_widget.layout_sender.connect(
            self.configure_widget.set_graph
        )

    def clear(self) -> None:
        """Clear the sub-widgets."""
        self.structure_widget.clear()
        self.configure_widget.clear()

    def collect_data(self) -> List[Sequence[Tuple[int, int]]]:
        """Return collections to database."""
        return [tuple(G.edges) for G in self.structure_widget.collections]

    def config_data(self) -> Dict[str, Dict[str, Any]]:
        """Return profiles to database."""
        return self.configure_widget.collections
