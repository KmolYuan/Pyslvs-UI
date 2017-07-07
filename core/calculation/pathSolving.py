# -*- coding: utf-8 -*-
from ..QtModules import *
from .algorithm import generateProcess
import timeit

class WorkerThread(QThread):
    done = pyqtSignal(dict, int)
    def __init__(self, type_num, mechanismParams, GenerateData, algorithmPrams, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.type_num = type_num
        self.mechanismParams = mechanismParams
        self.GenerateData = GenerateData
        self.algorithmPrams = algorithmPrams
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        alg = 'Genetic' if self.type_num==0 else 'Firefly' if self.type_num==1 else "Differtial Evolution"
        print("Algorithm: "+alg)
        print("Through: {}".format(self.mechanismParams['targetPath']))
        t0 = timeit.default_timer()
        TnF, FP = generateProcess(self.type_num, self.mechanismParams, self.GenerateData, self.algorithmPrams)
        if self.stoped: return
        t1 = timeit.default_timer()
        time_spand = t1-t0
        mechanism = {
            'Algorithm':alg,
            'time':time_spand,
            'Ax':FP[0], 'Ay':FP[1],
            'Dx':FP[2], 'Dy':FP[3],
            'L0':FP[4], 'L1':FP[5], 'L2':FP[6], 'L3':FP[7], 'L4':FP[8],
            'mechanismParams':self.mechanismParams,
            'GenerateData':self.GenerateData,
            'algorithmPrams':self.algorithmPrams,
            'TimeAndFitness':TnF}
        print('total cost time: {:.4f} [s]'.format(time_spand))
        self.done.emit(mechanism, time_spand)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
