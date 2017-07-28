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
from .planeSolving import slvsProcess
from copy import copy
from ..io.elements import VPath, VPaths
import timeit

class WorkerThread(QThread):
    done = pyqtSignal(list)
    progress_Signal = pyqtSignal(int)
    def __init__(self, Point, Link, Chain, Shaft, Slider, Rod, warning, parent=None):
        super(WorkerThread, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.progress = 0
        self.Point = Point
        self.Link = Link
        self.Chain = Chain
        self.Shaft = Shaft
        self.Slider = Slider
        self.Rod = Rod
        self.warning = warning
    
    def set(self, ShaftList, Run_list, Resolution):
        self.ShaftList = ShaftList
        self.Run_list = Run_list
        self.Resolution = Resolution
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        print("Path Tracking...")
        t0 = timeit.default_timer()
        nPath = list()
        Point = [(copy(vpoint.cx), copy(vpoint.cy)) for vpoint in self.Point]
        for vpoint in self.Point:
            vpoint.move()
        for i in self.ShaftList:
            if self.stoped:
                for p, vpoint in enumerate(self.Point):
                    vpoint.move(Point[p][0], Point[p][1])
                return
            normal = self.Shaft[i].start<self.Shaft[i].end
            start_angle = (self.Shaft[i].start if normal else self.Shaft[i].start-360)*100
            end_angle = (self.Shaft[i].end if normal else self.Shaft[i].end-360)*100
            Resolution = self.Resolution*100
            paths = list()
            allPath = list()
            angleSE = sorted([int(start_angle), int(end_angle)])
            for j in range(angleSE[0], angleSE[1]+int(Resolution)*2, int(Resolution)):
                if self.stoped:
                    for p, vpoint in enumerate(self.Point):
                        vpoint.move(Point[p][0], Point[p][1])
                    return
                angle = float(j/100)
                result = slvsProcess(self.Point, self.Link, self.Chain, self.Shaft, self.Slider, self.Rod,
                    currentShaft=i, currentAngle=angle, hasWarning=self.warning)
                allPath.append(result)
                if not False in result:
                    for p, vpoint in enumerate(self.Point):
                        dot = result[p]
                        vpoint.move(dot['x'], dot['y'])
                self.progress_going()
            for n in self.Run_list:
                path = [(dot[n]['x'], dot[n]['y']) for dot in allPath]
                paths.append(VPath(n, path))
            nPath.append(VPaths(i, paths))
        for p, vpoint in enumerate(self.Point):
            vpoint.move(Point[p][0], Point[p][1])
        t1 = timeit.default_timer()
        time_spand = t1-t0
        print('total cost time: {:.4f} [s]'.format(time_spand))
        self.done.emit(nPath)
    
    def progress_going(self):
        self.progress += 1
        self.progress_Signal.emit(self.progress)
    
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True
