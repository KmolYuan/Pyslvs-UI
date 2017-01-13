# -*- coding: utf-8 -*-
from .modules import *
from .calculation import pathTrackProcess

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
        nPath = []
        for i in self.ShaftList:
            start_angle = self.Shaft[i]['start']*100
            end_angle = self.Shaft[i]['end']*100
            Resolution = self.Resolution*100
            Path = []
            for n in point_list:
                Xval = []
                Yval = []
                for j in range(int(start_angle), int(end_angle)+1, int(Resolution)):
                    angle = float(j/100)
                    x, y = pathTrackProcess(n, angle, self.Point, self.Link,
                        self.Chain, self.Shaft, self.Slider, self.Rod, self.Parameter, i)
                    Xval += [x]
                    Yval += [y]
                    self.progress_going()
                Path += [Xval, Yval]
            nPath += [Path]
        self.done.emit(nPath)
    
    def progress_going(self):
        self.progress += 1
        self.progress_Signal.emit(self.progress)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
