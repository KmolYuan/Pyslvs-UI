# -*- coding: utf-8 -*-
from ..QtModules import *
import timeit, numpy
from ..kernel.kernel_getter import build_planar, Genetic, Firefly, DiffertialEvolution

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
        self.socket = None
    def setSocket(self, socket): self.socket = socket
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        alg = 'Genetic' if self.type_num==0 else 'Firefly' if self.type_num==1 else "Differtial Evolution"
        print("Algorithm: "+alg)
        print("Through: {}".format(self.mechanismParams['targetPath']))
        t0 = timeit.default_timer()
        TnF, FP = self.generateProcess(self.type_num, self.mechanismParams, self.GenerateData, self.algorithmPrams)
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
    
    #TODO: Put socket into Cython lib.
    def generateProcess(self, type_num, mechanismParams, GenerateData, algorithmPrams):
        mechanismObj = build_planar(mechanismParams)
        #Genetic Algorithm
        if type_num==0:
            APs = {
                'nParm':GenerateData['nParm'],
                'nPop':algorithmPrams['nPop'], #250
                'pCross':algorithmPrams['pCross'], #0.95
                'pMute':algorithmPrams['pMute'], #0.05
                'pWin':algorithmPrams['pWin'], #0.95
                'bDelta':algorithmPrams['bDelta'], #5.
                'upper':GenerateData['upper'],
                'lower':GenerateData['lower'],
                'maxGen':GenerateData['maxGen'],
                'report':GenerateData['report']}
            self.foo = Genetic(mechanismObj, **APs)
        #Firefly Algorithm
        elif type_num==1:
            APs = {
                'D':GenerateData['nParm'],
                'n':algorithmPrams['n'], #40
                'alpha':algorithmPrams['alpha'], #0.01
                'betaMin':algorithmPrams['betaMin'], #0.2
                'gamma':algorithmPrams['gamma'], #1.
                'beta0':algorithmPrams['beta0'], #1.
                'ub':GenerateData['upper'],
                'lb':GenerateData['lower'],
                'maxGen':GenerateData['maxGen'],
                'report':GenerateData['report']}
            self.foo = Firefly(mechanismObj, **APs)
        #Differential Evolution
        elif type_num==2:
            APs = {
                'D':GenerateData['nParm'],
                'strategy':algorithmPrams['strategy'], #1
                'NP':algorithmPrams['NP'], #190
                'F':algorithmPrams['F'], #0.6
                'CR':algorithmPrams['CR'], #0.9
                'upper':GenerateData['upper'],
                'lower':GenerateData['lower'],
                'maxGen':GenerateData['maxGen'],
                'report':GenerateData['report']}
            self.foo = DiffertialEvolution(mechanismObj, **APs)
        time_and_fitness, fitnessParameter = self.foo.run()
        return([float(k[1]) for k in [e.split(',') for e in time_and_fitness.split(';')[0:-1]]],
            [float(e) for e in fitnessParameter.split(',')])
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True
