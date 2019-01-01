# -*- coding: utf-8 -*-

"""Thread of dimensional synthesis."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Dict,
    Any,
)
from time import time
from platform import (
    system,
    release,
    machine,
)
from psutil import virtual_memory
import numpy
import numpy.distutils.cpuinfo
from core.QtModules import pyqtSignal, QThread
from core.libs import (
    Genetic,
    Firefly,
    Differential,
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
        super(WorkerThread, self).__init__()
        self.is_stop = False
        self.type_num = type_num
        self.mech_params = mech_params
        self.settings = settings
        self.loop = 1
        self.currentLoop = 0
        self.fun = None

    def setLoop(self, loop: int):
        """Set the loop times."""
        self.loop = loop

    def run(self):
        """Start the algorithm loop."""
        for name, path in self.mech_params['Target'].items():
            print(f"- [{name}]: {path}")
        t0 = time()
        for self.currentLoop in range(self.loop):
            print(f"Algorithm [{self.currentLoop + 1}]: {self.type_num}")
            if self.is_stop:
                # Cancel the remaining tasks.
                print("Canceled.")
                continue
            mechanism, time_spend = self.__algorithm()
            self.result.emit(mechanism, time_spend)
        print(f"total cost time: {time() - t0:.02f} [s]")
        self.done.emit()

    def __algorithm(self) -> Tuple[Dict[str, Any], float]:
        """Get the algorithm result."""
        t0 = time()
        params, tf = self.__generate_process()
        time_spend = time() - t0
        cpu = numpy.distutils.cpuinfo.cpu.info[0]
        last_gen = tf[-1][0]
        mechanism = {
            'Algorithm': self.type_num.value,
            'time': time_spend,
            'last_gen': last_gen,
            'interrupted': str(last_gen) if self.is_stop else 'False',
            'settings': self.settings,
            'hardware_info': {
                'os': f"{system()} {release()} {machine()}",
                'memory': f"{virtual_memory().total / (1 << 30):.04f} GB",
                'cpu': cpu.get("model name", cpu.get('ProcessorNameString', '')),
            },
            'time_fitness': tf,
        }
        mechanism.update(self.mech_params)
        mechanism.update(params)
        print(f"cost time: {time_spend:.02f} [s]")
        return mechanism, time_spend

    def __generate_process(self) -> Tuple[
        Dict[str, Any],
        List[Tuple[int, float, float]]
    ]:
        """Re-create function object then execute algorithm."""
        if self.type_num == AlgorithmType.RGA:
            foo = Genetic
        elif self.type_num == AlgorithmType.Firefly:
            foo = Firefly
        else:
            foo = Differential
        self.fun = foo(
            Planar(self.mech_params),
            self.settings,
            progress_fun=self.progress_update.emit,
            interrupt_fun=self.__is_stop,
        )
        params, tf = self.fun.run()
        # Note: Remove numpy 'scalar' format.
        return eval(str(params)), tf

    def __is_stop(self) -> bool:
        """Return stop status for Cython function."""
        return self.is_stop

    def stop(self):
        """Stop the algorithm."""
        self.is_stop = True
