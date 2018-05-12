# -*- coding: utf-8 -*-

"""Collections main tab widget."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QIcon,
    QPixmap,
)
from .Structure import StructureWidget
from .TriangularIteration import TriangularIterationWidget


class Collections(QWidget):
    
    """Just a widget contains a sub tab widget."""
    
    def __init__(self, parent):
        """Create two widget page and using main window to make their parent."""
        super(Collections, self).__init__(parent)
        layout = QVBoxLayout(self)
        tabWidget = QTabWidget(self)
        layout.addWidget(tabWidget)
        self.setWindowIcon(QIcon(QPixmap(":/icons/collections.png")))
        self.StructureWidget = StructureWidget(parent)
        self.TriangularIterationWidget = TriangularIterationWidget(
            self.StructureWidget.addCollection,
            parent
        )
        tabWidget.addTab(
            self.StructureWidget,
            self.StructureWidget.windowIcon(),
            "Structures"
        )
        tabWidget.addTab(
            self.TriangularIterationWidget,
            self.TriangularIterationWidget.windowIcon(),
            "Triangular iteration"
        )
        self.StructureWidget.triangle_button.clicked.connect(
            lambda: tabWidget.setCurrentIndex(1)
        )
        self.StructureWidget.layout_sender.connect(
            self.TriangularIterationWidget.setGraph
        )
    
    def clear(self):
        """Clear the sub-widgets."""
        self.StructureWidget.clear()
        self.TriangularIterationWidget.clear()
    
    def CollectDataFunc(self):
        """Return collections to peewee IO."""
        return [tuple(G.edges) for G in self.StructureWidget.collections]
    
    def TriangleDataFunc(self):
        """Return profiles to peewee IO."""
        return self.TriangularIterationWidget.collections
