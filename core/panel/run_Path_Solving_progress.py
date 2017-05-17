# -*- coding: utf-8 -*-
from ..QtModules import *
from copy import deepcopy
from .Ui_run_Path_Solving_progress import Ui_Dialog
from ..calculation.pathSolving import WorkerThread

class Path_Solving_progress_show(QDialog, Ui_Dialog):
    def __init__(self, path, upper, lower, minAngle, maxAngle, type_num, maxGen, report, parent=None):
        super(Path_Solving_progress_show, self).__init__(parent)
        self.setupUi(self)
        self.rejected.connect(self.closeWork)
        msgGeo = QApplication.desktop().availableGeometry()
        self.move(msgGeo.topLeft())
        self.path = deepcopy(path)
        self.type_num = type_num
        self.upper = deepcopy(upper)
        self.lower = deepcopy(lower)
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.maxGen = maxGen
        self.report = report
        self.work = WorkerThread(self.path, self.upper, self.lower, self.minAngle, self.maxAngle,
            self.type_num, self.maxGen, self.report, None)
        self.work.done.connect(self.finish)
    
    @pyqtSlot()
    def on_Start_clicked(self):
        self.work.start()
        self.Start.setEnabled(False)
        self.buttonBox.setEnabled(False)
        self.progressBar.setRange(0, 0)
        print("Start Path Solving...")
    
    @pyqtSlot(dict, int)
    def finish(self, mechanism, time_spand):
        self.mechanism = mechanism
        self.time_spand = time_spand
        self.accept()
    
    @pyqtSlot()
    def closeWork(self):
        if self.work.isRunning():
            #self.work.terminate()
            self.work.exit()
            self.work.wait()
            print("The thread has been canceled.")
