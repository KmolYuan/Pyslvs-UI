# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from ..QtModules import *
import timeit
import platform
import numpy
import numpy.distutils.cpuinfo
from psutil import virtual_memory
from ..kernel.pyslvs_algorithm import tinycadlib
from ..kernel.pyslvs_algorithm.planarlinkage import build_planar

class WorkerThread(QThread):
    progress_update = pyqtSignal(int, str)
    result = pyqtSignal(dict, float)
    done = pyqtSignal()
    def __init__(self, type_num, mechanismParams, generateData, algorithmPrams, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.type_num = type_num
        self.mechanismParams = mechanismParams
        self.generateData = generateData
        self.algorithmPrams = algorithmPrams
        self.socket = None
        self.loop = 1
        self.currentLoop = 0
    
    def setSocket(self, socket):
        self.socket = socket
    
    def setLoop(self, loop):
        self.loop = loop
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        T0 = timeit.default_timer()
        for self.currentLoop in range(self.loop):
            print("Algorithm [{}]: {}".format(self.currentLoop,
                "Genetic Algorithm" if self.type_num==0 else "Firefly Algorithm" if self.type_num==1 else "Differtial Evolution"))
            if self.stoped:
                #Cancel the remaining tasks.
                print("Canceled.")
                continue
            print("Through: {}".format(self.mechanismParams['targetPath']))
            t0 = timeit.default_timer()
            TnF, FP = self.generateProcess()
            t1 = timeit.default_timer()
            time_spand = round(t1-t0, 2)
            mem = virtual_memory()
            cpu = numpy.distutils.cpuinfo.cpu.info[0]
            mechanism = {
                'Algorithm':'RGA' if self.type_num==0 else 'Firefly' if self.type_num==1 else 'DE',
                'time':time_spand,
                'Ax':FP[0], 'Ay':FP[1],
                'Dx':FP[2], 'Dy':FP[3],
                'interruptedGeneration':str(TnF[-1][0]) if self.stoped else 'False',
                'mechanismParams':self.mechanismParams,
                'generateData':self.generateData,
                'algorithmPrams':self.algorithmPrams,
                'hardwareInfo':{
                    'os':"{} {} {}".format(platform.system(), platform.release(), platform.machine()),
                    'memory':"{} GB".format(round(mem.total/(1024.**3), 4)),
                    'cpu':cpu.get("model name", cpu.get('ProcessorNameString', '')),
                    'network':str(self.socket!=None)},
                'TimeAndFitness':TnF}
            for index in range(len(self.mechanismParams['Link'].split(','))):
                mechanism['L{}'.format(index)] = FP[4+index]
            print('cost time: {} [s]'.format(time_spand))
            self.result.emit(mechanism, time_spand)
        T1 = timeit.default_timer()
        totalTime = round(T1-T0, 2)
        print('total cost time: {} [s]'.format(totalTime))
        self.done.emit()
    
    def generateProcess(self):
        if self.socket!=None:
            from ..server.rga import Genetic
            from ..server.firefly import Firefly
            from ..server.de import DiffertialEvolution
        else:
            from ..kernel.pyslvs_algorithm.rga import Genetic
            from ..kernel.pyslvs_algorithm.firefly import Firefly
            from ..kernel.pyslvs_algorithm.de import DiffertialEvolution
        mechanismObj = build_planar(self.mechanismParams)
        #Genetic Algorithm
        if self.type_num==0:
            APs = {
                'nParm':self.generateData['nParm'],
                'nPop':self.algorithmPrams['nPop'], #250
                'pCross':self.algorithmPrams['pCross'], #0.95
                'pMute':self.algorithmPrams['pMute'], #0.05
                'pWin':self.algorithmPrams['pWin'], #0.95
                'bDelta':self.algorithmPrams['bDelta'], #5.
                'upper':self.generateData['upper'],
                'lower':self.generateData['lower'],
                'maxGen':self.generateData['maxGen'],
                'report':self.generateData['report']}
            foo = Genetic
        #Firefly Algorithm
        elif self.type_num==1:
            APs = {
                'D':self.generateData['nParm'],
                'n':self.algorithmPrams['n'], #40
                'alpha':self.algorithmPrams['alpha'], #0.01
                'betaMin':self.algorithmPrams['betaMin'], #0.2
                'gamma':self.algorithmPrams['gamma'], #1.
                'beta0':self.algorithmPrams['beta0'], #1.
                'ub':self.generateData['upper'],
                'lb':self.generateData['lower'],
                'maxGen':self.generateData['maxGen'],
                'report':self.generateData['report']}
            foo = Firefly
        #Differential Evolution
        elif self.type_num==2:
            APs = {
                'D':self.generateData['nParm'],
                'strategy':self.algorithmPrams['strategy'], #1
                'NP':self.algorithmPrams['NP'], #190
                'F':self.algorithmPrams['F'], #0.6
                'CR':self.algorithmPrams['CR'], #0.9
                'upper':self.generateData['upper'],
                'lower':self.generateData['lower'],
                'maxGen':self.generateData['maxGen'],
                'report':self.generateData['report']}
            foo = DiffertialEvolution
        if self.socket!=None:
            APs['socket_port'] = self.socket
            APs['targetPath'] = self.mechanismParams['targetPath']
        self.fun = foo(mechanismObj,
            progress_fun=self.progress_update.emit,
            interrupt_fun=self.isStoped,
            **APs)
        time_and_fitness, fitnessParameter = self.fun.run()
        return(tuple(tuple([int(e.split(',')[0]), float(e.split(',')[1]), float(e.split(',')[2])]) for e in time_and_fitness.split(';')[0:-1]),
            [float(e) for e in fitnessParameter.split(',')])
    
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True
    
    def isStoped(self):
        return self.stoped
