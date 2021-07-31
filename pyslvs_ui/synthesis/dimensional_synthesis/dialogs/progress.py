# -*- coding: utf-8 -*-

"""The progress dialog of dimensional synthesis algorithm."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List, Dict, Any
from qtpy.QtCore import Qt, QTimer, Signal, Slot
from qtpy.QtWidgets import QDialog
from pyslvs.metaheuristics import AlgorithmType
from pyslvs_ui.info import logger
from .progress_ui import Ui_Dialog
from .thread import DimensionalThread


class ProgressDialog(QDialog, Ui_Dialog):
    """Progress dialog.

    + Batch execute function.
    + Interrupt function.
    """
    mechanisms: List[Dict[str, Any]]

    stop_signal = Signal()

    def __init__(
        self,
        algorithm: AlgorithmType,
        mech: Dict[str, Any],
        setting: Dict[str, Any],
        parent
    ):
        super(ProgressDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        self.rejected.connect(self.__close_work)

        self.mechanisms = []
        # Batch label
        if 'max_gen' in setting:
            self.limit = setting['max_gen']
            if self.limit > 0:
                self.batch_label.setText(f"{self.limit} generation(s)")
            else:
                self.batch_label.setText('∞')
            self.limit_mode = 'max_gen'
        elif 'min_fit' in setting:
            self.limit = setting['min_fit']
            self.batch_label.setText(f"fitness less then {self.limit}")
            self.limit_mode = 'min_fit'
        elif 'max_time' in setting:
            self.limit = setting['max_time']
            self.batch_label.setText(
                f"{self.limit // 3600:02d}:"
                f"{self.limit % 3600 // 60:02d}:"
                f"{self.limit % 3600 % 60:02d}"
            )
            self.limit_mode = 'max_time'
        else:
            self.limit = 0
            self.batch_label.setText('∞')
            self.limit_mode = 'max_gen'
        self.loopTime.setEnabled(self.limit > 0)

        # Timer
        self.time = 0
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.__set_time)
        self.time_spend = 0.

        # Worker thread
        self.work = DimensionalThread(algorithm, mech, setting, self)
        self.stop_signal.connect(self.work.stop)
        if self.work.planar.is_two_kernel():
            self.fast_kernel_label.hide()
        else:
            self.full_kernel_label.hide()
        self.work.progress_update.connect(self.__set_progress)
        self.work.result.connect(self.__get_result)
        self.work.finished.connect(self.__finish)

    @Slot(int, str)
    def __set_progress(self, progress: int, fitness: str) -> None:
        """Progress bar will always full if no generation counter."""
        value = progress + self.limit * self.work.loop
        if self.limit_mode in {'min_fit', 'max_time'} or self.limit == 0:
            self.progress_bar.setMaximum(value)
        self.progress_bar.setValue(value)
        self.fitness_label.setText(fitness)

    @Slot()
    def __set_time(self) -> None:
        """Set time label."""
        self.time += 1
        t_min = self.time % 3600
        self.time_label.setText(
            f"{self.time // 3600:02d}:"
            f"{t_min // 60:02d}:"
            f"{t_min % 60:02d}"
        )

    @Slot(name='on_start_btn_clicked')
    def __start(self) -> None:
        """Start the process."""
        loop = self.loopTime.value()
        self.progress_bar.setMaximum(self.limit * loop)
        if self.limit_mode in {'min_fit', 'max_time'} or self.limit == 0:
            # Progress bar will show generations instead of percent
            self.progress_bar.setFormat("%v generations")
        self.work.set_loop(loop)
        self.timer.start()
        self.work.start()
        self.start_btn.setEnabled(False)
        self.loopTime.setEnabled(False)
        self.interrupt_btn.setEnabled(True)

    @Slot(dict)
    def __get_result(self, mechanism: Dict[str, Any]) -> None:
        """Get the result."""
        self.mechanisms.append(mechanism)
        self.time_spend += mechanism['time']

    @Slot()
    def __finish(self) -> None:
        """Finish the process."""
        self.timer.stop()
        self.work.wait()
        self.accept()

    @Slot(name='on_interrupt_btn_clicked')
    def __interrupt(self) -> None:
        """Interrupt the process."""
        if self.work.isRunning():
            self.stop_signal.emit()
            logger.info("The thread has been interrupted.")

    @Slot()
    def __close_work(self) -> None:
        """Close the thread."""
        if not self.work.isRunning():
            return
        self.stop_signal.emit()
        logger.info("The thread has been canceled.")
        self.work.wait()
