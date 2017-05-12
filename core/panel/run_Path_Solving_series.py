# -*- coding: utf-8 -*-
from ..QtModules import *
from math import sin, cos, pi
from .Ui_run_Path_Solving_series import Ui_Dialog as PathSolvingSeries_Dialog

class Path_Solving_series_show(QDialog, PathSolvingSeries_Dialog):
    FORMULA = [lambda x, k, c: k*x+c, lambda x, k, c: k*x**2+c,
        lambda x, k, c: k*cos(x/180*pi)+c, lambda x, k, c: k*sin(x/180*pi)+c]
    def __init__(self, parent=None):
        super(Path_Solving_series_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot()
    def on_generateButton_clicked(self):
        scale = 100
        formula = lambda x: self.FORMULA[self.formula.currentIndex()](x, self.coefficientValue.value(), self.constant.value())
        self.path = [((formula(e)/scale, e/scale) if self.reverseX.isChecked() else (e/scale, formula(e)/scale))
            for e in range(int(self.startNum.value()*scale), int(self.endNum.value()*scale), int(self.diffNum.value()*scale))]
