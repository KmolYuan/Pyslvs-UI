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

from core.QtModules import *
import numpy as np
from .Ui_path_adjust import Ui_Dialog

#Return a 2D fitting equation.
def polyfit(x, y, d: int):
    coeffs = np.polyfit(x, y, d)
    #Fit values and mean.
    yhat = np.poly1d(coeffs)(x)
    ybar = np.sum(y)/len(y)
    return (
        lambda t: sum(c * t**power for power, c in enumerate(reversed(coeffs))),
        np.sum((yhat - ybar)**2)/np.sum((y - ybar)**2)
    )

class Path_adjust_show(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(Path_adjust_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.path = parent.currentPath()
        self.r_path = []
        for x, y in self.path:
            self.path_list.addItem("({}, {})".format(x, y))
        self.points_num.setText(str(len(self.path)))
        self.match_num.setValue(len(self.path))
    
    @pyqtSlot()
    def on_scaling_button_clicked(self):
        self.r_path = [
            (
                self.scaling_rx.value() + (x - self.scaling_rx.value())*self.scaling_h.value(),
                self.scaling_ry.value() + (y - self.scaling_ry.value())*self.scaling_v.value()
            ) for x, y in self.path
        ]
        self.accept()
    
    @pyqtSlot()
    def on_moving_button_clicked(self):
        self.r_path = [
            (x + self.moving_x_coordinate.value(), y + self.moving_y_coordinate.value())
            for x, y in self.path
        ]
        self.accept()
    
    @pyqtSlot()
    def on_match_button_clicked(self):
        l = len(self.path)
        if l==0:
            return
        index = list(range(l))
        x_func, x_accuracy = polyfit(index, [x for x, y in self.path], 4)
        y_func, y_accuracy = polyfit(index, [y for x, y in self.path], 4)
        QMessageBox.information(self, "Curve fitting",
            "Accuracy:\nx: {:.02f}%\ny: {:.02f}%".format(x_accuracy, y_accuracy),
            QMessageBox.Ok,
            QMessageBox.Ok
        )
        m = self.match_num.value()
        self.r_path = [(x_func(i/m*l), y_func(i/m*l)) for i in range(m)]
        self.accept()
