# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
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
from core.graphics import (
    BaseCanvas,
    distance_sorted
)
from networkx import Graph
from .Ui_TriangularIteration import Ui_Form

class PreviewCanvas(BaseCanvas):
    def __init__(self, parent=None):
        super(PreviewCanvas, self).__init__(parent)
        self.G = Graph()
        self.pos = {}
    
    def paintEvent(self, event):
        self.ox = self.width()/2
        self.oy = self.height()/2
        super(PreviewCanvas, self).paintEvent(event)
        self.painter.end()
    
    @pyqtSlot(Graph, dict)
    def setGraph(self, G, pos):
        self.G = G
        self.pos = pos
        self.update()

class CollectionTriangularIteration(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(CollectionTriangularIteration, self).__init__(parent)
        self.setupUi(self)
        self.PreviewWindow = PreviewCanvas(self)
        self.main_layout.insertWidget(0, self.PreviewWindow)
