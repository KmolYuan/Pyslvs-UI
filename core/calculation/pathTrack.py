from .__init__ import *
from .calculation import Solvespace

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
        solvespace = Solvespace()
        nPath = []
        for i in range(len(self.Shaft)):
            start_angle = self.Shaft[i]['start']*100
            end_angle = self.Shaft[i]['end']*100
            Resolution = self.Resolution*100
            Path = []
            for n in point_list:
                Xval = []
                Yval = []
                for j in range(int(start_angle), int(end_angle)+1, int(Resolution)):
                    angle = float(j/100)
                    x, y = solvespace.path_track_process(n, angle, self.Point, self.Link,
                        self.Chain, self.Shaft, self.Slider, self.Rod, self.Parameter)
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
