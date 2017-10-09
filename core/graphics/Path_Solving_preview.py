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
from .Ui_Path_Solving_preview import Ui_Dialog
from .canvas import BaseCanvas
from .color import colorQt
from time import sleep
from typing import List

class playShaft(QThread):
    progress_Signal = pyqtSignal(int)
    def __init__(self, limit, parent=None):
        super(playShaft, self).__init__(parent)
        self.limit = limit
        self.stoped = False
        self.mutex = QMutex()
    
    def run(self):
        with QMutexLocker(self.mutex):
            self.stoped = False
        i = 0
        while True:
            i += 1
            if self.stoped:
                return
            if i>=self.limit:
                i = 0
            sleep(.05)
            self.progress_Signal.emit(i)
    
    def stop(self):
        with QMutexLocker(self.mutex):
            self.stoped = True

class DynamicCanvas(BaseCanvas):
    def __init__(self, mechanism, Path, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.mechanism = mechanism
        self.Path.path = Path
        self.index = 0
        expression = self.mechanism['mechanismParams']['Expression'].split(',')
        self.expression_tag = tuple(tuple(expression[i+j] for j in range(5)) for i in range(0, len(expression), 5))
        #(('A', 'L0', 'a0', 'D', 'B'), ('B', 'L1', 'L2', 'D', 'C'), ('B', 'L3', 'L4', 'C', 'E'))
        self.exp_symbol = (self.expression_tag[0][0], self.expression_tag[0][3])+tuple(exp[-1] for exp in self.expression_tag)
        #('A', 'D', 'B', 'C', 'E')
    
    def paintEvent(self, event):
        super(DynamicCanvas, self).paintEvent(event)
        width = self.width()
        height = self.height()
        Comparator = lambda fun, i: fun(fun(path[i] for path in point if path) for point in self.Path.path if point)
        pathMaxX = Comparator(max, 0)
        pathMinX = Comparator(min, 0)
        pathMaxY = Comparator(max, 1)
        pathMinY = Comparator(min, 1)
        diffX = max(max(self.mechanism['Ax'], self.mechanism['Dx']), pathMaxX)-min(min(self.mechanism['Ax'], self.mechanism['Dx']), pathMinX)
        diffY = max(max(self.mechanism['Ay'], self.mechanism['Dy']), pathMaxY)-min(min(self.mechanism['Ay'], self.mechanism['Dy']), pathMinY)
        cdiff = diffX/diffY > width/height
        self.zoom = (width if cdiff else height)/(diffX if cdiff else diffY)*0.47*self.rate
        cenx = (min(min(self.mechanism['Ax'], self.mechanism['Dx']), pathMinX)+max(max(self.mechanism['Ax'], self.mechanism['Dx']), pathMaxX))/2
        ceny = (min(min(self.mechanism['Ay'], self.mechanism['Dy']), pathMinY)+max(max(self.mechanism['Ay'], self.mechanism['Dy']), pathMaxY))/2
        self.painter.translate(width/2-cenx*self.zoom, height/2+ceny*self.zoom)
        #Points
        self.Point = (
            (self.mechanism['Ax'], self.mechanism['Ay']),
            (self.mechanism['Dx'], self.mechanism['Dy'])
        ) + tuple((c[self.index][0], c[self.index][1]) if c else False for c in self.Path.path[2:])
        #Draw links.
        for i, exp in enumerate(self.expression_tag):
            if i%3==0:
                g = tuple(self.exp_symbol.index(exp[n]) for n in (0, -1))
            elif i%3==1:
                g = tuple(self.exp_symbol.index(exp[n]) for n in (3, -1))
            else:
                g = tuple(self.exp_symbol.index(exp[n]) for n in (0, 3, -1))
            self.drawLink('link_{}'.format(i), g)
        #Draw path.
        self.drawPath()
        #Draw points.
        for i, name in enumerate(self.exp_symbol):
            coordinate = self.Point[i]
            fixed = i<2
            self.drawPoint(i, coordinate[0], coordinate[1], fixed, colorQt('Blue') if fixed else colorQt('Green'))
        self.painter.end()
    
    def drawLink(self,
        name: str,
        points: List[int]
    ):
        #Draw link function.
        color = colorQt('Blue')
        pen = QPen(color)
        pen.setWidth(self.linkWidth)
        self.painter.setPen(pen)
        self.painter.setBrush(QColor(226, 219, 190))
        qpoints = tuple(
            QPointF(self.Point[i][0]*self.zoom, self.Point[i][1]*-self.zoom)
            for i in points
        )
        self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.showPointMark and name!='ground' and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.fontSize))
            text = '[{}]'.format(name)
            cenX = sum(self.Point[i][0] for i in points)/len(points)
            cenY = sum(self.Point[i][1] for i in points)/len(points)
            self.painter.drawText(QPointF(cenX*self.zoom, cenY*-self.zoom), text)
    
    def drawPath(self):
        def drawPath(path):
            pointPath = QPainterPath()
            for i, coordinate in enumerate(path):
                if coordinate:
                    x = coordinate[0]*self.zoom
                    y = coordinate[1]*-self.zoom
                    if i==0:
                        pointPath.moveTo(x, y)
                    else:
                        pointPath.lineTo(QPointF(x, y))
            self.painter.drawPath(pointPath)
        def drawDot(path):
            for coordinate in path:
                if coordinate:
                    x = coordinate[0]*self.zoom
                    y = coordinate[1]*-self.zoom
                    self.painter.drawPoint(QPointF(x, y))
        draw = drawPath if self.Path.mode else drawDot
        Path = self.Path.path
        for i, path in enumerate(Path):
            pen = QPen(colorQt('Green'))
            pen.setWidth(self.pathWidth)
            self.painter.setPen(pen)
            draw(path)
    
    @pyqtSlot(int)
    def change_index(self, i):
        self.index = i
        self.update()

