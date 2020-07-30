# -*- coding: utf-8 -*-

"""Thread of dimensional synthesis."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Dict, Any
from time import process_time
from platform import system, release, machine
from psutil import virtual_memory
from numpy.distutils.cpuinfo import cpu
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget
from pyslvs import FMatch
from pyslvs.metaheuristics import ALGORITHM, AlgorithmType
from pyslvs_ui.info import logger
from pyslvs_ui.synthesis.thread import BaseThread


class DimensionalThread(BaseThread):
    """The QThread class to handle algorithm."""
    progress_update = Signal(int, str)
    result = Signal(dict)

    def __init__(
        self,
        algorithm: AlgorithmType,
        mech: Dict[str, Any],
        settings: Dict[str, Any],
        parent: QWidget
    ):
        super(DimensionalThread, self).__init__(parent)
        self.algorithm = algorithm
        self.mech = mech
        self.planar = FMatch(self.mech)
        self.settings = settings
        self.loop = 1

    def is_two_kernel(self) -> bool:
        return self.planar.is_two_kernel()

    def set_loop(self, loop: int) -> None:
        """Set the loop times."""
        self.loop = loop

    def run(self) -> None:
        """Start the algorithm loop."""
        for name, path in self.mech['target'].items():
            logger.debug(f"- [P{name}] ({len(path)})")
        t0 = process_time()
        for self.loop in range(self.loop):
            logger.info(f"Algorithm [{self.loop + 1}]: {self.algorithm}")
            if self.is_stop:
                # Cancel the remaining tasks
                logger.info("Canceled.")
                continue
            self.result.emit(self.__algorithm())
        logger.info(f"total cost time: {process_time() - t0:.02f} [s]")
        self.finished.emit()

    def __algorithm(self) -> Dict[str, Any]:
        """Get the algorithm result."""
        t0 = process_time()
        algorithm = ALGORITHM[self.algorithm](
            self.planar,
            self.settings,
            progress_fun=self.progress_update.emit,
            interrupt_fun=lambda: self.is_stop,
        )
        expression = algorithm.run()
        tf = algorithm.history()
        time_spend = process_time() - t0
        info = cpu.info[0]
        my_cpu = info.get("model name", info.get('ProcessorNameString', ''))
        last_gen = tf[-1][0]
        mechanism = {
            'algorithm': self.algorithm.value,
            'time': time_spend,
            'last_gen': last_gen,
            'last_fitness': tf[-1][1],
            'interrupted': str(last_gen) if self.is_stop else 'False',
            'settings': self.settings,
            'hardware_info': {
                'os': f"{system()} {release()} {machine()}",
                'memory': f"{virtual_memory().total / (1 << 30):.04f} GB",
                'cpu': my_cpu,
            },
            'time_fitness': tf,
        }
        mechanism.update(self.mech)
        mechanism['expression'] = expression
        logger.info(f"cost time: {time_spend:.02f} [s]")
        return mechanism
