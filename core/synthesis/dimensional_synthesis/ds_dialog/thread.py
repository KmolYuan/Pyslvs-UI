# -*- coding: utf-8 -*-

"""Thread of dimensional synthesis."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Dict,
    Any,
)
from time import time
import platform
from psutil import virtual_memory
import numpy
import numpy.distutils.cpuinfo
from core.QtModules import pyqtSignal, QThread
from core.libs import (
    Genetic,
    Firefly,
    DiffertialEvolution,
    Planar,
)
from .options import AlgorithmType


class WorkerThread(QThread):
    
    """The QThread class to handle algorithm."""
    
    progress_update = pyqtSignal(int, str)
    result = pyqtSignal(dict, float)
    done = pyqtSignal()
    
    def __init__(
        self,
        type_num: AlgorithmType,
        mech_params: Dict[str, Any],
        settings: Dict[str, Any]
    ):
        """Input settings from dialog, then call public method 'start'
        to start the algorithm.
        """
        super(WorkerThread, self).__init__(None)
        self.stoped = False
        self.type_num = type_num
        self.mech_params = mech_params
        self.settings = settings
        self.loop = 1
    
    def setLoop(self, loop: int):
        """Set the loop times."""
        self.loop = loop
    
    def run(self):
        """Start the algorithm loop."""
        for name, path in self.mech_params['Target'].items():
            print(f"- [{name}]: {path}")
        mechanismObj = Planar(self.mech_params)
        if self.type_num == AlgorithmType.RGA:
            foo = Genetic
        elif self.type_num == AlgorithmType.Firefly:
            foo = Firefly
        elif self.type_num == AlgorithmType.DE:
            foo = DiffertialEvolution
        self.fun = foo(
            mechanismObj,
            self.settings,
            progress_fun = self.progress_update.emit,
            interrupt_fun = self.__isStoped,
        )
        t0 = time()
        self.currentLoop = 0
        for self.currentLoop in range(self.loop):
            print(f"Algorithm [{self.currentLoop + 1}]: {self.type_num}")
            if self.stoped:
                # Cancel the remaining tasks.
                print("Canceled.")
                continue
            mechanism, time_spand = self.__algorithm()
            self.result.emit(mechanism, time_spand)
        print(f"total cost time: {time() - t0:.02f} [s]")
        self.done.emit()
    
    def __algorithm(self) -> Tuple[Dict[str, Any], float]:
        """Get the algorithm result."""
        t0 = time()
        params, tf = self.__generateProcess()
        time_spend = time() - t0
        cpu = numpy.distutils.cpuinfo.cpu.info[0]
        last_gen = tf[-1][0]
        mechanism = {
            'Algorithm': self.type_num.value,
            'time': time_spend,
            'last_gen': last_gen,
            'interrupted': str(last_gen) if self.stoped else 'False',
            'settings': self.settings,
            'hardware_info': {
                'os': f"{platform.system()} {platform.release()} {platform.machine()}",
                'memory': f"{virtual_memory().total / (1 << 30):.04f} GB",
                'cpu': cpu.get("model name", cpu.get('ProcessorNameString', '')),
            },
            'time_fitness': tf,
        }
        mechanism.update(self.mech_params)
        mechanism.update(params)
        print(f"cost time: {time_spend:.02f} [s]")
        return mechanism, time_spend
    
    def __generateProcess(self) -> Tuple[
        Dict[str, Any],
        List[Tuple[int, float, float]]
    ]:
        """Execute algorithm and sort out the result."""
        params, tf = self.fun.run()
        return params, tf
    
    def __isStoped(self) -> bool:
        """Return stop status for Cython function."""
        return self.stoped
    
    def stop(self):
        """Stop the algorithm."""
        self.stoped = True
