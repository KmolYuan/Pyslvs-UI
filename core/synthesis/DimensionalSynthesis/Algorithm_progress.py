# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
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

from ...QtModules import *
import zmq
from .Ui_Algorithm_progress import Ui_Dialog
from .pathSolving import WorkerThread

class Algorithm_progress_show(QDialog, Ui_Dialog):
    def __init__(self, type_num, mechanismParams, setting, PORT=None, parent=None):
        super(Algorithm_progress_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.rejected.connect(self.closeWork)
        self.maxGen = setting['maxGen']
        self.loopTime.setEnabled(self.maxGen>0)
        self.maxGen_label.setText(str(self.maxGen) if self.maxGen>0 else '∞')
        self.mechanisms = []
        self.work = WorkerThread(type_num, mechanismParams, setting)
        self.work.progress_update.connect(self.setProgress)
        self.work.result.connect(self.getResult)
        self.work.done.connect(self.finish)
        if PORT is None:
            self.label.setText(
                "<html><head/><body><p><span style=\"font-size:12pt;\">"+
                "This action will take some time, depending on the length of path, "+
                "advanced settings and your computer performance.</p></body></html>"
            )
            self.argumentText.hide()
        else:
            context = zmq.Context()
            self.socket = context.socket(zmq.REQ)
            try:
                self.socket.bind(PORT)
                self.socket.setsockopt(zmq.LINGER, 0)
                self.socket.close()
            except:
                QMessageBox.warning(self, "Connect Error",
                    "The following address are not available:\n{}".format(PORT),
                    QMessageBox.Ok, QMessageBox.Ok
                )
                self.reject()
            self.argumentText.setText("--server tcp://localhost:{}".format(PORT.split(':')[2]))
            self.work.setSocket(PORT)
    
    @pyqtSlot(int, str)
    def setProgress(self, progress, fitness):
        if self.maxGen==0:
            self.progressBar.setMaximum(progress)
        self.progressBar.setValue(progress+self.maxGen*self.work.currentLoop)
        self.fitness_label.setText(fitness)
    
    @pyqtSlot()
    def on_Start_clicked(self):
        loop = self.loopTime.value()
        self.progressBar.setMaximum(self.maxGen*loop)
        if self.maxGen==0:
            self.progressBar.setFormat("%v generations")
        self.work.setLoop(loop)
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
