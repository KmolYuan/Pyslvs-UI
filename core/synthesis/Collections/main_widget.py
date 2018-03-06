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
from .Structure import CollectionsStructure
from .TriangularIteration import CollectionsTriangularIteration

class Collections(QWidget):
    
    """Just a widget contains a sub tab widget."""
    
    def __init__(self, parent=None):
        super(Collections, self).__init__(parent)
        layout = QVBoxLayout(self)
        tabWidget = QTabWidget(self)
        layout.addWidget(tabWidget)
        self.setWindowIcon(QIcon(QPixmap(":/icons/collections.png")))
        self.CollectionsStructure = CollectionsStructure(parent)
        self.CollectionsTriangularIteration = CollectionsTriangularIteration(parent)
        self.CollectionsTriangularIteration.addToCollection = self.CollectionsStructure.addCollection
        tabWidget.addTab(self.CollectionsStructure, self.CollectionsStructure.windowIcon(), "Structure")
        tabWidget.addTab(self.CollectionsTriangularIteration, self.CollectionsTriangularIteration.windowIcon(), "Triangular iteration")
        self.CollectionsStructure.triangle_button.clicked.connect(lambda: tabWidget.setCurrentIndex(1))
        self.CollectionsStructure.layout_sender.connect(self.CollectionsTriangularIteration.setGraph)
    
    def clear(self):
        """Clear the sub-widgets."""
        self.CollectionsStructure.clear()
        self.CollectionsTriangularIteration.clear()
    
    def CollectDataFunc(self):
        """Return collections to peewee IO."""
        return [tuple(G.edges) for G in self.CollectionsStructure.collections]
    
    def TriangleDataFunc(self):
        """Return profiles to peewee IO."""
        return self.CollectionsTriangularIteration.collections
