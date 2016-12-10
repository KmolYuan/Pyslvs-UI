# -*- coding: utf-8 -*-
from .__init__ import *
_translate = QCoreApplication.translate

class Drive_show(QWidget, Drive_Form):
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
        self.Degree_text.setValue(float(value/100))
    
    def start(self):
        self.work.start()
        self.Shaft.setEnabled(False)
        self.playButton.setEnabled(False)
        self.Degree.setEnabled(False)
        self.Degree_text.setEnabled(False)
    
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
        self.Shaft.setEnabled(True)
        self.playButton.setEnabled(True)
        self.Degree.setEnabled(True)
        self.Degree_text.setEnabled(True)
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index): self.Shaft_change.emit(index)
    
    @pyqtSlot(float)
    def on_Degree_text_valueChanged(self, val):
        self.Degree.setValue(int(val*100))

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
            else:
                time.sleep(0.05)
                self.progress = self.progress+100
                self.progress_Signal.emit(self.progress)
        self.done.emit()
    
    def continue_progress(self):
        with QMutexLocker(self.mutex): self.stoped = False
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
