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
from time import sleep

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
    def __init__(self, mechanism, Paths, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.mechanism = mechanism
        self.Paths = Paths
        self.zoom = 5
        self.index = 0
    
    def paintEvent(self, event):
        super(DynamicCanvas, self).paintEvent(event)
        width = self.width()
        height = self.height()
        pen = QPen()
        try:
            pathMaxX = max([max(dot[0] for dot in path) for path in self.Paths.values()])
            pathMinX = min([min(dot[0] for dot in path) for path in self.Paths.values()])
            pathMaxY = max([max(dot[1] for dot in path) for path in self.Paths.values()])
            pathMinY = min([min(dot[1] for dot in path) for path in self.Paths.values()])
            diffX = max(max(self.mechanism['Ax'], self.mechanism['Dx']), pathMaxX)-min(min(self.mechanism['Ax'], self.mechanism['Dx']), pathMinX)
            diffY = max(max(self.mechanism['Ay'], self.mechanism['Dy']), pathMaxY)-min(min(self.mechanism['Ay'], self.mechanism['Dy']), pathMinY)
            cdiff = diffX/diffY > width/height
            self.zoom = (width if cdiff else height)/(diffX if cdiff else diffY)*0.47
            Tp = self.zoom*self.options.rate
            cenx = (min(min(self.mechanism['Ax'], self.mechanism['Dx']), pathMinX)+max(max(self.mechanism['Ax'], self.mechanism['Dx']), pathMaxX))/2
            ceny = (min(min(self.mechanism['Ay'], self.mechanism['Dy']), pathMinY)+max(max(self.mechanism['Ay'], self.mechanism['Dy']), pathMaxY))/2
            origin_x = width/2-cenx*Tp
            origin_y = height/2+ceny*Tp
            self.painter.translate(origin_x, origin_y)
            expression = self.mechanism['mechanismParams']['Expression'].split(',')
            expression_tag = tuple(tuple(expression[i+j] for j in range(5)) for i in range(0, len(expression), 5))
            shaft_r = self.Paths[expression_tag[0][-1]][self.index]
            self.drawShaft(0, self.mechanism['Ax']*Tp, self.mechanism['Ay']*Tp*-1, shaft_r[0]*Tp, shaft_r[1]*Tp*-1)
            for i, exp in enumerate(expression_tag[1:]):
                p_l = list()
                for i, k in enumerate([0, 3, -1]):
                    if exp[k] in self.Paths:
                        p_l.append(QPointF(self.Paths[exp[k]][self.index][0]*Tp, self.Paths[exp[k]][self.index][1]*Tp*-1))
                    else:
                        if exp[k]=='A':
                            p_l.append(QPointF(self.mechanism['Ax']*Tp, self.mechanism['Ay']*Tp*-1))
                        else:
                            p_l.append(QPointF(self.mechanism['Dx']*Tp, self.mechanism['Dy']*Tp*-1))
                self.drawLink(0, p_l[2].x(), p_l[2].y(), p_l[0].x(), p_l[0].y(), str())
                self.drawLink(0, p_l[2].x(), p_l[2].y(), p_l[1].x(), p_l[1].y(), str())
            for i, tag in enumerate(sorted(list(self.Paths.keys()))):
                pen.setWidth(self.linkWidth)
                pen.setColor(self.Color['Green'] if i<len(self.Paths)-1 else self.Color['Brick-Red'])
                self.painter.setPen(pen)
                pointPath = QPainterPath()
                for j, coordinate in enumerate(self.Paths[tag]):
                    point = QPointF(coordinate[0]*Tp, coordinate[1]*Tp*-1)
                    if j==0:
                        pointPath.moveTo(point)
                    else:
                        pointPath.lineTo(point)
                self.painter.drawPath(pointPath)
            for tag in ['A', 'D']:
                x = self.mechanism[tag+'x']*Tp
                y = self.mechanism[tag+'y']*Tp*-1
                self.drawPoint(0, x, y, True, self.Color['Blue'])
            for i, tag in enumerate(sorted(list(self.Paths.keys()))):
                x = self.Paths[tag][self.index][0]*Tp
                y = self.Paths[tag][self.index][1]*Tp*-1
                self.drawPoint(0, x, y, False, self.Color['Green'] if i<len(self.Paths)-1 else self.Color['Brick-Red'])
            pathData = self.mechanism['mechanismParams']['targetPath']
            pen.setWidth(self.pathWidth+3)
            pen.setColor(QColor(69, 247, 232))
            self.painter.setPen(pen)
            pointPath = QPainterPath()
            for i, coordinate in enumerate(pathData):
                point = QPointF(coordinate[0]*Tp, coordinate[1]*Tp*-1)
                if i==0:
                    pointPath.moveTo(point)
                else:
                    pointPath.lineTo(point)
            self.painter.drawPath(pointPath)
        except Exception as e:
            self.painter.translate(width/2, height/2)
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', 20))
            self.painter.drawText(QPoint(0, 0), "Error occurred!\nPlease check dimension data.")
        self.painter.end()
    
    @pyqtSlot(int)
    def change_index(self, i):
        self.index = i
        self.update()

class PreviewDialog(QDialog, Ui_Dialog):
    def __init__(self, mechanism, Paths, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Preview: {} (max {} generations)".format(mechanism['Algorithm'], mechanism['generateData']['maxGen']))
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.splitter.setSizes([800, 100])
        previewWidget = DynamicCanvas(mechanism, Paths, self)
        self.left_layout.insertWidget(0, previewWidget)
        #Basic information
        self.basic_label.setText("\n".join(["{}: {}".format(tag, mechanism[tag]) for tag in ['Algorithm', 'time']]+
            ["{}: ({}, {})".format(tag, mechanism[tag+'x'], mechanism[tag+'y']) for tag in ['A', 'D']]+
            ["{}: {}".format(tag, mechanism[tag]) for tag in mechanism['mechanismParams']['Link'].split(',')]))
        #Algorithm information
        interrupt = mechanism['interruptedGeneration']
        fitness = mechanism['TimeAndFitness'][-1]
        self.algorithm_label.setText("<html><head/><body><p>"+
            "<br/>".join(["Max generation: {}".format(mechanism['generateData']['maxGen'])]+
            ["Fitness: {}".format(fitness if type(fitness)==float else fitness[1])]+
            ["<img src=\"{}\" width=\"15\"/>".format(":/icons/task-completed.png" if interrupt=='False' else
            ":/icons/question-mark.png" if interrupt=='N/A' else ":/icons/interrupted.png")+
            "Interrupted at: {}".format(interrupt)]+
            ["{}: {}".format(k, v) for k, v in mechanism['algorithmPrams'].items()])+
            "</p></body></html>")
        #Hardware information
        self.hardware_label.setText("\n".join(["{}: {}".format(tag, mechanism['hardwareInfo'][tag]) for tag in
            ['os', 'memory', 'cpu', 'network']]))
        #playShaft
        self.playShaft = playShaft(len(Paths[list(Paths.keys())[0]])-1)
        self.playShaft.progress_Signal.connect(previewWidget.change_index)
        self.playShaft.start()
