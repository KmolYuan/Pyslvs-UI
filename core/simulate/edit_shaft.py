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
from .Ui_edit_shaft import Ui_Dialog as edit_shaft_Dialog

class edit_shaft_show(QDialog, edit_shaft_Dialog):
    def __init__(self, Point, Shafts, pos=False, parent=None):
        super(edit_shaft_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/circle.png"))
        self.Shafts = Shafts
        for i, p in enumerate(Point):
            name = 'Point{}'.format(i)
            if p.fix:
                self.Center.insertItem(i, icon, name)
            else:
                self.References.insertItem(i, icon, name)
        if pos is False:
            self.Shaft.addItem(iconSelf, 'Shaft{}'.format(len(Shafts)))
            self.Shaft.setEnabled(False)
        else:
            for i in range(len(Shafts)):
                self.Shaft.insertItem(i, iconSelf, 'Shaft{}'.format(i))
            self.Shaft.setCurrentIndex(pos)
        for signal in [self.Start_Angle.valueChanged, self.End_Angle.valueChanged,
                self.Start_Angle.editingFinished, self.End_Angle.editingFinished,
                self.Center.currentIndexChanged, self.References.currentIndexChanged]:
            signal.connect(self.isOk)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index):
        if len(self.Shafts)>index:
            self.Center.setCurrentIndex(self.Center.findText('Point{}'.format(self.Shafts[index].cen)))
            self.References.setCurrentIndex(self.References.findText('Point{}'.format(self.Shafts[index].ref)))
            self.Start_Angle.setValue(self.Shafts[index].start)
            self.End_Angle.setValue(self.Shafts[index].end)
    
    @pyqtSlot()
    @pyqtSlot(int)
    @pyqtSlot(float)
    def isOk(self):
        try:
            self.center = int(self.Center.currentText().replace('Point', ''))
        except:
            self.center = None
        try:
            self.ref = int(self.References.currentText().replace('Point', ''))
        except:
            self.ref = None
        self.start = self.Start_Angle.text()
        self.end = self.End_Angle.text()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
            self.center!=None and self.ref!=None and self.center!=self.ref and self.Start_Angle.value()<self.End_Angle.value())
