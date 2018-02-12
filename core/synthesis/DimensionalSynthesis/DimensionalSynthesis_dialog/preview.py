# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
##Copyright (C) 2016-2018 Yuan Chang
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
from core.graphics import (
    BaseCanvas,
    colorQt,
    colorPath
)
from core.io import get_from_parenthesis
from math import isnan
from typing import Tuple
from .Ui_preview import Ui_Dialog
inf = float('inf')

class DynamicCanvas(BaseCanvas):
    def __init__(self, mechanism, Path, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.mechanism = mechanism
        self.Path.path = Path
        self.solvingPath = self.mechanism['Target']
        self.index = 0
        #exp_symbol = ('A', 'B', 'C', 'D', 'E')
        self.exp_symbol = []
        self.links = []
        for exp in self.mechanism['Link_Expression'].split(';'):
            tags = get_from_parenthesis(exp, '[', ']').split(',')
            self.links.append(tuple(tags))
            for name in tags:
                if name not in self.exp_symbol:
                    self.exp_symbol.append(name)
        self.exp_symbol = sorted(self.exp_symbol)
        #Timer start.
        timer = QTimer(self)
        timer.setInterval(10)
        timer.timeout.connect(self.change_index)
        timer.start()
    
    def setInLimit(self):
        x_right = inf
        x_left = -inf
        y_top = -inf
        y_bottom = inf
        #Points
        for name in self.exp_symbol:
            x, y = self.mechanism[name]
            if x < x_right:
                x_right = x
            if x > x_left:
                x_left = x
            if y < y_bottom:
                y_bottom = y
            if y > y_top:
                y_top = y
        #Paths
        for i, path in enumerate(self.Path.path):
            if self.Path.show!=-1 and self.Path.show!=i:
                continue
            for x, y in path:
                if x < x_right:
                    x_right = x
                if x > x_left:
                    x_left = x
                if y < y_bottom:
                    y_bottom = y
                if y > y_top:
                    y_top = y
        #Solving paths
        for path in self.solvingPath.values():
            for x, y in path:
                if x < x_right:
                    x_right = x
                if x > x_left:
                    x_left = x
                if y < y_bottom:
                    y_bottom = y
                if y > y_top:
                    y_top = y
        return x_right, x_left, y_top, y_bottom
    
    def paintEvent(self, event):
        width = self.width()
        height = self.height()
        x_right, x_left, y_top, y_bottom = self.setInLimit()
        x_diff = x_right - x_left
        y_diff = y_top - y_bottom
        x_diff = x_diff if x_diff!=0 else 1
        y_diff = y_diff if y_diff!=0 else 1
        diff = x_diff/y_diff > width/height
        self.zoom = (width if diff else height)/(x_diff if diff else y_diff)*0.95
        self.ox = width/2 - (x_left + x_right)/2*self.zoom
        self.oy = height/2 + (y_bottom + y_top)/2*self.zoom
        super(DynamicCanvas, self).paintEvent(event)
        #Points that in the current angle section.
        self.Point = []
        for i, name in enumerate(self.exp_symbol):
            if (name in self.mechanism['Driver']) or (name in self.mechanism['Follower']):
                self.Point.append(self.mechanism[name])
            else:
                x, y = self.Path.path[i][self.index]
                if isnan(x):
                    self.index += 1
                    return
                else:
                    self.Point.append((x, y))
        #Draw links.
        for i, exp in enumerate(self.links):
            if i==0:
                continue
            name = "link_{}".format(i)
            self.drawLink(name, tuple(self.exp_symbol.index(tag) for tag in exp))
        #Draw path.
        self.drawPath()
        #Draw points.
        for i, name in enumerate(self.exp_symbol):
            coordinate = self.Point[i]
            if coordinate:
                color = colorQt('Green')
                fixed = False
                if name in self.mechanism['Target']:
                    color = colorQt('Dark-Orange')
                elif name in self.mechanism['Driver']:
                    color = colorQt('Red')
                    fixed = True
                elif name in self.mechanism['Follower']:
                    color = colorQt('Blue')
                    fixed = True
                self.drawPoint(i, coordinate[0], coordinate[1], fixed, color)
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
        brush.setAlphaF(0.70)
        self.painter.setBrush(brush)
        qpoints = tuple(
            QPointF(self.Point[i][0]*self.zoom, self.Point[i][1]*-self.zoom)
            for i in points if self.Point[i] and not isnan(self.Point[i][0])
        )
        if len(qpoints)==len(points):
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.showPointMark and name!='ground' and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.fontSize))
            text = "[{}]".format(name)
            cenX = sum(self.Point[i][0] for i in points if self.Point[i])/len(points)
            cenY = sum(self.Point[i][1] for i in points if self.Point[i])/len(points)
            self.painter.drawText(QPointF(cenX*self.zoom, cenY*-self.zoom), text)
    
    def drawPath(self):
        pen = QPen()
        #Draw the path of mechanism.
        def drawPath(path):
            pointPath = QPainterPath()
            for i, coordinate in enumerate(path):
                if coordinate:
                    x = coordinate[0]*self.zoom
                    y = coordinate[1]*-self.zoom
                    if isnan(x):
                        continue
                    if i==0:
                        pointPath.moveTo(x, y)
                    else:
                        pointPath.lineTo(QPointF(x, y))
            self.painter.drawPath(pointPath)
        def drawDot(path):
            for coordinate in path:
                if isnan(coordinate[0]):
                    continue
                self.painter.drawPoint(QPointF(coordinate[0]*self.zoom, coordinate[1]*-self.zoom))
        draw = drawPath if self.Path.curve else drawDot
        Path = self.Path.path
        for i, path in enumerate(Path):
            color = colorQt('Green')
            if self.exp_symbol[i] in self.mechanism['Target']:
                color = colorQt('Dark-Orange')
            pen.setColor(color)
            pen.setWidth(self.pathWidth)
            self.painter.setPen(pen)
            draw(path)
        #Draw the path that specified by user.
        pen.setWidth(self.pathWidth)
        for i, name in enumerate(sorted(self.solvingPath)):
            path = self.solvingPath[name]
            Pen, Dot, Brush = colorPath(i)
            self.painter.setBrush(Brush)
            pointPath = QPainterPath()
            for i, (x, y) in enumerate(path):
                x *= self.zoom
                y *= -self.zoom
                pen.setColor(Dot)
                self.painter.setPen(pen)
                self.painter.drawEllipse(QPointF(x, y), 3, 3)
                if i==0:
                    self.painter.drawText(QPointF(x+6, y-6), name)
                    pointPath.moveTo(x, y)
                else:
                    x2, y2 = path[i-1]
                    pen.setColor(Pen)
                    self.painter.setPen(pen)
                    self.drawArrow(x, y, x2*self.zoom, y2*-self.zoom)
                    pointPath.lineTo(QPointF(x, y))
            pen.setColor(Pen)
            self.painter.setPen(pen)
            self.painter.drawPath(pointPath)
        self.painter.setBrush(Qt.NoBrush)
    
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
        self.setWindowTitle("Preview: {} (max {} generations)".format(
            self.mechanism['Algorithm'], self.mechanism['lastGen']
        ))
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.main_splitter.setSizes([800, 100])
        self.splitter.setSizes([100, 100, 100])
        previewWidget = DynamicCanvas(self.mechanism, Path, self)
        self.left_layout.insertWidget(0, previewWidget)
        #Basic information
        link_tags = []
        for expr in self.mechanism['Expression'].split(';'):
            for p in get_from_parenthesis(expr, '[', ']').split(','):
                if ('L' in p) and (p not in link_tags):
                    link_tags.append(p)
        self.basic_label.setText("\n".join(
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in ['Algorithm', 'time']] +
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in self.mechanism['Driver']] +
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in self.mechanism['Follower']] +
            ["{}: {}".format(tag, self.mechanism[tag]) for tag in sorted(link_tags)]
        ))
        #Algorithm information
        interrupt = self.mechanism['interrupted']
        fitness = self.mechanism['TimeAndFitness'][-1]
        self.algorithm_label.setText("<html><head/><body><p>"+
            "<br/>".join(["Max generation: {}".format(self.mechanism['lastGen'])]+
            ["Fitness: {}".format(fitness if type(fitness)==float else fitness[1])]+
            ["<img src=\"{}\" width=\"15\"/>".format(":/icons/task-completed.png" if interrupt=='False' else
            ":/icons/question-mark.png" if interrupt=='N/A' else ":/icons/interrupted.png")+
            "Interrupted at: {}".format(interrupt)]+
            ["{}: {}".format(k, v) for k, v in self.mechanism['settings'].items()])+
            "</p></body></html>")
        #Hardware information
        self.hardware_label.setText("\n".join(["{}: {}".format(tag, self.mechanism['hardwareInfo'][tag]) for tag in
            ['os', 'memory', 'cpu', 'network']]))
