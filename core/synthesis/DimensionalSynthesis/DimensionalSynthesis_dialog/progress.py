# -*- coding: utf-8 -*-

"""The progress dialog of dimensional synthesis algorithm."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QDialog,
    Qt,
    QTimer,
    pyqtSlot,
)
from .Ui_progress import Ui_Dialog
from .thread import WorkerThread
from .options import AlgorithmType
from typing import Dict, Any

class Progress_show(QDialog, Ui_Dialog):
    
    """Progress dialog.
    
    + Batch execute function.
    + Interrupt function.
    """
    
    def __init__(self,
        type_num: AlgorithmType,
        mechanismParams: Dict[str, Any],
        setting: Dict[str, Any],
        parent=None
    ):
        super(Progress_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.rejected.connect(self.closeWork)
        self.mechanisms = []
        #Batch label.
        if 'maxGen' in setting:
            self.limit = setting['maxGen']
            self.batch_label.setText(
                "{} generation(s)".format(self.limit) if self.limit>0 else '∞'
            )
            self.limit_mode = 'maxGen'
        elif 'minFit' in setting:
            self.limit = setting['minFit']
            self.batch_label.setText("fitness less then {}".format(self.limit))
            self.limit_mode = 'minFit'
        elif 'maxTime' in setting:
            self.limit = setting['maxTime']
            self.batch_label.setText("{:02d}:{:02d}:{:02d}".format(
                self.limit // 3600,
                (self.limit % 3600) // 60,
                self.limit % 3600 % 60
            ))
            self.limit_mode = 'maxTime'
        self.loopTime.setEnabled(self.limit > 0)
        #Timer.
        self.time = 0
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.setTime)
        #Worker thread.
        self.work = WorkerThread(type_num, mechanismParams, setting)
        self.work.progress_update.connect(self.setProgress)
        self.work.result.connect(self.getResult)
        self.work.done.connect(self.finish)
    
    @pyqtSlot(int, str)
    def setProgress(self, progress, fitness):
        """Progress bar will always full."""
        value = progress + self.limit * self.work.currentLoop
        if (self.limit_mode in ('minFit', 'maxTime')) or self.limit==0:
            self.progressBar.setMaximum(value)
        self.progressBar.setValue(value)
        self.fitness_label.setText(fitness)
    
    @pyqtSlot()
    def setTime(self):
        """Set time label."""
        self.time += 1
        self.time_label.setText("{:02d}:{:02d}:{:02d}".format(
            self.time // 3600,
            (self.time % 3600) // 60,
            self.time % 3600 % 60
        ))
    
    @pyqtSlot()
    def on_Start_clicked(self):
        """Start the proccess."""
        loop = self.loopTime.value()
        self.progressBar.setMaximum(self.limit * loop)
        #Progress bar will show generations instead of percent.
        if (self.limit_mode in ('minFit', 'maxTime')) or self.limit==0:
            self.progressBar.setFormat("%v generations")
        self.work.setLoop(loop)
        self.timer.start()
        self.work.start()
        self.Start.setEnabled(False)
        self.loopTime.setEnabled(False)
        self.Interrupt.setEnabled(True)
    
    @pyqtSlot(dict, float)
    def getResult(self,
        mechanism: Dict[str, Any],
        time_spand: float
    ):
        """Get the result."""
        self.mechanisms.append(mechanism)
        self.time_spand = time_spand
    
    @pyqtSlot()
    def finish(self):
        """Finish the proccess."""
        self.timer.stop()
        self.accept()
    
    @pyqtSlot()
    def on_Interrupt_clicked(self):
        """Interrupt the proccess."""
        if self.work.isRunning():
            self.work.stop()
            print("The thread has been interrupted.")
    
    @pyqtSlot()
    def closeWork(self):
        """Close the thread."""
        if self.work.isRunning():
            self.work.stop()
            print("The thread has been canceled.")
