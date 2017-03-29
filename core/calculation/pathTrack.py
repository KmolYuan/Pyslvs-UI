# -*- coding: utf-8 -*-
from ..QtModules import *
from .calculation import slvsProcess
import timeit

class WorkerThread(QThread):
    done = pyqtSignal(list)
    progress_Signal = pyqtSignal(int)
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.progress = 0
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        print("Path Tracking...")
        t0 = timeit.default_timer()
        nPath = list()
        for i in self.ShaftList:
            start_angle = self.Shaft[i]['start']*100
            end_angle = self.Shaft[i]['end']*100
            Resolution = self.Resolution*100
            Path = list()
            for n in self.Run_list:
                Xval = list()
                Yval = list()
                for j in range(int(start_angle), int(end_angle)+1, int(Resolution)):
                    angle = float(j/100)
                    x, y = slvsProcess(self.Point, self.Link, self.Chain, self.Shaft, self.Slider, self.Rod, i, n, angle)
                    Xval.append(x)
                    Yval.append(y)
                    self.progress_going()
                Path.append(Xval)
                Path.append(Yval)
            nPath.append(Path)
        t1 = timeit.default_timer()
        time_spand = t1-t0
        print('total cost time: {:.4f} [s]'.format(time_spand))
        self.done.emit(nPath)
    
    def progress_going(self):
        self.progress += 1
        self.progress_Signal.emit(self.progress)
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
