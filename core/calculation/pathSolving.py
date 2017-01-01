# -*- coding: utf-8 -*-
from .modules import *
from .calculation import pathSolvingProcess

class WorkerThread(QThread):
    done = pyqtSignal(list)
    progress_Signal = pyqtSignal(int)
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.stoped = False
        self.mutex = QMutex()
        self.progress = 0
    
    def setPath(self, data, type_num):
        self.path = data
        self.type_num = type_num
    
    def run(self):
        ''''''
        lst = list()
        self.done.emit(lst)
    
    def progress_going(self):
        self.progress = self.progress+1
        self.progress_Signal.emit(self.progress)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
