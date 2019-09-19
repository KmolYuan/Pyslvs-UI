# -*- coding: utf-8 -*-

"""Thread of dimensional synthesis."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Tuple, List, Dict, Any
from time import perf_counter
from platform import system, release, machine
from psutil import virtual_memory
from numpy.distutils.cpuinfo import cpu
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget
from pyslvs import (
    Genetic,
    Firefly,
    Differential,
    Planar,
)
from pyslvs_ui.core.info import logger
from pyslvs_ui.core.synthesis.thread import BaseThread
from .options import AlgorithmType


class WorkerThread(BaseThread):

    """The QThread class to handle algorithm."""

    progress_update = Signal(int, str)
    result = Signal(dict)

    def __init__(
        self,
        type_num: AlgorithmType,
        mech_params: Dict[str, Any],
        settings: Dict[str, Any],
        parent: QWidget
    ):
        super(WorkerThread, self).__init__(parent)
        self.type_num = type_num
        self.mech_params = mech_params
        self.planar = Planar(self.mech_params)
        self.settings = settings
        self.loop = 1
        self.current_loop = 0
        self.fun = None

    def is_two_kernel(self) -> bool:
        return self.planar.is_two_kernel()

    def set_loop(self, loop: int) -> None:
        """Set the loop times."""
        self.loop = loop

    def run(self) -> None:
        """Start the algorithm loop."""
        for name, path in self.mech_params['Target'].items():
            logger.debug(f"- [P{name}] ({len(path)})")
        t0 = perf_counter()
        for self.current_loop in range(self.loop):
            logger.info(f"Algorithm [{self.current_loop + 1}]: {self.type_num}")
            if self.is_stop:
                # Cancel the remaining tasks
                logger.info("Canceled.")
                continue
            self.result.emit(self.__algorithm())
        logger.info(f"total cost time: {perf_counter() - t0:.02f} [s]")
        self.finished.emit()

    def __algorithm(self) -> Dict[str, Any]:
        """Get the algorithm result."""
        t0 = perf_counter()
        expression, tf = self.__generate_process()
        time_spend = perf_counter() - t0
        cpu_info = cpu.info[0]
        last_gen = tf[-1][0]
        mechanism = {
            'Algorithm': self.type_num.value,
            'time': time_spend,
            'last_gen': last_gen,
            'last_fitness': tf[-1][1],
            'interrupted': str(last_gen) if self.is_stop else 'False',
            'settings': self.settings,
            'hardware_info': {
                'os': f"{system()} {release()} {machine()}",
                'memory': f"{virtual_memory().total / (1 << 30):.04f} GB",
                'cpu': cpu_info.get("model name", cpu_info.get('ProcessorNameString', '')),
            },
            'time_fitness': tf,
        }
        mechanism.update(self.mech_params)
        mechanism['Expression'] = expression
        logger.info(f"cost time: {time_spend:.02f} [s]")
        return mechanism

    def __generate_process(self) -> Tuple[str, List[Tuple[int, float, float]]]:
        """Re-create function object then execute algorithm."""
        if self.type_num == AlgorithmType.RGA:
            foo = Genetic
        elif self.type_num == AlgorithmType.Firefly:
            foo = Firefly
        else:
            foo = Differential
        self.fun = foo(
            self.planar,
            self.settings,
            progress_fun=self.progress_update.emit,
            interrupt_fun=lambda: self.is_stop,
        )
        return self.fun.run()
