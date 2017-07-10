# -*- coding: utf-8 -*-
from ...QtModules import *
import zmq
from .Ui_Path_Solving_progress_zmq import Ui_Dialog
from ...calculation.pathSolving import WorkerThread

class Path_Solving_progress_zmq_show(QDialog, Ui_Dialog):
    def __init__(self, type_num, mechanismParams, GenerateData, algorithmPrams, PORT=None, parent=None):
        super(Path_Solving_progress_zmq_show, self).__init__(parent)
        self.setupUi(self)
        self.rejected.connect(self.closeWork)
        msgGeo = QApplication.desktop().availableGeometry()
        self.move(msgGeo.topLeft())
        self.work = WorkerThread(type_num, mechanismParams, GenerateData, algorithmPrams)
        self.work.done.connect(self.finish)
        if PORT is None:
            self.label.setText("<html><head/><body><p><span style=\"font-size:12pt;\">"+
                "This action will take some time, depending on the number of path points and your computer performance."+
                "<br/><br/>Please wait patiently.</p></body></html>")
            self.argumentText.hide()
        else:
            context = zmq.Context()
            self.socket = context.socket(zmq.REQ)
            try: self.socket.bind(PORT)
            except:
                dlgbox = QMessageBox(QMessageBox.Warning, "Connect Error",
                    "The following address are not available:\n{}".format(PORT), (QMessageBox.Ok), self)
                if dlgbox.exec_(): self.reject()
            self.argumentText.setText("--server tcp://localhost:{}".format(PORT.split(':')[1]))
            self.work.setSocket(self.socket)
    
    @pyqtSlot()
    def on_Start_clicked(self):
        self.work.start()
        self.Start.setEnabled(False)
        self.buttonBox.setEnabled(False)
        self.progressBar.setRange(0, 0)
        print("Start Path Solving...")
    
    @pyqtSlot(dict, int)
    def finish(self, mechanism, time_spand):
        self.mechanism = mechanism
        self.time_spand = time_spand
        self.accept()
    
    @pyqtSlot()
    def closeWork(self):
        if self.work.isRunning():
            self.work.exit()
            self.work.wait()
            print("The thread has been canceled.")
