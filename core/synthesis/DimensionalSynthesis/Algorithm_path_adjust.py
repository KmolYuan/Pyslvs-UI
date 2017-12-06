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
from .Ui_Algorithm_path_adjust import Ui_Dialog

class Algorithm_path_adjust_show(QDialog, Ui_Dialog):
    def __init__(self, path, parent=None):
        super(Algorithm_path_adjust_show, self).__init__(parent)
        self.setupUi(self)
        for e in path:
            self.Point_list.addItem("({}, {})".format(e[0], e[1]))
        self.points_num.setText(str(len(path)))
        self.blurring_num.setMaximum(len(path))
        self.blurring_num.setValue(self.blurring_num.maximum())
        self.path = path
        self.r_path = []
    
    def get_path(self):
        return self.r_path
    
    @pyqtSlot()
    def on_scalingButton_clicked(self):
        self.r_path = [
            (self.scaling_rx.value()+(e['x']-self.scaling_rx.value())*self.scaling_h.value(),
            self.scaling_ry.value()+(e['y']-self.scaling_ry.value())*self.scaling_v.value()) for e in self.path]
        self.accept()
    
    @pyqtSlot()
    def on_movingButton_clicked(self):
        self.r_path = [(e['x']+self.moving_x_coordinate.value(), e['y']+self.moving_y_coordinate.value()) for e in self.path]
        self.accept()
    
    @pyqtSlot()
    def on_blurringButton_clicked(self):
        try:
            target_num = round(len(self.path)/self.blurring_num.value())
        except ZeroDivisionError:
            target_num = len(self.path)
        self.r_path = [(e[0], e[1]) for i, e in enumerate(self.path) if i%target_num==0]
        f_p = (self.path[0][0], self.path[0][1])
        e_p = (self.path[-1][0], self.path[-1][1])
        if self.r_path[0]!=f_p:
            self.r_path.insert(0, f_p)
        if self.r_path[-1]!=e_p:
            self.r_path.append(e_p)
        self.accept()
