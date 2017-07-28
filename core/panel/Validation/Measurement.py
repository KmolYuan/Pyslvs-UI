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
from .Ui_Measurement import Ui_Form as Measurement_Form

class Measurement_show(QWidget, Measurement_Form):
    point_change = pyqtSignal(int, int)
    def __init__(self, table, parent=None):
        super(Measurement_show, self).__init__(parent)
        self.setupUi(self)
        self.Distance.setPlainText("0.0")
        self.First_Detection = True
        for i in range(table.rowCount()):
            self.Start.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
            self.End.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
    
    @pyqtSlot(float, float)
    def show_mouse_track(self, x, y):
        self.Mouse.setPlainText("({}, {})".format(x, y))
    
    @pyqtSlot(int)
    def on_Start_currentIndexChanged(self, index):
        self.First_Detection = True
        self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
    @pyqtSlot(int)
    def on_End_currentIndexChanged(self, index):
        self.First_Detection = True
        self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
    @pyqtSlot(float)
    def change_distance(self, val):
        self.Distance.setPlainText(str(val))
    
    @pyqtSlot()
    def Detection_do(self):
        if self.First_Detection:
            self.First_Detection = False
            self.Max_val.setPlainText(self.Distance.toPlainText())
            self.Min_val.setPlainText(self.Distance.toPlainText())
        else:
            if float(self.Max_val.toPlainText())<float(self.Distance.toPlainText()):
                self.Max_val.setPlainText(self.Distance.toPlainText())
            if float(self.Min_val.toPlainText())>float(self.Distance.toPlainText()):
                self.Min_val.setPlainText(self.Distance.toPlainText())
        self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
