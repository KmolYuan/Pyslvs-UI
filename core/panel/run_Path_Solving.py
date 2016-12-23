# -*- coding: utf-8 -*-
from .modules import *
from ..calculation.pathSolving import WorkerThread

class Path_Solving_show(QDialog, PathSolving_Dialog):
    def __init__(self, parent=None):
        super(Path_Solving_show, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkerThread()
    
    def readPath(self, data):
        self.work.setPath(data)