class PreviewDialog(QDialog, Ui_Dialog):
    def __init__(self, mechanism, Path, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.mechanism = mechanism
        self.setWindowTitle("Preview: {} (max {} generations)".format(self.mechanism['Algorithm'], self.mechanism['generateData']['maxGen']))
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.splitter.setSizes([800, 100])
        previewWidget = DynamicCanvas(self.mechanism, Path, self)
        self.left_layout.insertWidget(0, previewWidget)
        #Basic information
        self.basic_label.setText("\n".join(["{}: {}".format(tag, self.mechanism[tag]) for tag in ['Algorithm', 'time']]+
            ["{}: ({}, {})".format(tag, self.mechanism[tag+'x'], self.mechanism[tag+'y']) for tag in ['A', 'D']]+
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in self.mechanism['mechanismParams']['Link'].split(',')]))
        #Algorithm information
        interrupt = self.mechanism['interruptedGeneration']
        fitness = self.mechanism['TimeAndFitness'][-1]
        self.algorithm_label.setText("<html><head/><body><p>"+
            "<br/>".join(["Max generation: {}".format(self.mechanism['generateData']['maxGen'])]+
            ["Fitness: {}".format(fitness if type(fitness)==float else fitness[1])]+
            ["<img src=\"{}\" width=\"15\"/>".format(":/icons/task-completed.png" if interrupt=='False' else
            ":/icons/question-mark.png" if interrupt=='N/A' else ":/icons/interrupted.png")+
            "Interrupted at: {}".format(interrupt)]+
            ["{}: {}".format(k, v) for k, v in self.mechanism['algorithmPrams'].items()])+
            "</p></body></html>")
        #Hardware information
        self.hardware_label.setText("\n".join(["{}: {}".format(tag, self.mechanism['hardwareInfo'][tag]) for tag in
            ['os', 'memory', 'cpu', 'network']]))
        #playShaft
        self.playShaft = playShaft(max(len(path) for path in Path)-1)
        self.playShaft.progress_Signal.connect(previewWidget.change_index)
        self.playShaft.start()
        self.rejected.connect(self.playShaft.stop)
