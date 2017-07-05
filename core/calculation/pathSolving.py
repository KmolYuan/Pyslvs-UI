# -*- coding: utf-8 -*-
from ..QtModules import *
from .algorithm import generateProcess
import timeit

class WorkerThread(QThread):
    done = pyqtSignal(dict, int)
    def __init__(self, type_num, mechanismParams, GenerateData, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.type_num = type_num
        self.mechanismParams = mechanismParams
        self.GenerateData = GenerateData
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        alg = 'Genetic' if self.type_num==0 else ('Firefly' if self.type_num==1 else "Differtial Evolution")
        print("Algorithm: "+alg)
        t0 = timeit.default_timer()
        print("Through: {}".format(self.mechanismParams['targetPath']))
        time_and_fitness, fitnessParameter = generateProcess(self.type_num, self.mechanismParams, self.GenerateData)
        if self.stoped: return
        t1 = timeit.default_timer()
        time_spand = t1-t0
        mechanism = {
            'Algorithm':alg,
            'time':time_spand,
            'Ax':fitnessParameter[0],
            'Ay':fitnessParameter[1],
            'Dx':fitnessParameter[2],
            'Dy':fitnessParameter[3],
            'L0':fitnessParameter[4],
            'L1':fitnessParameter[5],
            'L2':fitnessParameter[6],
            'L3':fitnessParameter[7],
            'L4':fitnessParameter[8],
            'mechanismParams':self.mechanismParams,
            'GenerateData':self.GenerateData,
            'TimeAndFitness':time_and_fitness}
        print('total cost time: {:.4f} [s]'.format(time_spand))
        self.done.emit(mechanism, time_spand)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
