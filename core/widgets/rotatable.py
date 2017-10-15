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

#Rotate QDial widget.
class RotatableView(QGraphicsView):
    def __init__(self, item):
        QGraphicsView.__init__(self)
        scene = QGraphicsScene(self)
        self.setScene(scene)
        item.setMinimumSize(QSize(150, 150))
        item.setMaximum(36000)
        item.setSingleStep(100)
        item.setPageStep(100)
        item.setInvertedAppearance(True)
        item.setWrapping(True)
        item.setNotchTarget(.1)
        item.setNotchesVisible(True)
        graphics_item = scene.addWidget(item)
        graphics_item.setRotation(-90)
        # make the QGraphicsView invisible.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(item.height())
        self.setFixedWidth(item.width())
        self.setStyleSheet("border: 0px;")
