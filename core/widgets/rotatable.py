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
from time import sleep

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

#Control QDial widget value.
class playShaft(QThread):
    rotate = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(playShaft, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.startAngle = 0
        self.minima = 0
        self.maxima = 36000
        self.speed = 300
        self.reversed = False
    
    def setStartAngle(self, startAngle: float):
        with QMutexLocker(self.mutex):
            self.startAngle = int(startAngle)
    
    def setReversed(self, reversed: bool):
        with QMutexLocker(self.mutex):
            self.reversed = reversed
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        FirstLoop = range(self.startAngle if self.startAngle>self.minima else self.minima, self.maxima, self.speed)
        rFirstLoop = range(self.startAngle if self.startAngle<self.maxima else self.maxima, self.minima, -self.speed)
        #FirstLoop
        for i in (rFirstLoop if self.reversed else FirstLoop):
            if self.stoped:
                return
            sleep(.05)
            self.rotate.emit(i)
        while True:
            Loop = range(self.minima, self.maxima, self.speed)
            if (self.minima != self.minima) and (self.maxima != self.maxima):
                for i in (reversed(Loop) if self.reversed else Loop):
                    if self.stoped:
                        return
                    sleep(.05)
                    self.rotate.emit(self.maxima-i)
            for i in (reversed(Loop) if self.reversed else Loop):
                if self.stoped:
                    return
                sleep(.05)
                self.rotate.emit(i)
    
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True
