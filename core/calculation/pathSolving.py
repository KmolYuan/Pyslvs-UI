# -*- coding: utf-8 -*-
from ..QtModules import *
from .algorithm import generateProcess
import timeit

class WorkerThread(QThread):
    done = pyqtSignal(dict, int)
    def __init__(self, path, upper, lower, minAngle, maxAngle, type_num, maxGen, report, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.path = path
        self.type_num = type_num
        self.upper = upper
        self.lower = lower
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.maxGen = maxGen
        self.report = report
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        alg = 'Genetic' if self.type_num==0 else ('Firefly' if self.type_num==1 else "Differtial Evolution")
        print("Algorithm: "+alg)
        t0 = timeit.default_timer()
        pathData = tuple((e['x'],e['y']) for e in self.path)
        print("Through: {}".format(pathData))
        time_and_fitness, fitnessParameter = generateProcess(pathData,
            self.upper, self.lower, self.minAngle, self.maxAngle, self.type_num, self.maxGen, self.report)
        if self.stoped: return
        t1 = timeit.default_timer()
        time_spand = t1-t0
        mechanism = {
            'Algorithm':alg,
            'path':pathData,
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
            'AxMax':self.upper[0],
            'AyMax':self.upper[1],
            'DxMax':self.upper[2],
            'DyMax':self.upper[3],
            'IMax':self.upper[4],
            'LMax':self.upper[5],
            'FMax':self.upper[6],
            'AxMin':self.lower[0],
            'AyMin':self.lower[1],
            'DxMin':self.lower[2],
            'DyMin':self.lower[3],
            'IMin':self.lower[4],
            'LMin':self.lower[5],
            'FMin':self.lower[6],
            'minAngle':self.minAngle,
            'maxAngle':self.maxAngle,
            'maxGen':self.maxGen,
            'report':self.report,
            'TimeAndFitness':time_and_fitness}
        print('total cost time: {:.4f} [s]'.format(time_spand))
        self.done.emit(mechanism, time_spand)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
