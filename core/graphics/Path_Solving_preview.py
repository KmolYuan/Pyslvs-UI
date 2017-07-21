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
from ..graphics.color import colorlist
from .canvas_0 import PointOptions

class DynamicCanvas(QWidget):
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.options = PointOptions(self.width(), self.height())
        self.Color = colorlist()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.options.style['Background']))
        origin_x = event.rect().width()/2
        origin_y = event.rect().height()/2
        painter.translate(origin_x, origin_y)

class PreviewDialog(QDialog):
    def __init__(self, name, row, startAngle, endAngle, answer, Paths, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self.setWindowTitle('Preview {}'.format(name))
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        previewWidget = DynamicCanvas(self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(previewWidget)
