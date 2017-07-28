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
from .Ui_Drive_rod import Ui_Form

class Drive_rod_show(QWidget, Ui_Form):
    positionChange = pyqtSignal(float, int)
    def __init__(self, table, tablePoint, parent=None):
        super(Drive_rod_show, self).__init__(parent)
        self.setupUi(self)
        self.table = table
        self.tablePoint = tablePoint
        for i in range(len(table)):
            self.Rod.insertItem(i, QIcon(QPixmap(":/icons/spring.png")), 'Rod{}'.format(i))
        self.on_Rod_currentIndexChanged(0)
    
    @pyqtSlot(int)
    def on_Rod_currentIndexChanged(self, index):
        start = self.table[index].start
        end = self.table[index].end
        distance = int(((self.tablePoint[start].cx-self.tablePoint[end].cx)**2+(self.tablePoint[start].cy-self.tablePoint[end].cy)**2)**(1/2)*100)
        self.Position.setMaximum(distance)
        self.Position.setValue(int(self.table[index].pos*100))
        self.Distance_text.setValue(distance/100)
        self.Center.setText(str(self.table[index].cen))
        self.Start.setText(str(start))
    
    @pyqtSlot()
    def on_ResetButton_clicked(self):
        index = self.Rod.currentIndex()
        start = self.table[index].start
        end = self.table[index].end
        distance = int(((self.tablePoint[start].cx-self.tablePoint[end].cx)**2+(self.tablePoint[start].cy-self.tablePoint[end].cy)**2)**(1/2)*100)
        self.Position.setMaximum(distance)
        self.Position.setValue(int(self.table[index].pos*100))
        self.Distance_text.setValue(distance/100)
    
    @pyqtSlot(float)
    def on_Distance_text_valueChanged(self, p0):
        self.Position.setMaximum(int(p0*100))
    @pyqtSlot(int)
    def on_Position_valueChanged(self, value):
        self.Distance.setText(str(value/100))
    
    def __del__(self):
        self.positionChange.emit(self.Distance_text.value(), self.Rod.currentIndex())
