# -*- coding: utf-8 -*-
from .modules import *
from ..calculation.pathSolving import WorkerThread

class Path_Solving_show(QDialog, PathSolving_Dialog):
    addPathPoint = pyqtSignal(float, float)
    deletePathPoint = pyqtSignal(int)
    def __init__(self, parent=None):
        super(Path_Solving_show, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkerThread()
    
    def setUI(self, mask, data):
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
        for e in data: self.Point_list.addItem('('+str(e['x'])+", "+str(e['y'])+')')
        self.work.setPath(data)
    
    @pyqtSlot()
    def on_add_clicked(self):
        e = (float(self.X_coordinate.text()) if self.X_coordinate.text()!='' else float(self.X_coordinate.placeholderText()),
            float(self.Y_coordinate.text()) if self.Y_coordinate.text()!='' else float(self.Y_coordinate.placeholderText()))
        self.addPathPoint.emit(e[0], e[1])
        self.Point_list.addItem('('+str(e[0])+", "+str(e[1])+')')
    
    @pyqtSlot()
    def on_remove_clicked(self):
        try:
            if self.Point_list.currentRow()>-1:
                self.deletePathPoint.emit(self.Point_list.currentRow())
                self.Point_list.takeItem(self.Point_list.currentRow())
        except: pass
