# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
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

from core.QtModules import (
    QThread,
    pyqtSignal,
    QMutex,
    QMutexLocker,
)
import timeit
import platform
import numpy
import numpy.distutils.cpuinfo
from psutil import virtual_memory
from core.libs import (
    Genetic,
    Firefly,
    DiffertialEvolution,
)
from core.libs import build_planar
from . import AlgorithmType

class WorkerThread(QThread):
    progress_update = pyqtSignal(int, str)
    result = pyqtSignal(dict, float)
    done = pyqtSignal()
    
    def __init__(self, type_num: AlgorithmType, mechanismParams, settings):
        super(WorkerThread, self).__init__(None)
        self.stoped = False
        self.mutex = QMutex()
        self.type_num = type_num
        self.mechanismParams = mechanismParams
        self.settings = settings
        self.loop = 1
        self.currentLoop = 0
    
    def setLoop(self, loop):
        self.loop = loop
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        T0 = timeit.default_timer()
        for self.currentLoop in range(self.loop):
            print("Algorithm [{}]: {}".format(self.currentLoop, self.type_num))
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
            lastGen = time_and_fitness[-1][0]
            mechanism = {
                'time': time_spand,
                'lastGen': lastGen,
                'interrupted': str(lastGen) if self.stoped else 'False',
                'settings': self.settings,
                'hardwareInfo': {
                    'os': "{} {} {}".format(platform.system(), platform.release(), platform.machine()),
                    'memory': "{} GB".format(round(virtual_memory().total/(1024.**3), 4)),
                    'cpu': cpu.get("model name", cpu.get('ProcessorNameString', ''))
                },
                'TimeAndFitness': time_and_fitness
            }
            mechanism['Algorithm'] = self.type_num.value
            mechanism.update(self.mechanismParams)
            mechanism.update(fitnessParameter)
            print("cost time: {} [s]".format(time_spand))
            self.result.emit(mechanism, time_spand)
        T1 = timeit.default_timer()
        totalTime = round(T1-T0, 2)
        print("total cost time: {} [s]".format(totalTime))
        self.done.emit()
    
    def generateProcess(self):
        mechanismObj = build_planar(self.mechanismParams)
        if self.type_num == AlgorithmType.RGA:
            foo = Genetic
        elif self.type_num == AlgorithmType.Firefly:
            foo = Firefly
        elif self.type_num == AlgorithmType.DE:
            foo = DiffertialEvolution
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
