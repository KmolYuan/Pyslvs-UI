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
from ..graphics.color import colorName, colorIcons
from .Ui_edit_point import Ui_Dialog as edit_point_Dialog

class edit_point_show(QDialog, edit_point_Dialog):
    def __init__(self, mask, Points, pos=False, parent=None):
        super(edit_point_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        icon = QIcon(QPixmap(":/icons/point.png"))
        self.Points = Points
        for i, e in enumerate(colorName()):
            self.Color.insertItem(i, colorIcons()[e], e)
        if pos is False:
            self.Point.addItem(icon, 'Point{}'.format(len(Points)))
            self.Point.setEnabled(False)
            self.Color.setCurrentIndex(self.Color.findText('Green'))
        else:
            for i in range(1, len(Points)):
                self.Point.insertItem(i, icon, 'Point{}'.format(i))
            self.Point.setCurrentIndex(pos-1)
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index):
        if len(self.Points)-1>index:
            self.X_coordinate.setText(str(self.Points[index+1].x))
            self.X_coordinate.setPlaceholderText(str(self.Points[index+1].x))
            self.Y_coordinate.setText(str(self.Points[index+1].y))
            self.Y_coordinate.setPlaceholderText(str(self.Points[index+1].y))
            self.Fix_Point.setCheckState(Qt.Checked if self.Points[index+1].fix else Qt.Unchecked)
            self.Color.setCurrentIndex(self.Color.findText(self.Points[index+1].color))
