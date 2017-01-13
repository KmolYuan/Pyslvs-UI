# -*- coding: utf-8 -*-
from .modules import *

class Path_Solving_listbox_show(QWidget, PathSolvingListbox_Dialog):
    def __init__(self, resultData, parent=None):
        super(Path_Solving_listbox_show, self).__init__(parent)
        self.setupUi(self)
        for e in resultData: self.addResult(e)
    
    def addResult(self, e):
        item = QListWidgetItem(e['Algorithm'])
        item.setToolTip(
            "["+e['Algorithm']+"]"+
            "\nAx: %f"%e['Ax']+
            "\nAy: %f"%e['Ay']+
            "\nDx: %f"%e['Dx']+
            "\nDy: %f"%e['Dy']+
            "\nL0: %f"%e['L0']+
            "\nL1: %f"%e['L1']+
            "\nL2: %f"%e['L2']+
            "\nL3: %f"%e['L3']+
            "\nL4: %f"%e['L4']+
            "\nTime spand: %.2f"%e['time']+" s")
        self.Result_list.addItem(item)
