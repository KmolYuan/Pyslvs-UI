# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Path_Solving_progress import Ui_Dialog
from ..calculation.pathSolving import WorkerThread

class Path_Solving_progress_show(QDialog, Ui_Dialog):
    def __init__(self, path, upper, lower, minAngle, maxAngle, type_num, maxGen, report, parent=None):
        super(Path_Solving_progress_show, self).__init__(parent)
        self.setupUi(self)
        self.path = path
        self.type_num = type_num
        self.upper = upper
        self.lower = lower
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.maxGen = maxGen
        self.report = report
    
    @pyqtSlot()
    def on_Start_clicked(self):
        self.Start.setEnabled(False)
        self.work = WorkerThread(self.path, self.upper, self.lower, self.minAngle, self.maxAngle,
            self.type_num, self.maxGen, self.report)
        self.work.done.connect(self.finish)
        self.work.start()
        print("Start Path Solving...")
        self.progressBar.setRange(0, 0)
    
    @pyqtSlot(dict, int)
    def finish(self, mechanism, time_spand):
        self.mechanism = mechanism
        self.time_spand = time_spand
        self.accept()
