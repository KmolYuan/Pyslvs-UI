# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver import Ui_Form as Triangle_Solver_Form
from .run_Triangle_Solver_edit import Triangle_Solver_edit_show
from .run_Triangle_Solver_template import Triangle_Solver_template_show
from ..io.undoRedo import TSeditCommand, TSdeleteCommand
from ..kernel.pyslvs_triangle_solver.TS import solver
from copy import deepcopy

class Triangle_Solver_show(QWidget, Triangle_Solver_Form):
    startMerge = pyqtSignal()
    def __init__(self, FileState, Point, Directions=list(), parent=None):
        super(Triangle_Solver_show, self).__init__(parent)
        self.setupUi(self)
        self.answers = list()
        self.setPoint(Point)
        self.FileState = FileState
        self.ReloadTable(Directions)
    
    def setPoint(self, Point): self.Point = Point
    
    def ReloadTable(self, Directions):
        self.directions = Directions
        for direction in self.directions:
            row = self.directionsTable.rowCount()
            self.directionsTable.insertRow(row)
            self.directionsTable.setItem(row, 0, QTableWidgetItem(direction.Type))
            e = direction.p1
            p1Item = QTableWidgetItem('Result{}'.format(e+1) if type(e)==int else str(e))
            if type(e)==tuple: p1Item.setToolTip("x = {}\ny = {}".format(e[0], e[1]))
            self.directionsTable.setItem(row, 2, p1Item)
            e = direction.p2
            p2Item = QTableWidgetItem('Result{}'.format(e+1) if type(e)==int else str(e))
            if type(e)==tuple: p1Item.setToolTip("x = {}\ny = {}".format(e[0], e[1]))
            self.directionsTable.setItem(row, 3, p2Item)
            condition = [
                "{}: {}".format(k, (v if k!='merge' else ["Points only", "Slider"][v] if direction.Type=='PLPP' else
                ["Points only", "Linking L0", "Linking R0", "Fixed Chain", "Linking L0 & R0"][v])) for k, v in direction.items().items()]
            conditionItem = QTableWidgetItem(', '.join(condition))
            conditionItem.setToolTip('\n'.join(condition))
            self.directionsTable.setItem(row, 4, conditionItem)
    
    def editDirection(self, name, edit=False):
        if edit is False: dlg = Triangle_Solver_edit_show(self.Point, self.directionsTable.rowCount(), name, parent=self)
        else: dlg = Triangle_Solver_edit_show(self.Point, edit, parent=self, **self.directions[edit].items())
        dlg.show()
        if dlg.exec_():
            direction = dlg.condition
            self.FileState.beginMacro("{} {{TS Direction}}".format('Add' if edit is False else 'Edit'))
            self.FileState.push(TSeditCommand(self.directions, self.directionsTable, direction, edit))
            self.FileState.endMacro()
    
    @pyqtSlot()
    def on_pluse_PLAP_clicked(self): self.editDirection('PLAP')
    @pyqtSlot()
    def on_pluse_PLLP_clicked(self): self.editDirection('PLLP')
    @pyqtSlot()
    def on_pluse_PLPP_clicked(self): self.editDirection('PLPP')
    @pyqtSlot()
    def on_pluse_PPP_clicked(self): self.editDirection('PPP')
    
    def addTemplate(self, name):
        dlg = Triangle_Solver_template_show(self.Point, self.directionsTable.rowCount(), name, self)
        dlg.show()
        if dlg.exec_():
            for e in dlg.conditions:
                self.FileState.beginMacro("Add {TS Direction}")
                self.FileState.push(TSeditCommand(self.directions, self.directionsTable, e, False))
                self.FileState.endMacro()
    
    @pyqtSlot()
    def on_Bar4_clicked(self): self.addTemplate('4-bar linkage')
    @pyqtSlot()
    def on_Bar8_clicked(self): self.addTemplate('8-bar linkage')
    
    @pyqtSlot(int, int)
    def on_directionsTable_cellDoubleClicked(self, row, column):
        if row>-1: self.editDirection(self.directions[row].Type, row)
    
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        n = self.directionsTable.rowCount()
        if n>0:
            self.FileState.beginMacro("Delete {TS Direction}")
            self.FileState.push(TSdeleteCommand(self.directions, self.directionsTable))
            self.FileState.endMacro()
    @pyqtSlot()
    def on_clear_botton_clicked(self):
        for i in range(self.directionsTable.rowCount()): self.on_remove_botton_clicked()
    
    @pyqtSlot(QTableWidgetItem)
    def on_directionsTable_itemChanged(self, item): self.Solve.setEnabled(len(self.directions)>0)
    
    @pyqtSlot()
    def on_Solve_clicked(self):
        if self.directions:
            directions = deepcopy(self.directions)
            for e in directions:
                for p in ['p1', 'p2', 'p3']:
                    if type(e.get(p, False))==str:
                        pointTag = e.get(p, False).replace('Point', '')
                        e.set(p, (self.Point[int(pointTag)].cx, self.Point[int(pointTag)].cy))
            s = solver(directions)
            answers = s.answer()
            for e in answers:
                if e!=False:
                    show = ('({})'.format(', '.join(['{:.02f}']*len(e)))).format(*e)
                    result = QTableWidgetItem(show)
                    result.setToolTip(show)
                else: result = QTableWidgetItem('Failed!')
                self.directionsTable.setItem(answers.index(e), 1, result)
            self.answers = answers
            self.Merge.setEnabled(len(self.answers)>0 and not(False in self.answers))
    
    @pyqtSlot()
    def on_Merge_clicked(self): self.startMerge.emit()
