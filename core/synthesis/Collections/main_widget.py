# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from core.QtModules import *
from .Structure import CollectionsStructure
from .TriangularIteration import CollectionsTriangularIteration

class Collections(QWidget):
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
        self.CollectionsStructure.clear()
        self.CollectionsTriangularIteration.clear()
    
    def CollectDataFunc(self):
        return [tuple(G.edges) for G in self.CollectionsStructure.collections]
    
    def TriangleDataFunc(self):
        return self.CollectionsTriangularIteration.collections
