# -*- coding: utf-8 -*-
from .modules import *
from .calculation import pathSolvingProcess
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
        t0 = timeit.default_timer()
        data = tuple((e['x'],e['y']) for e in self.path)
        time_and_fitness, fitnessParameter = pathSolvingProcess(data, self.Limit, self.type_num)
        mechanism = {
            'Algorithm':'Genetic' if self.type_num==0 else ('Firefly' if self.type_num==1 else 'Differtial Evolution'),
            'Ax':fitnessParameter[0],
            'Ay':fitnessParameter[1],
            'Dx':fitnessParameter[2],
            'Dy':fitnessParameter[3],
            'L0':fitnessParameter[4],
            'L1':fitnessParameter[5],
            'L2':fitnessParameter[6],
            'L3':fitnessParameter[7],
            'L4':fitnessParameter[8],
        }
        t1 = timeit.default_timer()
        time_spand = t1-t0
        print('total cost time: %d [s]'%time_spand)
        self.done.emit(mechanism, time_spand)
    
    def progress_going(self):
        self.progress = self.progress+1
        self.progress_Signal.emit(self.progress)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
