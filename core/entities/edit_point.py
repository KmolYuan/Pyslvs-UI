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
    def __init__(self, Points, Links, pos=False, parent=None):
        super(edit_point_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        icon = self.windowIcon()
        self.LinkIcon = QIcon(QPixmap(":/icons/link.png"))
        self.Points = Points
        self.Links = Links
        for i, e in enumerate(colorName()):
            self.Color.insertItem(i, colorIcons(e), e)
        for vlink in Links:
            self.noSelected.addItem(QListWidgetItem(self.LinkIcon, vlink.name))
        if pos is False:
            self.Point.addItem(icon, 'Point{}'.format(len(Points)))
            self.Point.setEnabled(False)
            self.Color.setCurrentIndex(self.Color.findText('Green'))
        else:
            for i in range(len(Points)):
                self.Point.insertItem(i, icon, 'Point{}'.format(i))
            self.Point.setCurrentIndex(pos)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index):
        if len(self.Points)>index:
            vpoint = self.Points[index]
            self.X_coordinate.setValue(vpoint.x)
            self.Y_coordinate.setValue(vpoint.y)
            self.Color.setCurrentIndex(self.Color.findText(vpoint.colorSTR))
            self.Type.setCurrentIndex(vpoint.type)
            self.Angle.setValue(vpoint.angle)
            self.noSelected.clear()
            self.selected.clear()
            for linkName in vpoint.links:
                self.selected.addItem(QListWidgetItem(self.LinkIcon, linkName))
            for linkName in tuple(set([vlink.name for vlink in self.Links])-set(vpoint.links)):
                self.noSelected.addItem(QListWidgetItem(self.LinkIcon, linkName))
    
    @pyqtSlot(int)
    def on_Type_currentIndexChanged(self, index):
        self.Angle.setEnabled(index!=0)
    
    @pyqtSlot(QListWidgetItem)
    def on_noSelected_itemDoubleClicked(self, item):
        item = self.noSelected.takeItem(self.noSelected.row(item))
        self.selected.addItem(item)
    
    @pyqtSlot(QListWidgetItem)
    def on_selected_itemDoubleClicked(self, item):
        item = self.selected.takeItem(self.selected.row(item))
        self.noSelected.addItem(item)
