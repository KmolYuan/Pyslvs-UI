# -*- coding: utf-8 -*-
import time
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
_translate = QCoreApplication.translate
from .Ui_run_Drive import Ui_Form

class Drive_show(QWidget, Ui_Form):
    Degree_change = pyqtSignal(int, float)
    Shaft_change = pyqtSignal(int)
    def __init__(self, parent=None):
        super(Drive_show, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkerThread()
        self.playButton.clicked.connect(self.start)
        self.work.progress_Signal.connect(self.progressbar_change)
        self.work.done.connect(self.finish)
    
    @pyqtSlot(int)
    def on_Degree_valueChanged(self, value):
        self.Degree_change.emit(self.Shaft.currentIndex(), float(value/100))
        self.Degree_text.setPlainText(str(float(value/100))+"°")
    
    def start(self):
        self.work.start()
        self.playButton.setEnabled(False)
        self.Degree.setEnabled(False)
        self.Shaft.setEnabled(False)
    
    @pyqtSlot(int)
    def progressbar_change(self, val): self.Degree.setValue(val)
    
    @pyqtSlot()
    def finish(self):
        self.Degree.setValue(0)
        self.work = WorkerThread()
        self.playButton.clicked.connect(self.start)
        self.work.progress_Signal.connect(self.progressbar_change)
        self.work.done.connect(self.finish)
        self.playButton.setText(_translate("Info_Dialog", "Start"))
        self.Degree.setEnabled(True)
        self.Shaft.setEnabled(True)
        self.playButton.setEnabled(True)
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index): self.Shaft_change.emit(index)

class WorkerThread(QThread):
    done = pyqtSignal()
    progress_Signal = pyqtSignal(int)
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.stoped = False
        self.mutex = QMutex()
        self.progress = 0
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        for i in range(360):
            if self.stoped: return
            else: self.progress_going()
        self.done.emit()
    
    def progress_going(self):
        time.sleep(0.05)
        self.progress = self.progress+100
        self.progress_Signal.emit(self.progress)
    
    def continue_progress(self):
        with QMutexLocker(self.mutex): self.stoped = False
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
