# -*- coding: utf-8 -*-
from .modules import *
from .Ui_run_Path_Solving import Ui_Dialog as PathSolving_Dialog
from ..calculation.pathSolving import WorkerThread
from .run_Path_Solving_listbox import Path_Solving_listbox_show
from .run_Path_Solving_series import Path_Solving_series_show

class Path_Solving_show(QDialog, PathSolving_Dialog):
    addPathPoint = pyqtSignal(float, float)
    deletePathPoint = pyqtSignal(int)
    moveupPathPoint = pyqtSignal(int)
    movedownPathPoint = pyqtSignal(int)
    mergeMechanism = pyqtSignal(list)
    def __init__(self, mask, data, resultData, width, parent=None):
        super(Path_Solving_show, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_QuitOnClose, False)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.move(QPoint(width-self.width(), 0))
        self.Listbox = Path_Solving_listbox_show(resultData)
        self.mechanism_data = list()
        self.work = WorkerThread()
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.stop)
        self.work.done.connect(self.finish)
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
        for e in data: self.Point_list.addItem('('+str(e['x'])+", "+str(e['y'])+')')
        self.Point_list_Count()
    
    def __del__(self):
        self.stop()
        self.Listbox.deleteLater()
        del self.Listbox
    
    @pyqtSlot()
    def on_clearAll_clicked(self):
        self.Point_list.setCurrentRow(0)
        for i in reversed(range(self.Point_list.count()+1)): self.on_remove_clicked()
        self.Point_list_Count()
    
    @pyqtSlot()
    def on_series_clicked(self):
        dlg = Path_Solving_series_show()
        dlg.show()
        if dlg.exec_():
            start = int(dlg.startNum.value()*10)
            end = int(dlg.endNum.value()*10)
            diff = int(dlg.diffNum.value()*10)
            for e in range(start, end, diff): self.on_add_clicked(e/10, e/10)
    
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
        self.Point_list.addItem('({}, {})'.format(x, y))
        self.Point_list_Count()
    
    @pyqtSlot()
    def on_add_clicked(self, x=False, y=False):
        if x is False:
            x=float(self.X_coordinate.text() if self.X_coordinate.text()!='' else self.X_coordinate.placeholderText())
            y=float(self.Y_coordinate.text() if self.Y_coordinate.text()!='' else self.Y_coordinate.placeholderText())
        self.addPathPoint.emit(x, y)
        self.Point_list.addItem("({}, {})".format(x, y))
        self.Point_list_Count()
    @pyqtSlot()
    def on_remove_clicked(self):
        if self.Point_list.currentRow()>-1:
            self.deletePathPoint.emit(self.Point_list.currentRow())
            self.Point_list.takeItem(self.Point_list.currentRow())
            self.Point_list_Count()
    
    def Point_list_Count(self):
        self.pointNum.setText(
            "<html><head/><body><p><span style=\" font-size:12pt; color:#00aa00;\">"+str(self.Point_list.count())+"</span></p></body></html>")
        self.Generate.setEnabled(self.Point_list.count()>1)
    
    @pyqtSlot(list)
    def start(self, path):
        type_num = 0 if self.type0.isChecked() else (1 if self.type1.isChecked() else 2)
        upper = [self.AxMax.value(), self.AyMax.value(), self.DxMax.value(), self.DyMax.value()]+[self.LMax.value()]*5
        lower = [self.AxMin.value(), self.AyMin.value(), self.DxMin.value(), self.DyMin.value()]+[self.LMin.value()]*5
        self.work.setPath(path, upper, lower, type_num)
        print('Start Path Solving...')
        self.work.start()
        self.algorithmPanel.setEnabled(False)
        self.mainPanel.setEnabled(False)
        self.Generate.setEnabled(False)
        self.timeShow.setText("<html><head/><body><p><span style=\" font-size:12pt; color:#ffff0000\">Calculating...</span></p></body></html>")
        self.timePanel.setEnabled(False)
        self.progressBar.setRange(0, 0)
    @pyqtSlot(bool)
    def stop(self, p0): self.work.stop()
    
    @pyqtSlot(dict, int)
    def finish(self, mechanism, time_spand):
        self.mechanism_data = [mechanism]
        self.mergeMechanism.emit(self.mechanism_data)
        self.Listbox.addResult(mechanism)
        self.algorithmPanel.setEnabled(True)
        self.mainPanel.setEnabled(True)
        self.Generate.setEnabled(True)
        self.timePanel.setEnabled(True)
        self.progressBar.setRange(0, 100)
        sec = time_spand%60
        mins = int(time_spand/60)
        self.timeShow.setText("<html><head/><body><p><span style=\" font-size:12pt\">"+str(mins)+" [min] "+str(sec)+" [s]</span></p></body></html>")
        print('Finished.')
    
    @pyqtSlot()
    def on_isCustomize_clicked(self): self.limitPanel.setEnabled(self.isCustomize.isChecked())
