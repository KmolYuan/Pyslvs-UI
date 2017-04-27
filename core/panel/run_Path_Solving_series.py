# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Path_Solving_series import Ui_Dialog as PathSolvingSeries_Dialog

class Path_Solving_series_show(QDialog, PathSolvingSeries_Dialog):
    def __init__(self, parent=None):
        super(Path_Solving_series_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_generateButton_clicked(self):
        start = int(self.startNum.value()*10)
        end = int(self.endNum.value()*10)
        diff = int(self.diffNum.value()*10)
        self.path = [(e/10, e/10) for e in range(start, end, diff)]
