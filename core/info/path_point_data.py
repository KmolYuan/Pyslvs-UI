# -*- coding: utf-8 -*-
from ..QtModules import *
from ..graphics.color import colorIcons
from .Ui_path_point_data import Ui_Info_Dialog

class path_point_data_show(QDialog, Ui_Info_Dialog):
    def __init__(self, Environment_variables, pathData, Point, parent=None):
        super(path_point_data_show, self).__init__(parent)
        self.setupUi(self)
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
            for pointNode, vpath in zip(shaft, vpaths.paths): vpath.show = True if pointNode.checkState(0)==Qt.Checked else False
    
    @pyqtSlot()
    def on_showAll_clicked(self): self.setAllCheckState(True)
    @pyqtSlot()
    def on_hideAll_clicked(self): self.setAllCheckState(False)
    def setAllCheckState(self, checked):
        for shaft in self.Nodes:
            for pointNode in shaft: pointNode.setCheckState(0, Qt.Checked if checked else Qt.Unchecked)
    
    @pyqtSlot()
    def on_pathTree_itemSelectionChanged(self):
        currentItem = self.pathTree.currentItem()
        for shaft in self.Nodes:
            if currentItem in shaft:
                shaftIndex = self.Nodes.index(shaft)
                pointIndex = shaft.index(currentItem)
                for i in range(self.path_data.rowCount()): self.path_data.removeRow(0)
                for i, dot in enumerate(self.pathData[shaftIndex].paths[pointIndex].path):
                    self.path_data.insertRow(i)
                    self.path_data.setItem(i, 0, QTableWidgetItem(str(dot[0])))
                    self.path_data.setItem(i, 1, QTableWidgetItem(str(dot[1])))
    
    @pyqtSlot()
    def on_copyPath_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText('\n'.join([
            ', '.join([self.path_data.item(row, column).text() for column in range(self.path_data.columnCount())
            ]) for row in range(self.path_data.rowCount())]))
