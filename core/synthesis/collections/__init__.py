# -*- coding: utf-8 -*-

"""'collections' module contains
the result from type _synthesis and triangular iteration by users.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    List,
    Tuple,
    Dict,
    Any,
)
from core.QtModules import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QIcon,
    QPixmap,
)
from .structure_widget import StructureWidget
from .triangular_iteration_widget import TriangularIterationWidget
from .ti_dialog import CollectionsDialog

__all__ = ['Collections', 'CollectionsDialog']


class Collections(QWidget):

    """Just a widget contains a sub tab widget."""

    def __init__(self, parent: QWidget):
        """Create two widget page and using main window to make their parent."""
        super(Collections, self).__init__(parent)
        layout = QVBoxLayout(self)
        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)
        self.setWindowIcon(QIcon(QPixmap(":/icons/collections.png")))
        self.StructureWidget = StructureWidget(parent)
        self.TriangularIterationWidget = TriangularIterationWidget(
            self.StructureWidget.addCollection,
            parent
        )
        tab_widget.addTab(
            self.StructureWidget,
            self.StructureWidget.windowIcon(),
            "Structures"
        )
        tab_widget.addTab(
            self.TriangularIterationWidget,
            self.TriangularIterationWidget.windowIcon(),
            "Triangular iteration"
        )
        self.StructureWidget.triangle_button.clicked.connect(
            lambda: tab_widget.setCurrentIndex(1)
        )
        self.StructureWidget.layout_sender.connect(
            self.TriangularIterationWidget.setGraph
        )

    def clear(self):
        """Clear the sub-widgets."""
        self.StructureWidget.clear()
        self.TriangularIterationWidget.clear()

    def collect_data(self) -> List[Tuple[Tuple[int, int], ...]]:
        """Return collections to database."""
        return [tuple(G.edges) for G in self.StructureWidget.collections]

    def triangle_data(self) -> Dict[str, Dict[str, Any]]:
        """Return profiles to database."""
        return self.TriangularIterationWidget.collections
