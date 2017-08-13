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
from .Ui_edit_slider import Ui_Dialog as edit_slider_Dialog

class edit_slider_show(QDialog, edit_slider_Dialog):
    def __init__(self, Point, Sliders, pos=False, parent=None):
        super(edit_slider_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/pointonx.png"))
        self.Sliders = Sliders
        for i in range(len(Point)):
            name = 'Point{}'.format(i)
            self.Slider_Center.insertItem(i, icon, name)
            self.Start.insertItem(i, icon, name)
            self.End.insertItem(i, icon, name)
        if pos is False:
            self.Slider.addItem(iconSelf, 'Slider{}'.format(len(Sliders)))
            self.Slider.setEnabled(False)
        else:
            for i in range(len(Sliders)):
                self.Slider.insertItem(i, iconSelf, 'Slider{}'.format(i))
            self.Slider.setCurrentIndex(pos)
        for signal in [self.Slider_Center.currentIndexChanged, self.Start.currentIndexChanged, self.End.currentIndexChanged]:
            signal.connect(self.isOk)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Slider_currentIndexChanged(self, index):
        if len(self.Sliders)>index:
            self.Slider_Center.setCurrentIndex(self.Sliders[index].cen)
            self.Start.setCurrentIndex(self.Sliders[index].start)
            self.End.setCurrentIndex(self.Sliders[index].end)
    
    @pyqtSlot(int)
    def isOk(self):
        self.slider = self.Slider_Center.currentIndex()
        self.start = self.Start.currentIndex()
        self.end = self.End.currentIndex()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.slider!=self.start and self.start!=self.end and self.slider!=self.end)
