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
from .Ui_Algorithm_preview import Ui_Dialog
from .canvas import BaseCanvas
from .color import colorQt
from typing import Tuple

class DynamicCanvas(BaseCanvas):
    Exp_4 = 'A,L0,a0,D,B,B,L1,L2,D,C,B,L3,L4,C,E'
    Exp_8 = 'A,L0,a0,B,C,B,L2,L1,C,D,B,L4,L3,D,E,C,L5,L6,B,F,F,L8,L7,E,G,F,L9,L10,G,H'
    
    def __init__(self, mechanism, Path, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.mechanism = mechanism
        self.Path.path = Path
        self.index = 0
        expression = (self.Exp_8 if self.mechanism['type']=='8Bar' else self.Exp_4).split(',')
        self.expression_tag = tuple(tuple(expression[i+j] for j in range(5)) for i in range(0, len(expression), 5))
        #(('A', 'L0', 'a0', 'D', 'B'), ('B', 'L1', 'L2', 'D', 'C'), ('B', 'L3', 'L4', 'C', 'E'))
        self.exp_symbol = (self.expression_tag[0][0], self.expression_tag[0][3])+tuple(exp[-1] for exp in self.expression_tag)
        #('A', 'D', 'B', 'C', 'E')
        #Timer start.
        timer = QTimer(self)
        timer.setInterval(10)
        timer.timeout.connect(self.change_index)
        timer.start()
    
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        Comparator = lambda fun, i: fun(fun(path[i] for path in point if path) for point in self.Path.path if point)
        maxX = max(Comparator(max, 0), self.mechanism['Ax'], self.mechanism['Dx'])
        minX = min(Comparator(min, 0), self.mechanism['Ax'], self.mechanism['Dx'])
        maxY = max(Comparator(max, 1), self.mechanism['Ay'], self.mechanism['Dy'])
        minY = min(Comparator(min, 1), self.mechanism['Ay'], self.mechanism['Dy'])
        diffX = maxX - minX
        diffY = maxY - minY
        diff = diffX/diffY > width/height
        self.zoom = (width if diff else height)/(diffX if diff else diffY)*0.95
        self.ox = width/2 - (minX + maxX)/2*self.zoom
        self.oy = height/2 + (minY + maxY)/2*self.zoom
        super(DynamicCanvas, self).paintEvent(event)
        #Points that in the current angle section.
        self.Point = (
            (self.mechanism['Ax'], self.mechanism['Ay']),
            (self.mechanism['Dx'], self.mechanism['Dy'])
        ) + tuple((c[self.index][0], c[self.index][1]) if c[self.index] else False for c in self.Path.path[2:])
        if False in self.Point:
            self.index += 1
            return
        #Draw links.
        for i, exp in enumerate(self.expression_tag):
            name = 'link_{}'.format(i)
            if i==0:
                self.drawLink(name, tuple(self.exp_symbol.index(exp[n]) for n in (0, 4)))
            elif i%3==0:
                self.drawLink(name, tuple(self.exp_symbol.index(exp[n]) for n in (0, 4)))
                self.drawLink(name, tuple(self.exp_symbol.index(exp[n]) for n in (3, 4)))
            elif i%3==1:
                self.drawLink(name, tuple(self.exp_symbol.index(exp[n]) for n in (3, 4)))
            else:
                self.drawLink(name, tuple(self.exp_symbol.index(exp[n]) for n in (0, 3, 4)))
        #Draw path.
        self.drawPath()
        #Draw points.
        for i, name in enumerate(self.exp_symbol):
            coordinate = self.Point[i]
            if coordinate:
                self.drawPoint(i, coordinate[0], coordinate[1], i<2, colorQt('Blue') if i<2 else colorQt('Green'))
        self.painter.end()
    
    def drawLink(self,
        name: str,
        points: Tuple[int]
    ):
        color = colorQt('Blue')
        pen = QPen(color)
        pen.setWidth(self.linkWidth)
        self.painter.setPen(pen)
        brush = QColor(226, 219, 190)
        brush.setAlphaF(0.75)
        self.painter.setBrush(brush)
        qpoints = tuple(
            QPointF(self.Point[i][0]*self.zoom, self.Point[i][1]*-self.zoom)
            for i in points if self.Point[i]
        )
        if qpoints:
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.showPointMark and name!='ground' and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.fontSize))
            text = '[{}]'.format(name)
            cenX = sum(self.Point[i][0] for i in points if self.Point[i])/len(points)
            cenY = sum(self.Point[i][1] for i in points if self.Point[i])/len(points)
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
                    self.painter.drawPoint(QPointF(coordinate[0]*self.zoom, coordinate[1]*-self.zoom))
        draw = drawPath if self.Path.mode else drawDot
        Path = self.Path.path
        for i, path in enumerate(Path):
            pen = QPen(colorQt('Green'))
            pen.setWidth(self.pathWidth)
            self.painter.setPen(pen)
            draw(path)
    
    @pyqtSlot()
    def change_index(self):
        self.index += 1
        self.index %= 360
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
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in sorted(k for k in self.mechanism if 'L' in k)]))
        #Algorithm information
        interrupt = self.mechanism['interrupted']
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
