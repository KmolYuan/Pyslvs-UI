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
from math import sin, cos, pi
from .Ui_Path_Solving_series import Ui_Dialog as PathSolvingSeries_Dialog

class Path_Solving_series_show(QDialog, PathSolvingSeries_Dialog):
    FORMULA = [lambda x, k, c: k*x+c, lambda x, k, c: k*x**2+c,
        lambda x, k, c: k*cos(x/180*pi)+c, lambda x, k, c: k*sin(x/180*pi)+c]
    def __init__(self, parent=None):
        super(Path_Solving_series_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
    
    @pyqtSlot()
    def on_generateButton_clicked(self):
        scale = 100
        formula = lambda x: self.FORMULA[self.formula.currentIndex()](x, self.coefficientValue.value(), self.constant.value())
        self.path = [((formula(e)/scale, e/scale) if self.reverseX.isChecked() else (e/scale, formula(e)/scale))
            for e in range(int(self.startNum.value()*scale), int(self.endNum.value()*scale), int(self.diffNum.value()*scale))]
