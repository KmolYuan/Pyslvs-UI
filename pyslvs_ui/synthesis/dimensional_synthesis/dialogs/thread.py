# -*- coding: utf-8 -*-

"""Thread of dimensional synthesis."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, Dict, Any
from time import process_time
from platform import system, release, machine, processor
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QWidget
from pyslvs.optimization import FPlanar, FConfig
from pyslvs.metaheuristics import algorithm, AlgorithmType, Setting
from pyslvs_ui.info import logger
from pyslvs_ui.synthesis.thread import BaseThread


class DimensionalThread(BaseThread):
    """The QThread class to handle algorithm."""
    progress_update = Signal(int, str)
    result = Signal(dict)

    def __init__(
        self,
        alg: AlgorithmType,
        mech: Dict[str, Any],
        settings: Dict[str, Any],
        parent: QWidget
    ):
        super(DimensionalThread, self).__init__(parent)
        self.alg = alg
        self.mech = cast(FConfig, mech)
        self.planar = FPlanar(self.mech)
        self.settings = cast(Setting, settings)
        self.loop = 1

    def set_loop(self, loop: int) -> None:
        """Set the loop times."""
        self.loop = loop

    def run(self) -> None:
        """Start the algorithm loop."""
        for name, path in self.mech['target'].items():
            logger.debug(f"- [P{name}] ({len(path)})")
        t0 = process_time()
        for self.loop in range(self.loop):
            logger.info(f"Algorithm [{self.loop + 1}]: {self.alg}")
            if self.is_stop:
                # Cancel the remaining tasks
                logger.info("Canceled.")
                continue
            self.result.emit(self.__task())
        logger.info(f"total cost time: {process_time() - t0:.02f} [s]")
        self.finished.emit()

    def __task(self) -> Dict[str, Any]:
        """Get the algorithm result."""
        t0 = process_time()
        a = algorithm(self.alg)(
            self.planar,
            self.settings,
            progress_fun=self.progress_update.emit,
            interrupt_fun=lambda: self.is_stop,
        )
        expression = a.run()
        tf = a.history()
        time_spend = process_time() - t0
        last_gen = tf[-1][0]
        mechanism = {
            'algorithm': self.alg.value,
            'time': time_spend,
            'last_gen': last_gen,
            'last_fitness': tf[-1][1],
            'interrupted': str(last_gen) if self.is_stop else 'False',
            'settings': self.settings,
            'hardware_info': {
                'os': f"{system()} {release()} {machine()}",
                'cpu': processor(),
            },
            'time_fitness': tf,
            'callback': self.planar.callback,
        }
        mechanism.update(self.mech)
        mechanism['expression'] = expression
        logger.info(f"cost time: {time_spend:.02f} [s]")
        return mechanism
