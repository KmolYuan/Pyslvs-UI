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

from ..QtModules import *
from .Ui_edit_rod import Ui_Dialog as edit_rod_Dialog

class edit_rod_show(QDialog, edit_rod_Dialog):
    def __init__(self, Point, Rods, pos=False, parent=None):
        super(edit_rod_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/spring.png"))
        self.Rods = Rods
        for i in range(len(Point)):
            name = 'Point{}'.format(i)
            self.Center.insertItem(i, icon, name)
            self.Start.insertItem(i, icon, name)
            self.End.insertItem(i, icon, name)
        if pos is False:
            self.Rod.addItem(iconSelf, 'Rod{}'.format(len(Rods)))
            self.Rod.setEnabled(False)
        else:
            for i in range(len(Rods)):
                self.Rod.insertItem(i, iconSelf, 'Rod{}'.format(i))
            self.Rod.setCurrentIndex(pos)
        for signal in [self.Center.currentIndexChanged, self.Start.currentIndexChanged, self.End.currentIndexChanged,
                self.Position.valueChanged, self.Position.editingFinished]:
            signal.connect(self.isOk)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Rod_currentIndexChanged(self, index):
        if len(self.Rods)>index:
            self.Center.setCurrentIndex(self.Rods[index].cen)
            self.Start.setCurrentIndex(self.Rods[index].start)
            self.End.setCurrentIndex(self.Rods[index].end)
            self.Position.setValue(self.Rods[index].pos)
    
    @pyqtSlot()
    @pyqtSlot(int)
    @pyqtSlot(float)
    def isOk(self):
        self.cen = self.Center.currentIndex()
        self.start = self.Start.currentIndex()
        self.end = self.End.currentIndex()
        self.pos = self.Position.text()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.cen!=self.start and self.start!=self.end and self.cen!=self.end)
