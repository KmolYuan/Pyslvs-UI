# -*- coding: utf-8 -*-
from ..QtModules import *
from ..kernel.pyslvs_triangle_solver.TS import Direction
from .Ui_run_Triangle_Solver_template import Ui_Dialog

class Triangle_Solver_template_show(QDialog, Ui_Dialog):
    def __init__(self, Point, row, template='4-bar linkage', parent=None):
        super(Triangle_Solver_template_show, self).__init__(parent)
        self.setupUi(self)
        self.template = [
            { #4-Bar
                'pic':":/icons/preview/4Bar.png",
                'pic_tri':":/icons/preview/4Bar_triangle.png",
                'parama':5,
                'triangle':[
                    {'p':[1, 2, 3], 'merge':1},
                    {'p':[3, 2, 4], 'merge':2},
                    {'p':[3, 4, 5], 'merge':3}]},
            { #8-Bar
                'pic':":/icons/preview/8Bar.png",
                'pic_tri':":/icons/preview/8Bar_triangle.png",
                'parama':8,
                'triangle':[
                    {'p':[2, 1, 3], 'merge':2},
                    {'p':[2, 3, 4], 'merge':2},
                    {'p':[2, 4, 5], 'merge':3},
                    {'p':[3, 2, 6], 'merge':4},
                    {'p':[6, 5, 7], 'merge':2},
                    {'p':[6, 7, 8], 'merge':3}]},
            ]
        self.Point = Point
        self.on_templateType_currentIndexChanged(0)
        self.templateType.setCurrentIndex(self.templateType.findText(template))
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.turn2Dict)
        self.isOk()
    
    @pyqtSlot(int)
    def on_templateType_currentIndexChanged(self, pos):
        self.clearTables()
        self.paramaTable(self.template[pos]['parama'])
        self.triTable(self.template[pos]['triangle'])
        self.setPreview(self.template[pos]['pic'])
    
    @pyqtSlot(QModelIndex)
    def on_triangleTable_clicked(self, index):
        self.setPreview(self.template[self.templateType.currentIndex()]['pic_tri'])
    
    @pyqtSlot(QModelIndex)
    def on_parameterTable_clicked(self, index):
        self.setPreview(self.template[self.templateType.currentIndex()]['pic'])
    
    def setPreview(self, pic): self.templateImage.setPixmap(QPixmap(pic).scaledToWidth(500))
    
    def clearTables(self):
        for table in [self.triangleTable, self.parameterTable]:
            for i in range(table.rowCount()): table.removeRow(0)
    
    def paramaTable(self, c):
        for i in range(c):
            self.parameterTable.insertRow(i)
            self.parameterTable.setItem(i, 0, QTableWidgetItem('P{}'.format(i+1)))
            pointBox = QComboBox(self.parameterTable)
            for k in range(len(self.Point)): pointBox.insertItem(k, 'Point{}'.format(k))
            pointBox.currentIndexChanged.connect(self.isOk)
            self.parameterTable.setCellWidget(i, 1, pointBox)
        for i in range(c):
            self.parameterTable.cellWidget(i, 1).currentIndexChanged.connect(self.updateTriTable)
    
    def triTable(self, li):
        if self.triangleTable.rowCount()==0:
            for i in range(len(li)): self.triangleTable.insertRow(i)
        for e in li:
            row = li.index(e)
            self.triangleTable.setItem(row, 0, QTableWidgetItem('PPP'))
            self.triangleTable.setItem(row, 1, QTableWidgetItem(
                ["Points only", "Linking L0", "Linking R0", "Fixed Chain", "Linking L0 & R0"][e['merge']]))
            points = [self.parameterTable.cellWidget(p-1, 1).currentIndex() for p in e['p']]
            self.triangleTable.setItem(row, 2, QTableWidgetItem('Point{}'.format(points[0])))
            self.triangleTable.setItem(row, 3, QTableWidgetItem('Point{}'.format(points[1])))
            self.triangleTable.setItem(row, 4, QTableWidgetItem('Point{}'.format(points[2])))
    
    def updateTriTable(self):
        self.triTable(self.template[self.templateType.currentIndex()]['triangle'])
    
    @pyqtSlot(int)
    def isOk(self, *args):
        parameters = [self.parameterTable.cellWidget(i, 1).currentIndex() for i in range(self.parameterTable.rowCount())]
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(len(set(parameters))==len(parameters))
    
    def turn2Dict(self):
        triangle = self.template[self.templateType.currentIndex()]['triangle']
        self.conditions = [Direction(**{'Type':'PPP',
            'p1':self.triangleTable.item(row, 2).text(),
            'p2':self.triangleTable.item(row, 3).text(),
            'p3':self.triangleTable.item(row, 4).text(),
            'merge':triangle[row]['merge']}) for row in range(len(triangle))]
