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
    distance_sorted,
    colorQt
)
from networkx import Graph
from string import ascii_uppercase
from itertools import product
from .Ui_TriangularIteration import Ui_Form

#This is a generator to get a non-numeric and non-repeat name string.
#('A', 'B', ..., 'AA', 'AB', ..., 'AAA', 'AAB', ...)
def letter_names():
    i = 0
    while True:
        i += 1
        for e in product(ascii_uppercase, repeat=i):
            yield ''.join(e)

class PreviewCanvas(BaseCanvas):
    def __init__(self, parent=None):
        super(PreviewCanvas, self).__init__(parent)
        self.clear()
    
    def clear(self):
        self.G = Graph()
        self.pos = {}
        self.update()
    
    def paintEvent(self, event):
        self.ox = self.width()/2
        self.oy = self.height()/2
        super(PreviewCanvas, self).paintEvent(event)
        ln = letter_names()
        r = 4.5
        pen = QPen()
        self.painter.setFont(QFont("Arial", self.fontSize*1.5))
        for node, (x, y) in self.pos.items():
            color = colorQt('Green')
            pen.setColor(color)
            self.painter.setPen(pen)
            self.painter.setBrush(QBrush(color))
            self.painter.drawEllipse(QPointF(x, -y), r, r)
            pen.setColor(colorQt('Black'))
            self.painter.setPen(pen)
            self.painter.drawText(QPointF(x + 2*r, -y), next(ln))
        self.painter.end()
    
    def setGraph(self, G, pos):
        self.G = G
        self.pos = pos
        self.update()

class CollectionsTriangularIteration(QWidget, Ui_Form):
    warning_icon = "<img width=\"15\" src=\":/icons/warning.png\"/> "
    
    def __init__(self, parent=None):
        super(CollectionsTriangularIteration, self).__init__(parent)
        self.setupUi(self)
        self.PreviewWindow = PreviewCanvas(self)
        self.main_layout.insertWidget(0, self.PreviewWindow)
        self.clear_button.clicked.connect(self.clear)
        self.clear()
    
    def clear(self):
        self.PreviewWindow.clear()
        self.joint_name.clear()
        self.Driver_list.clear()
        self.Follower_list.clear()
        self.Target_list.clear()
        self.constraint_list.clear()
        self.Link_Expression.clear()
        self.Expression.clear()
        for label in [
            self.Expression_list_label,
            self.grounded_label,
            self.Driver_label,
            self.Follower_label,
            self.Target_label,
            self.constraint_label
        ]:
            self.setWarning(label)
    
    def setWarning(self, label):
        self.removeWarning(label)
        label.setText(self.warning_icon + label.text())
    
    def removeWarning(self, label):
        label.setText(label.text().replace(self.warning_icon, ''))
    
    @pyqtSlot(Graph, dict)
    def setGraph(self, G, pos):
        self.clear()
        self.PreviewWindow.setGraph(G, pos)
        #TODO: Show the settings warning.
