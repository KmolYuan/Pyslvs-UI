# -*- coding: utf-8 -*-
from .modules import *
from .calculation import generateProcess
import timeit

class WorkerThread(QThread):
    done = pyqtSignal(dict, int)
    progress_Signal = pyqtSignal(int)
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.stoped = False
        self.mutex = QMutex()
        self.progress = 0
    def setPath(self, path, Limit, type_num):
        self.path = path
        self.type_num = type_num
        self.Limit = Limit
    
    def run(self):
        alg = 'Genetic' if self.type_num==0 else ('Firefly' if self.type_num==1 else 'Differtial Evolution')
        print("Algorithm: "+alg)
        t0 = timeit.default_timer()
        pathData = tuple((e['x'],e['y']) for e in self.path)
        print("Through: {}".format(pathData))
        time_and_fitness, fitnessParameter = generateProcess(pathData, self.Limit, self.type_num)
        t1 = timeit.default_timer()
        time_spand = t1-t0
        mechanism = {
            'Algorithm':alg,
            'path':pathData,
            'Ax':fitnessParameter[0],
            'Ay':fitnessParameter[1],
            'Dx':fitnessParameter[2],
            'Dy':fitnessParameter[3],
            'L0':fitnessParameter[4],
            'L1':fitnessParameter[5],
            'L2':fitnessParameter[6],
            'L3':fitnessParameter[7],
            'L4':fitnessParameter[8],
            'time':time_spand}
        print('total cost time: {:.4f} [s]'.format(time_spand))
        self.done.emit(mechanism, time_spand)
    
    def progress_going(self):
        self.progress += 1
        self.progress_Signal.emit(self.progress)
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
