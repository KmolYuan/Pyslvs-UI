# -*- coding: utf-8 -*-
from .modules import *
from ..calculation.pathSolving import WorkerThread

class Path_Solving_show(QDialog, PathSolving_Dialog):
    addPathPoint = pyqtSignal(float, float)
    deletePathPoint = pyqtSignal(int)
    moveupPathPoint = pyqtSignal(int)
    movedownPathPoint = pyqtSignal(int)
    def __init__(self, isResult=False, parent=None):
        super(Path_Solving_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.work = WorkerThread()
        self.work.progress_Signal.connect(self.progressbar_change)
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.stop)
        self.work.done.connect(self.finish)
        self.isResult.setVisible(not isResult)
    
    def setUI(self, mask, data):
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
        for e in data: self.Point_list.addItem('('+str(e['x'])+", "+str(e['y'])+')')
        self.Point_list_Count()
    
    @pyqtSlot()
    def on_clearAll_clicked(self):
        self.Point_list.setCurrentRow(0)
        for i in reversed(range(self.Point_list.count()+1)): self.on_remove_clicked()
        self.Point_list_Count()
    
    @pyqtSlot()
    def on_moveUp_clicked(self):
        n = self.Point_list.currentRow()
        if n>0 and self.Point_list.count()>1:
            self.moveupPathPoint.emit(n)
            x = self.Point_list.currentItem().text()[1:-1].split(', ')[0]
            y = self.Point_list.currentItem().text()[1:-1].split(', ')[1]
            self.Point_list.insertItem(n-1, '('+str(x)+", "+str(y)+')')
            self.Point_list.takeItem(n+1)
            self.Point_list.setCurrentRow(n-1)
    
    @pyqtSlot()
    def on_moveDown_clicked(self):
        n = self.Point_list.currentRow()
        if n<self.Point_list.count()-1 and self.Point_list.count()>1:
            self.movedownPathPoint.emit(n)
            x = self.Point_list.currentItem().text()[1:-1].split(', ')[0]
            y = self.Point_list.currentItem().text()[1:-1].split(', ')[1]
            self.Point_list.insertItem(n+2, '('+str(x)+", "+str(y)+')')
            self.Point_list.takeItem(n)
            self.Point_list.setCurrentRow(n+1)
    
    def addPath(self, x, y):
        self.Point_list.addItem('('+str(x)+", "+str(y)+')')
        self.Point_list_Count()
    
    @pyqtSlot()
    def on_add_clicked(self):
        e = (float(self.X_coordinate.text()) if self.X_coordinate.text()!='' else float(self.X_coordinate.placeholderText()),
            float(self.Y_coordinate.text()) if self.Y_coordinate.text()!='' else float(self.Y_coordinate.placeholderText()))
        self.addPathPoint.emit(e[0], e[1])
        self.Point_list.addItem('('+str(e[0])+", "+str(e[1])+')')
        self.Point_list_Count()
    @pyqtSlot()
    def on_remove_clicked(self):
        try:
            if self.Point_list.currentRow()>-1:
                self.deletePathPoint.emit(self.Point_list.currentRow())
                self.Point_list.takeItem(self.Point_list.currentRow())
                self.Point_list_Count()
        except: pass
    
    def Point_list_Count(self):
        self.pointNum.setText(
            "<html><head/><body><p><span style=\" font-size:12pt; color:#00aa00;\">"+str(self.Point_list.count())+"</span></p></body></html>")
        self.startPanel.setEnabled(self.Point_list.count()>1)
    
    def start(self):
        print('start')
        self.work.start()
        self.mainPanel.setEnabled(False)
        self.startPanel.setEnabled(False)
    
    def stop(self): self.work.stop()
    
    @pyqtSlot(int)
    def progressbar_change(self, val): self.progressBar.setValue(val)
    
    @pyqtSlot(list)
    def finish(self, mechanism):
        self.mechanism_data = mechanism
        self.mainPanel.setEnabled(True)
        self.Generate.setEnabled(True)
        print('finish')
