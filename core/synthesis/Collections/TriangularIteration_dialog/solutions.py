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

from core.QtModules import *
from .Ui_solutions import Ui_Dialog

class SolutionsDialog(QDialog, Ui_Dialog):
    def __init__(self, mode, parent):
        super(SolutionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("{} solution".format(mode))
        if mode=='PLAP':
            self.main_label.setText(
                "Two known points A and B, "+
                "with angle β and length L0 to find out the coordinate of point C."
            )
        elif mode=='PLLP':
            self.main_label.setText(
                "Two known points A and B, "+
                "with length L0 and R0 to find out the coordinate of point C."
            )
            self.graph_label.setPixmap(QPixmap(":/icons/preview/PLLP.png"))
