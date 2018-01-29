# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang
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

from core.QtModules import *
import timeit
import platform
import numpy
import numpy.distutils.cpuinfo
from psutil import virtual_memory
from core import libs
from core import server
from core.libs import build_planar

class WorkerThread(QThread):
    progress_update = pyqtSignal(int, str)
    result = pyqtSignal(dict, float)
    done = pyqtSignal()
    
    def __init__(self, type_num, mechanismParams, settings, parent):
        super(WorkerThread, self).__init__(None)
        self.stoped = False
        self.mutex = QMutex()
        self.type_num = type_num
        self.mechanismParams = mechanismParams
        self.settings = settings
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
            for name, path in self.mechanismParams['Target'].items():
                print("- [{}]: {}".format(name, tuple((round(x, 2), round(y, 2)) for x, y in path)))
            t0 = timeit.default_timer()
            fitnessParameter, time_and_fitness = self.generateProcess()
            t1 = timeit.default_timer()
            time_spand = round(t1-t0, 2)
            cpu = numpy.distutils.cpuinfo.cpu.info[0]
            mechanism = {
                'Algorithm':'RGA' if self.type_num==0 else 'Firefly' if self.type_num==1 else 'DE',
                'time':time_spand,
                'interrupted':str(time_and_fitness[-1][0]) if self.stoped else 'False',
                'settings':self.settings,
                'hardwareInfo':{
                    'os':"{} {} {}".format(platform.system(), platform.release(), platform.machine()),
                    'memory':"{} GB".format(round(virtual_memory().total/(1024.**3), 4)),
                    'cpu':cpu.get("model name", cpu.get('ProcessorNameString', '')),
                    'network':str(self.socket!=None)
                },
                'TimeAndFitness':time_and_fitness
            }
            mechanism.update(self.mechanismParams)
            mechanism.update(fitnessParameter)
            print("cost time: {} [s]".format(time_spand))
            self.result.emit(mechanism, time_spand)
        T1 = timeit.default_timer()
        totalTime = round(T1-T0, 2)
        print("total cost time: {} [s]".format(totalTime))
        self.done.emit()
    
    def generateProcess(self):
        if self.socket!=None:
            Genetic = server.Genetic
            Firefly = server.Firefly
            DiffertialEvolution = server.DiffertialEvolution
        else:
            Genetic = libs.Genetic
            Firefly = libs.Firefly
            DiffertialEvolution = libs.DiffertialEvolution
        mechanismObj = build_planar(self.mechanismParams)
        #Genetic Algorithm
        if self.type_num==0:
            foo = Genetic
        #Firefly Algorithm
        elif self.type_num==1:
            foo = Firefly
        #Differential Evolution
        elif self.type_num==2:
            foo = DiffertialEvolution
        if self.socket!=None:
            self.settings['socket_port'] = self.socket
            self.settings['Target'] = self.mechanismParams['Target']
        self.fun = foo(
            mechanismObj,
            self.settings,
            progress_fun=self.progress_update.emit,
            interrupt_fun=self.isStoped,
        )
        fitnessParameter, time_and_fitness = self.fun.run()
        return(
            fitnessParameter,
            tuple((int(e.split(',')[0]), float(e.split(',')[1]), float(e.split(',')[2])) for e in time_and_fitness.split(';')[0:-1])
        )
    
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True
    
    def isStoped(self):
        return self.stoped
