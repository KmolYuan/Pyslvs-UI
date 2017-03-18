# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver import Ui_Form as Triangle_Solver_Form
from .run_Triangle_Solver_edit import Triangle_Solver_edit_show
from ..kernel.pyslvs_triangle_solver.TS import solver

class Triangle_Solver_show(QWidget, Triangle_Solver_Form):
    newDirections = pyqtSignal(list)
    def __init__(self, Point, Directions=list(), parent=None):
        super(Triangle_Solver_show, self).__init__(parent)
        self.setupUi(self)
        self.directions = Directions
        self.answers = list()
        if Directions:
            for e in self.directions:
                self.editTable(False, self.directionsTable.rowCount(), **e)
        self.Point = Point
    
    def editDirection(self, name, edit=False):
        if edit is False: row = self.directionsTable.rowCount()
        else: row = edit
        dlg = Triangle_Solver_edit_show(self.Point, row, name)
        dlg.show()
        if dlg.exec_():
            self.editList(edit, row, **dlg.condition)
            self.editTable(edit, row, **dlg.condition)
    
    def editTable(self, edit, row, p1, p2, **condition):
        if edit is False: self.directionsTable.insertRow(row)
        self.directionsTable.setItem(row, 0, QTableWidgetItem(condition['Type']))
        self.directionsTable.setItem(row, 2, QTableWidgetItem('Result{}'.format(p1) if type(p1)==int else str(p1)))
        self.directionsTable.setItem(row, 3, QTableWidgetItem('Result{}'.format(p2) if type(p2)==int else str(p2)))
        condition = {k:v for k, v in condition.items() if k!='Type'}
        conditionItem = QTableWidgetItem(str(condition))
        conditionItem.setToolTip(str(condition))
        self.directionsTable.setItem(row, 4, conditionItem)
    
    def editList(self, edit, row, **condition):
        if edit is False: self.directions.append(condition)
        else: self.directions[row] = condition
        self.newDirections.emit(self.directions)
    
    @pyqtSlot()
    def on_pluse_PLAP_clicked(self): self.editDirection('PLAP')
    @pyqtSlot()
    def on_pluse_PLLP_clicked(self): self.editDirection('PLLP')
    @pyqtSlot()
    def on_pluse_PLPP_clicked(self): self.editDirection('PLPP')
    
    @pyqtSlot(int, int)
    def on_directionsTable_cellDoubleClicked(self, row, column):
        row = self.directionsTable.currentRow()
        if row>-1:
            name = self.directionsTable.item(row, 0).text()
            self.editDirection(name, row)
    
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        n = self.directionsTable.rowCount()
        if n>0:
            self.directionsTable.removeRow(n-1)
            del self.directions[n-1]
            self.newDirections.emit(self.directions)
    
    @pyqtSlot(QTableWidgetItem)
    def on_directionsTable_itemChanged(self, item):
        self.Solve.setEnabled(len(self.directions)>0)
        self.Merge.setEnabled(len(self.answers)>0)
    
    @pyqtSlot()
    def on_Solve_clicked(self):
        if self.directions:
            directions = [{k:v for k, v in e.items() if k!='Type'} for e in self.directions]
            s = solver(directions)
            self.answers = s.answer()
            for e in self.answers:
                result = QTableWidgetItem(str(e))
                result.setToolTip("x = {}\ny = {}".format(e[0], e[1]))
                self.directionsTable.setItem(self.answers.index(e), 1, result)
    
    @pyqtSlot()
    def on_Merge_clicked(self):
        pass
