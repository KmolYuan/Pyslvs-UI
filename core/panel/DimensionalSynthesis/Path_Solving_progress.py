# -*- coding: utf-8 -*-
from ...QtModules import *
from .Ui_Path_Solving_progress import Ui_Dialog
from ...calculation.pathSolving import WorkerThread

class Path_Solving_progress_show(QDialog, Ui_Dialog):
    def __init__(self, type_num, mechanismParams, GenerateData, algorithmPrams, parent=None):
        super(Path_Solving_progress_show, self).__init__(parent)
        self.setupUi(self)
        self.rejected.connect(self.closeWork)
        msgGeo = QApplication.desktop().availableGeometry()
        self.move(msgGeo.topLeft())
        self.type_num = type_num
        self.work = WorkerThread(type_num, mechanismParams, GenerateData, algorithmPrams)
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
            self.work.exit()
            self.work.wait()
            print("The thread has been canceled.")
