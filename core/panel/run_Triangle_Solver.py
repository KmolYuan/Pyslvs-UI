# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver import Ui_Form as Triangle_Solver_Form
from .run_Triangle_Solver_edit import Triangle_Solver_edit_show

class Triangle_Solver_show(QWidget, Triangle_Solver_Form):
    def __init__(self, Point, parent=None):
        super(Triangle_Solver_show, self).__init__(parent)
        self.setupUi(self)
        self.directions = list()
        self.Point = Point
    
    def editDirection(self, name, row=False):
        if row is False: row = self.directionsTable.rowCount()-1
        dlg = Triangle_Solver_edit_show(self.Point, name)
        dlg.show()
        if dlg.exec_(): pass
    
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
