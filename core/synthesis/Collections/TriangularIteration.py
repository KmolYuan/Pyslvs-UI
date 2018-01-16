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
'''
'CollectionsDialog',
'ConstrainsDialog',
'TargetsDialog',
'SolutionsDialog',
'''
from .TriangularIteration_dialog import *
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
        self.status = {}
        self.grounded = -1
        self.update()
    
    def paintEvent(self, event):
        self.ox = self.width()/2
        self.oy = self.height()/2
        super(PreviewCanvas, self).paintEvent(event)
        r = 4.5
        pen = QPen()
        pen.setWidth(r)
        self.painter.setPen(pen)
        self.painter.setBrush(QBrush(QColor(226, 219, 190, 150)))
        for link in self.G.nodes:
            if link==self.grounded:
                continue
            self.painter.drawPolygon(*distance_sorted([
                (self.pos[n][0], -self.pos[n][1])
                for n, edge in enumerate(self.G.edges) if link in edge
            ]))
        self.painter.setFont(QFont("Arial", self.fontSize*1.5))
        for node, (x, y) in self.pos.items():
            color = colorQt('Dark-Magenta') if self.status[node] else colorQt('Green')
            pen.setColor(color)
            self.painter.setPen(pen)
            self.painter.setBrush(QBrush(color))
            self.painter.drawEllipse(QPointF(x, -y), r, r)
            pen.setColor(colorQt('Black'))
            self.painter.setPen(pen)
            self.painter.drawText(QPointF(x + 2*r, -y), 'P{}'.format(node))
        self.painter.end()
    
    def setGraph(self, G, pos):
        self.G = G
        self.pos = pos
        self.status = {k:False for k in pos}
        self.update()
    
    def setGrounded(self, link: int):
        self.grounded = link
        for n, edge in enumerate(self.G.edges):
            self.status[n] = self.grounded in edge
        self.update()
    
    def setStatus(self, point: int, status: bool):
        self.status[point] = status

class CollectionsTriangularIteration(QWidget, Ui_Form):
    warning_icon = "<img width=\"15\" src=\":/icons/warning.png\"/> "
    
    def __init__(self, parent=None):
        super(CollectionsTriangularIteration, self).__init__(parent)
        self.setupUi(self)
        self.collections = []
        self.PreviewWindow = PreviewCanvas(self)
        self.main_layout.insertWidget(0, self.PreviewWindow)
        self.clear_button.clicked.connect(self.clear)
        self.clear()
    
    def clear(self):
        self.collections.clear()
        self.PreviewWindow.clear()
        self.joint_name.clear()
        self.Expression_list.clear()
        self.grounded_list.clear()
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
            self.Target_label
        ]:
            self.setWarning(label, True)
    
    def setWarning(self, label, warning: bool):
        label.setText(label.text().replace(self.warning_icon, ''))
        if warning:
            label.setText(self.warning_icon + label.text())
    
    @pyqtSlot(Graph, dict)
    def setGraph(self, G, pos):
        self.clear()
        self.PreviewWindow.setGraph(G, pos)
        for link in G.nodes:
            self.grounded_list.addItem("({})".format(", ".join(
                'P{}'.format(n) for n, edge in enumerate(G.edges) if link in edge
            )))
        for node in pos:
            self.joint_name.addItem('P{}'.format(node))
        self.name_dict = {
            self.joint_name.itemText(row):""
            for row in range(self.joint_name.count())
        }
    
    @pyqtSlot(int)
    def on_grounded_list_currentRowChanged(self, row):
        self.setWarning(self.grounded_label, not row>-1)
        self.PreviewWindow.setGrounded(row)
        self.on_joint_name_currentIndexChanged()
        self.Follower_list.clear()
        self.Driver_list.clear()
        if row>-1:
            self.Follower_list.addItems(
                self.grounded_list.currentItem().text()
                .replace('(', '')
                .replace(')', '')
                .split(", ")
            )
        self.setWarning(self.Follower_label, not row>-1)
        self.setWarning(self.Driver_label, True)
    
    @pyqtSlot(int)
    def on_joint_name_currentIndexChanged(self, index=None):
        if index is None:
            index = self.joint_name.currentIndex()
        if index>-1:
            status = self.PreviewWindow.status[index]
            self.status.setText("Known" if status else "Not known")
            self.PLAP_solution.setEnabled(not status)
            self.PLLP_solution.setEnabled(not status)
        else:
            self.status.setText("No status")
            self.PLAP_solution.setEnabled(False)
            self.PLLP_solution.setEnabled(False)
    
    @pyqtSlot()
    def on_Driver_add_clicked(self):
        row = self.Follower_list.currentRow()
        if row>-1:
            self.Driver_list.addItem(self.Follower_list.takeItem(row))
            self.setWarning(self.Driver_label, False)
    
    @pyqtSlot()
    def on_Follower_add_clicked(self):
        row = self.Driver_list.currentRow()
        if row>-1:
            self.Follower_list.addItem(self.Driver_list.takeItem(row))
            self.setWarning(self.Driver_label, not bool(self.Driver_list.count()))
    
    def get_currentMechanismParams(self):
        return {
            'Driver':{
                self.name_dict[self.Driver_list.item().text()]:None
                for row in range(self.Driver_list.count())
            },
            'Follower':{
                self.name_dict[self.Follower_list.item().text()]:None
                for row in range(self.Follower_list.count())
            },
            'Target':{
                self.name_dict[self.Target_list.item().text()]:None
                for row in range(self.Target_list.count())
            },
            'Link_Expression':self.Link_Expression.text(),
            'Expression':self.Expression.text(),
            'constraint':[
                tuple(self.constraint_list.item(row).text().split(','))
                for row in range(self.constraint_list.count())
            ]
        }
    
    @pyqtSlot()
    def on_load_button_clicked(self):
        dlg = CollectionsDialog(self)
        dlg.show()
        dlg.exec_()
    
    @pyqtSlot()
    def on_constrains_button_clicked(self):
        dlg = ConstrainsDialog(self)
        dlg.show()
        dlg.exec_()
    
    @pyqtSlot()
    def on_Target_button_clicked(self):
        dlg = TargetsDialog(self)
        dlg.show()
        dlg.exec_()
    
    @pyqtSlot()
    def on_PLAP_solution_clicked(self):
        dlg = SolutionsDialog('PLAP', self)
        dlg.show()
        dlg.exec_()
    
    @pyqtSlot()
    def on_PLLP_solution_clicked(self):
        dlg = SolutionsDialog('PLLP', self)
        dlg.show()
        dlg.exec_()
