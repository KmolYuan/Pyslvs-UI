# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_run_Path_Track import Ui_Dialog

from .. import calculation

class Path_Track_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Path_Track_show, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkerThread()
        self.Path_data = []
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.start)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.stop)
        self.work.done.connect(self.finish)
        self.work.progress_Signal.connect(self.progressbar_change)
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
    
    @pyqtSlot()
    def on_add_button_clicked(self):
        try:
            self.Run_list.addItem(self.Point_list.currentItem().text())
            self.Point_list.takeItem(self.Point_list.currentRow())
        except: pass
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(self.Run_list.count()>=1)
    
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        try:
            self.Point_list.addItem(self.Run_list.currentItem().text())
            self.Run_list.takeItem(self.Run_list.currentRow())
        except: pass
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(self.Run_list.count()>=1)
    
    def start(self):
        if not self.Run_list.count()==0:
            self.work.Run_list = self.Run_list
            self.work.Entiteis_Point = self.Entiteis_Point
            self.work.Entiteis_Link = self.Entiteis_Link
            self.work.Entiteis_Stay_Chain = self.Entiteis_Stay_Chain
            self.work.Drive_Shaft = self.Drive_Shaft
            self.work.Slider = self.Slider
            self.work.Rod = self.Rod
            self.work.Parameter_list = self.Parameter_list
            self.work.Resolution = self.Resolution
            q = 0
            for i in range(self.Drive_Shaft.rowCount()):
                start_angle = float(self.Drive_Shaft.item(i, 3).text().replace("°", ""))*100
                end_angle = float(self.Drive_Shaft.item(i, 4).text().replace("°", ""))*100
                Resolution = float(self.Resolution.text())*100
                angle_set = int((end_angle+1-start_angle)/Resolution)
                q = q+angle_set
            limit = self.Run_list.count()*q
            self.progressBar.setRange(0, limit)
            self.work.start()
            self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
            self.Run_list.setEnabled(False)
            self.Point_list.setEnabled(False)
            self.Resolution.setEnabled(False)
            self.add_button.setEnabled(False)
            self.remove_botton.setEnabled(False)
    def stop(self): self.work.stop()
    
    @pyqtSlot(int)
    def progressbar_change(self, val): self.progressBar.setValue(val)
    
    @pyqtSlot(list)
    def finish(self, Path):
        self.Path_data = Path
        self.accept()

class WorkerThread(QThread):
    done = pyqtSignal(list)
    progress_Signal = pyqtSignal(int)
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.stoped = False
        self.mutex = QMutex()
        self.progress = 0
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        point_list = []
        for i in range(self.Run_list.count()):
            point_list += [int(self.Run_list.item(i).text().replace("Point", ""))]
        table2 = self.Drive_Shaft
        solvespace = calculation.Solvespace()
        nPath = []
        for i in range(table2.rowCount()):
            start_angle = float(table2.item(i, 3).text().replace("°", ""))*100
            end_angle = float(table2.item(i, 4).text().replace("°", ""))*100
            Resolution = float(self.Resolution.text())*100
            Path = []
            for n in point_list:
                Xval = []
                Yval = []
                for j in range(int(start_angle), int(end_angle)+1, int(Resolution)):
                    angle = float(j/100)
                    x, y = solvespace.Solve(n, angle, self.Entiteis_Point, self.Entiteis_Link,
                        self.Entiteis_Stay_Chain, self.Drive_Shaft, self.Slider, self.Rod, self.Parameter_list)
                    Xval += [x]
                    Yval += [y]
                    self.progress_going()
                Path += [Xval, Yval]
            nPath += [Path]
        self.done.emit(nPath)
    
    def progress_going(self):
        self.progress = self.progress+1
        self.progress_Signal.emit(self.progress)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
