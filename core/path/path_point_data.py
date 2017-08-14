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

from ..QtModules import *
from ..graphics.color import colorIcons
from .Ui_path_point_data import Ui_Info_Dialog

class path_point_data_show(QDialog, Ui_Info_Dialog):
    def __init__(self, Environment_variables, pathData, Point, parent=None):
        super(path_point_data_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.Environment_variables = Environment_variables
        self.pathData = pathData
        self.Point = Point
        self.Nodes = list()
        for vpaths in self.pathData:
            shaftNode = QTreeWidgetItem(self.pathTree, ['Shaft{}'.format(vpaths.shaft)])
            shaft = list()
            for vpath in vpaths.paths:
                pointNode = QTreeWidgetItem(['Point{}'.format(vpath.point)])
                shaftNode.addChild(pointNode)
                pointNode.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemNeverHasChildren)
                pointNode.setIcon(0, colorIcons()[self.Point[vpath.point].color])
                pointNode.setCheckState(0, Qt.Checked if vpath.show else Qt.Unchecked)
                shaft.append(pointNode)
            self.pathTree.addTopLevelItem(shaftNode)
            self.Nodes.append(shaft)
            self.pathTree.expandItem(shaftNode)
    
    @pyqtSlot()
    def on_buttonBox_rejected(self):
        for shaft, vpaths in zip(self.Nodes, self.pathData):
            for pointNode, vpath in zip(shaft, vpaths.paths):
                vpath.show = True if pointNode.checkState(0)==Qt.Checked else False
    
    @pyqtSlot()
    def on_showAll_clicked(self):
        self.setAllCheckState(True)
    @pyqtSlot()
    def on_hideAll_clicked(self):
        self.setAllCheckState(False)
    def setAllCheckState(self, checked):
        for shaft in self.Nodes:
            for pointNode in shaft:
                pointNode.setCheckState(0, Qt.Checked if checked else Qt.Unchecked)
    
    @pyqtSlot()
    def on_pathTree_itemSelectionChanged(self):
        currentItem = self.pathTree.currentItem()
        for shaft in self.Nodes:
            if currentItem in shaft:
                shaftIndex = self.Nodes.index(shaft)
                pointIndex = shaft.index(currentItem)
                for i in range(self.path_data.rowCount()):
                    self.path_data.removeRow(0)
                for i, dot in enumerate(self.pathData[shaftIndex].paths[pointIndex].path):
                    self.path_data.insertRow(i)
                    self.path_data.setItem(i, 0, QTableWidgetItem(str(dot[0])))
                    self.path_data.setItem(i, 1, QTableWidgetItem(str(dot[1])))
    
    @pyqtSlot()
    def on_copyPath_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText('\n'.join([
            ',\t'.join([self.path_data.item(row, column).text() for column in range(self.path_data.columnCount())
            ]) for row in range(self.path_data.rowCount())]))
