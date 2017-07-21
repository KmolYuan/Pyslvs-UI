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
    def __init__(self, mechanism, Paths, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.options = PointOptions(self.width(), self.height())
        self.Color = colorlist()
        self.mechanism = mechanism
        self.Paths = Paths
        self.zoom = 5
    
    def paintEvent(self, event):
        if not False in self.Paths[list(self.Paths.keys())[0]]:
            painter = QPainter()
            painter.begin(self)
            painter.fillRect(event.rect(), QBrush(self.options.style['Background']))
            width = self.width()
            height = self.height()
            pen = QPen()
            pathMaxX = max([max(dot[0] for dot in path) for path in self.Paths.values()])
            pathMinX = min([min(dot[0] for dot in path) for path in self.Paths.values()])
            pathMaxY = max([max(dot[1] for dot in path) for path in self.Paths.values()])
            pathMinY = min([min(dot[1] for dot in path) for path in self.Paths.values()])
            diffX = max(max(self.mechanism['Ax'], self.mechanism['Dx']), pathMaxX)-min(min(self.mechanism['Ax'], self.mechanism['Dx']), pathMinX)
            diffY = max(max(self.mechanism['Ay'], self.mechanism['Dy']), pathMaxY)-min(min(self.mechanism['Ay'], self.mechanism['Dy']), pathMinY)
            cdiff = diffX/diffY > width/height
            self.zoom = int((width if cdiff else height)/((diffX if cdiff else diffY))*0.5)
            Tp = self.zoom*self.options.rate
            cenx = (min(min(self.mechanism['Ax'], self.mechanism['Dx']), pathMinX)+max(max(self.mechanism['Ax'], self.mechanism['Dx']), pathMaxX))/2
            ceny = (min(min(self.mechanism['Ay'], self.mechanism['Dy']), pathMinY)+max(max(self.mechanism['Ay'], self.mechanism['Dy']), pathMaxY))/2
            origin_x = width/2-cenx*Tp
            origin_y = height/2+ceny*Tp
            painter.translate(origin_x, origin_y)
            expression = self.mechanism['mechanismParams']['Expression'].split(',')
            expression_tag = tuple(tuple(expression[i+j] for j in range(5)) for i in range(0, len(expression), 5))
            pen.setWidth(self.options.style['penWidth']['pen']+2)
            pen.setColor(QColor(225, 140, 0))
            painter.setPen(pen)
            shaft_r = self.Paths[expression_tag[0][-1]][0]
            painter.drawLine(QPointF(self.mechanism['Ax']*Tp, self.mechanism['Ay']*Tp*-1), QPointF(shaft_r[0]*Tp, shaft_r[1]*Tp*-1))
            for i, exp in enumerate(expression_tag[1:]):
                if exp[0] in self.Paths:
                    p1x = self.Paths[exp[0]][0][0]*Tp
                    p1y = self.Paths[exp[0]][0][1]*Tp*-1
                else:
                    p1x = self.mechanism[exp[0]+'x']*Tp
                    p1y = self.mechanism[exp[0]+'y']*Tp*-1
                if exp[3] in self.Paths:
                    p2x = self.Paths[exp[3]][0][0]*Tp
                    p2y = self.Paths[exp[3]][0][1]*Tp*-1
                else:
                    p2x = self.mechanism[exp[3]+'x']*Tp
                    p2y = self.mechanism[exp[3]+'y']*Tp*-1
                if exp[-1] in self.Paths:
                    p3x = self.Paths[exp[-1]][0][0]*Tp
                    p3y = self.Paths[exp[-1]][0][1]*Tp*-1
                else:
                    p3x = self.mechanism[exp[-1]+'x']*Tp
                    p3y = self.mechanism[exp[-1]+'y']*Tp*-1
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(self.options.style['link'])
                painter.setPen(pen)
                painter.drawLine(QPointF(p1x, p1y), QPointF(p3x, p3y))
                painter.drawLine(QPointF(p2x, p2y), QPointF(p3x, p3y))
            for tag in ['A', 'D']:
                cx = self.mechanism[tag+'x']*Tp
                cy = self.mechanism[tag+'y']*Tp*-1
                pen.setWidth(2)
                pen.setColor(self.Color['Blue'])
                painter.setPen(pen)
                painter.drawEllipse(QPointF(cx, cy), 10., 10.)
                pen.setWidth(5)
                painter.setPen(pen)
                painter.drawPoint(QPointF(cx, cy))
            for i, tag in enumerate(set(self.Paths.keys())):
                pen.setWidth(self.options.style['penWidth']['path'])
                pen.setColor(self.Color['Green'] if i<len(self.Paths)-1 else self.Color['Brick-Red'])
                painter.setPen(pen)
                pointPath = QPainterPath()
                for j, coordinate in enumerate(self.Paths[tag]):
                    point = QPointF(coordinate[0]*Tp, coordinate[1]*Tp*-1)
                    if j==0: pointPath.moveTo(point)
                    else: pointPath.lineTo(point)
                painter.drawPath(pointPath)
            for i, tag in enumerate(set(self.Paths.keys())):
                cx = self.Paths[tag][0][0]*Tp
                cy = self.Paths[tag][0][1]*Tp*-1
                pen.setWidth(2)
                pen.setColor(self.Color['Green'] if i<len(self.Paths)-1 else self.Color['Brick-Red'])
                painter.setPen(pen)
                painter.drawEllipse(QPointF(cx, cy), 5., 5.)
                pen.setWidth(5)
                painter.setPen(pen)
                painter.drawPoint(QPointF(cx, cy))

class PreviewDialog(QDialog):
    def __init__(self, name, mechanism, Paths, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self.setWindowTitle('Preview {}'.format(name))
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        previewWidget = DynamicCanvas(mechanism, Paths, self)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(previewWidget)
