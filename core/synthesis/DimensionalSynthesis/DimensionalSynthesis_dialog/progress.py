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
    QDialog,
    Qt,
    QTimer,
    pyqtSlot,
)
from .Ui_progress import Ui_Dialog
from .thread import WorkerThread

class Progress_show(QDialog, Ui_Dialog):
    def __init__(self, type_num, mechanismParams, setting, parent=None):
        super(Progress_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.rejected.connect(self.closeWork)
        self.mechanisms = []
        #Batch label.
        if 'maxGen' in setting:
            self.limit = setting['maxGen']
            self.batch_label.setText("{} generation(s)".format(self.limit) if self.limit>0 else '∞')
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
        self.loopTime.setEnabled(self.limit>0)
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
        value = progress + self.limit * self.work.currentLoop
        #Progress bar will always full.
        if (self.limit_mode in ('minFit', 'maxTime')) or self.limit==0:
            self.progressBar.setMaximum(value)
        self.progressBar.setValue(value)
        self.fitness_label.setText(fitness)
    
    @pyqtSlot()
    def setTime(self):
        self.time += 1
        self.time_label.setText("{:02d}:{:02d}:{:02d}".format(
            self.time // 3600,
            (self.time % 3600) // 60,
            self.time % 3600 % 60
        ))
    
    @pyqtSlot()
    def on_Start_clicked(self):
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
    def getResult(self, mechanism, time_spand):
        self.mechanisms.append(mechanism)
        self.time_spand = time_spand
    
    @pyqtSlot()
    def finish(self):
        self.timer.stop()
        self.accept()
    
    @pyqtSlot()
    def on_Interrupt_clicked(self):
        if self.work.isRunning():
            self.work.stop()
            print("The thread has been interrupted.")
    
    @pyqtSlot()
    def closeWork(self):
        if self.work.isRunning():
            self.work.stop()
            print("The thread has been canceled.")
