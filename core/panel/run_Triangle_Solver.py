# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver import Ui_Form as Triangle_Solver_Form
from .run_Triangle_Solver_edit import Triangle_Solver_edit_show

class Triangle_Solver_show(QWidget, Triangle_Solver_Form):
    newDirections = pyqtSignal(list)
    def __init__(self, Point, Directions=list(), parent=None):
        super(Triangle_Solver_show, self).__init__(parent)
        self.setupUi(self)
        self.directions = Directions
        if Directions:
            for e in self.directions:
                self.editTable(False, self.directionsTable.rowCount(),
                    Type=0 if e.get('len2', False) is False else 1,
                    p1=e['p1'], p2=e['p2'], len1=e['len1'], len2=e.get('len2', 10.), angle=e.get('angle', 30.))
        self.Point = Point
    
    def editDirection(self, name, edit=False):
        if edit is False: row = self.directionsTable.rowCount()
        else: row = edit
        dlg = Triangle_Solver_edit_show(self.Point, row, name)
        dlg.show()
        if dlg.exec_():
            Arg = [edit, row, dlg.type.currentIndex(),
                (dlg.x1.value(), dlg.y1.value()) if dlg.p1Customize.isChecked() else (
                    dlg.p1.currentText() if dlg.p1Exist.isChecked() else dlg.r1.currentIndex()),
                (dlg.x2.value(), dlg.y2.value()) if dlg.p2Customize.isChecked() else (
                    dlg.p2.currentText() if dlg.p2Exist.isChecked() else dlg.r2.currentIndex()),
                dlg.len1.value(), dlg.angle.value(), dlg.len2.value()]
            self.editTable(*Arg)
            self.editList(*Arg)
    
    def editTable(self, edit, row, Type, p1, p2, len1, len2, angle):
        if edit is False: self.directionsTable.insertRow(row)
        self.directionsTable.setItem(row, 0, QTableWidgetItem('PLAP' if Type==0 else 'PLLP'))
        self.directionsTable.setItem(row, 1, QTableWidgetItem('Result{}'.format(p1) if type(p1)==int else str(p1)))
        self.directionsTable.setItem(row, 2, QTableWidgetItem(str(len1)))
        self.directionsTable.setItem(row, 3, QTableWidgetItem(str(len2)))
        self.directionsTable.setItem(row, 4, QTableWidgetItem(str(angle)))
        self.directionsTable.setItem(row, 5, QTableWidgetItem('Result{}'.format(p2) if type(p2)==int else str(p2)))
    
    def editList(self, edit, row, Type, p1, p2, len1, len2, angle):
        direction = {'p1':p1, 'p2':p2, 'len1':len1}
        if Type==0: direction['angle'] = angle
        else: direction['len2'] = len2
        if edit is False: self.directions.append(direction)
        else: self.directions[row] = direction
        self.newDirections.emit(self.directions)
    
    @pyqtSlot()
    def on_pluse_PLAP_clicked(self): self.editDirection('PLAP')
    @pyqtSlot()
    def on_pluse_PLLP_clicked(self): self.editDirection('PLLP')
    
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        n = self.directionsTable.rowCount()
        if n>0: self.directionsTable.removeRow(n-1)
    
    @pyqtSlot(int, int)
    def on_directionsTable_cellDoubleClicked(self, row, column):
        row = self.directionsTable.currentRow()
        if row>-1:
            name = self.directionsTable.item(row, 0).text()
            self.editDirection(name, row)
