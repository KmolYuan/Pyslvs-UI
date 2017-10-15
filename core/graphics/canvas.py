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
from math import sqrt
from typing import List
from heapq import nsmallest
from .color import colorQt

class Path:
    __slots__ = ('path', 'show', 'mode')
    
    def __init__(self):
        self.path = ()
        self.show = True
        #Display mode: The path will be the curve, otherwise the points.
        self.mode = True

class Selector:
    #Use to record mouse clicked point.
    __slots__ = ('x', 'y', 'selection', 'MiddleButtonDrag', 'LeftButtonDrag')
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.selection = []
        self.MiddleButtonDrag = False
        self.LeftButtonDrag = False
    
    def distance(self, x, y):
        return round(sqrt((self.x-x)**2+(self.y-y)**2), 2)

class BaseCanvas(QWidget):
    def __init__(self, parent=None):
        super(BaseCanvas, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        #Origin coordinate
        self.ox = self.width()/2
        self.oy = self.height()/2
        #Canvas zoom rate
        self.rate = 2
        self.zoom = 2*self.rate
        #Canvas line width
        self.linkWidth = 3
        self.pathWidth = 3
        #Font size
        self.fontSize = 10
        #Show point mark or dimension
        self.showPointMark = True
        self.showDimension = True
        #Path track
        self.Path = Path()
        #Path solving
        self.slvsPath = ()
        self.showSlvsPath = False
    
    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.fillRect(event.rect(), QBrush(Qt.white))
        self.painter.translate(self.ox, self.oy)
    
    def drawFrame(self, pen):
        positive_x = self.width()-self.ox
        positive_y = -self.oy
        negative_x = -self.ox
        negative_y = self.height()-self.oy
        self.painter.setPen(pen)
        self.painter.drawLine(QPointF(negative_x, positive_y), QPointF(positive_x, positive_y))
        self.painter.drawLine(QPointF(negative_x, negative_y), QPointF(positive_x, negative_y))
        self.painter.drawLine(QPointF(negative_x, positive_y), QPointF(negative_x, negative_y))
        self.painter.drawLine(QPointF(positive_x, positive_y), QPointF(positive_x, negative_y))
    
    def drawPoint(self,
        i: int,
        cx,
        cy,
        fix: bool,
        color: QColor
    ):
        x = cx*self.zoom
        y = cy*-self.zoom
        pen = QPen(color)
        pen.setWidth(2)
        self.painter.setPen(pen)
        if fix:
            self.painter.drawPolygon(QPointF(x, y), QPointF(x-10, y+20), QPointF(x+10, y+20))
            self.painter.drawEllipse(QPointF(x, y), 10., 10.)
        else:
            self.painter.drawEllipse(QPointF(x, y), 5., 5.)
        if self.showPointMark:
            pen.setColor(Qt.darkGray)
            pen.setWidth(2)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.fontSize))
            text = '[{}]'.format(i) if type(i)==str else '[Point{}]'.format(i)
            if self.showDimension:
                text += ':({:.02f}, {:.02f})'.format(cx, cy)
            self.painter.drawText(QPointF(x+6, y-6), text)

class DynamicCanvas(BaseCanvas):
    mouse_track = pyqtSignal(float, float)
    mouse_getSelection = pyqtSignal(tuple)
    mouse_freemoveSelection = pyqtSignal(tuple)
    mouse_noSelection = pyqtSignal()
    mouse_getDoubleClickAdd = pyqtSignal()
    mouse_getDoubleClickEdit = pyqtSignal(int)
    change_event = pyqtSignal()
    zoom_change = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStatusTip("Use mouse wheel or middle button to look around.")
        self.Selector = Selector()
        #Entities
        self.Point = ()
        self.Link = ()
        #Point selection
        self.pointsSelection = []
        #Path solving range
        defult_range = QRectF(QPointF(-50., 50.), QSizeF(100., 100.))
        self.ranges = (defult_range, defult_range)
        #Set showDimension to False
        self.showDimension = False
        #Free move mode
        self.freemove = False
    
    def update_figure(self, Point, Link, path):
        self.Point = Point
        self.Link = Link
        self.Path.path = path
        self.update()
    
    @pyqtSlot(int)
    def setLinkWidth(self, linkWidth):
        self.linkWidth = linkWidth
        self.update()
    
    @pyqtSlot(int)
    def setPathWidth(self, pathWidth):
        self.pathWidth = pathWidth
        self.update()
    
    @pyqtSlot(bool)
    def setPointMark(self, showPointMark):
        self.showPointMark = showPointMark
        self.update()
    
    @pyqtSlot(bool)
    def setShowDimension(self, showDimension):
        self.showDimension = showDimension
        self.update()
    
    @pyqtSlot(int)
    def setFontSize(self, fontSize):
        self.fontSize = fontSize
        self.update()
    
    @pyqtSlot(int)
    def setZoom(self, zoom):
        self.zoom = zoom/100*self.rate
        self.update()
    
    @pyqtSlot(bool)
    def setFreeMove(self, freemove):
        self.freemove = freemove
        self.update()
    
    def changePointsSelection(self, pointsSelection):
        self.pointsSelection = pointsSelection
        self.update()
    
    def path_solving(self, slvsPath):
        self.slvsPath = slvsPath
        self.update()
    
    @pyqtSlot(tuple, float, tuple, float)
    def update_ranges(self, point1, range1, point2, range2):
        self.ranges = (
            QRectF(QPointF(point1[0]-range1/2, point1[1]+range1/2), QSizeF(range1, range1)),
            QRectF(QPointF(point2[0]-range2/2, point2[1]+range2/2), QSizeF(range2, range2))
        )
        self.update()
    
    def paintEvent(self, event):
        super(DynamicCanvas, self).paintEvent(event)
        #Draw origin lines.
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.painter.setPen(pen)
        self.painter.drawLine(QPointF(-self.ox, 0), QPointF(self.width()-self.ox, 0))
        self.painter.drawLine(QPointF(0, -self.oy), QPointF(0, self.height()-self.oy))
        if self.freemove:
            #Draw a colored frame for free move mode.
            pen = QPen(QColor(161, 105, 229))
            pen.setWidth(8)
            self.painter.setPen(pen)
            self.drawFrame(pen)
        #Draw links.
        for i, vlink in enumerate(self.Link[1:]):
            points = [self.Point[i] for i in vlink.points]
            self.drawLink(vlink.name, vlink.color, points)
        #Draw path.
        self.drawPath()
        #Draw points.
        for i, vpoint in enumerate(self.Point):
            fix = 'ground' in vpoint.links
            self.drawPoint(i, vpoint.cx, vpoint.cy, fix, vpoint.color)
        self.painter.end()
        self.change_event.emit()
    
    def drawPoint(self, i, cx, cy, fix, color):
        super(DynamicCanvas, self).drawPoint(i, cx, cy, fix, color)
        #For selects function.
        if i in self.pointsSelection:
            pen = QPen(QColor(161, 16, 239))
            pen.setWidth(3)
            self.painter.setPen(pen)
            self.painter.drawRect(cx*self.zoom - 12, cy*-self.zoom - 12, 24, 24)
    
    def drawLink(self,
        name: str,
        color: QColor,
        points: List['VPoint']
    ):
        pen = QPen(color)
        pen.setWidth(self.linkWidth)
        self.painter.setPen(pen)
        self.painter.setBrush(QColor(226, 219, 190))
        #Rearrange: Put the nearest point to the next position.
        for i in range(len(points)):
            if i==len(points)-1:
                break
            distanceList = [points[i].distance(p) for p in points]
            j = i + nsmallest(2, range(len(distanceList)-i), key=distanceList[i:].__getitem__)[-1]
            points[i+1], points[j] = points[j], points[i+1]
        qpoints = [QPointF(vpoint.cx*self.zoom, vpoint.cy*-self.zoom) for vpoint in points]
        if qpoints:
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.showPointMark and name!='ground' and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.fontSize))
            text = '[{}]'.format(name)
            cenX = sum([vpoint.cx for vpoint in points])/len(points)
            cenY = sum([vpoint.cy for vpoint in points])/len(points)
            self.painter.drawText(QPointF(cenX*self.zoom, cenY*-self.zoom), text)
    
    def drawPath(self):
        if self.Path.show:
            #draw paths.
            def drawPath(path):
                pointPath = QPainterPath()
                for i, (x, y) in enumerate(path):
                    x *= self.zoom
                    y *= -self.zoom
                    if i==0:
                        pointPath.moveTo(x, y)
                    else:
                        pointPath.lineTo(QPointF(x, y))
                self.painter.drawPath(pointPath)
            def drawDot(path):
                for x, y in path:
                    x *= self.zoom
                    y *= -self.zoom
                    self.painter.drawPoint(QPointF(x, y))
            draw = drawPath if self.Path.mode else drawDot
            if hasattr(self, 'PathRecord'):
                Path = self.PathRecord
            else:
                Path = self.Path.path
            for i, path in enumerate(Path):
                if len(set(path))>1:
                    try:
                        color = self.Point[i].color
                    except:
                        color = colorQt('Green')
                    pen = QPen(color)
                    pen.setWidth(self.pathWidth)
                    self.painter.setPen(pen)
                    draw(path)
        if self.showSlvsPath:
            #Draw solving range.
            for (i, rect), range_color in zip(enumerate(self.ranges), [QColor(138, 21, 196, 30), QColor(74, 178, 176, 30)]):
                pen = QPen(range_color)
                self.painter.setBrush(range_color)
                self.painter.setPen(pen)
                cx = rect.x()*self.zoom
                cy = rect.y()*-self.zoom
                self.painter.drawRect(QRectF(cx, cy, rect.width()*self.zoom, rect.height()*self.zoom))
                range_color.setAlpha(100)
                pen.setColor(range_color)
                pen.setWidth(2)
                self.painter.setPen(pen)
                self.painter.setBrush(Qt.NoBrush)
                self.painter.drawRect(QRectF(cx, cy, rect.width()*self.zoom, rect.height()*self.zoom))
                self.painter.setFont(QFont('Arial', self.fontSize+5))
                range_color.setAlpha(255)
                pen.setColor(range_color)
                self.painter.setPen(pen)
                if i==0:
                    self.painter.drawText(QPointF(cx-70+rect.width()*self.zoom, cy-6), 'Driver')
                else:
                    self.painter.drawText(QPointF(cx+6, cy-6), 'Follower')
            #Draw solving path.
            if self.slvsPath:
                pen = QPen(QColor(69, 247, 232))
                pen.setWidth(self.pathWidth)
                self.painter.setPen(pen)
                if self.Path.mode:
                    if len(self.slvsPath)>1:
                        pointPath = QPainterPath()
                        for i, (x, y) in enumerate(self.slvsPath):
                            x *= self.zoom
                            y *= -self.zoom
                            if i==0:
                                pointPath.moveTo(x, y)
                            else:
                                pointPath.lineTo(QPointF(x, y))
                        self.painter.drawPath(pointPath)
                    elif len(self.slvsPath)==1:
                        self.painter.drawPoint(QPointF(self.slvsPath[0][0]*self.zoom, self.slvsPath[0][1]*-self.zoom))
                else:
                    for x, y in self.slvsPath:
                        x *= self.zoom
                        y *= -self.zoom
                        self.painter.drawPoint(QPointF(x, y))
    
    def recordStart(self):
        self.PathRecord = [[] for i in range(len(self.Point))]
    
    #Recording path.
    def recordPath(self):
        for i, vpoint in enumerate(self.Point):
            self.PathRecord[i].append((vpoint.cx, vpoint.cy))
    
    #Return paths.
    def getRecordPath(self):
        path = tuple(tuple(path) if len(set(path))>1 else () for path in self.PathRecord)
        del self.PathRecord
        return path
    
    def mousePressEvent(self, event):
        self.Selector.x = event.x()-self.ox
        self.Selector.y = event.y()-self.oy
        if event.buttons()==Qt.MiddleButton:
            self.Selector.MiddleButtonDrag = True
        if event.buttons()==Qt.LeftButton:
            self.Selector.LeftButtonDrag = True
            self.mouseGetPoint()
            if self.Selector.selection:
                self.mouse_getSelection.emit(tuple(self.Selector.selection))
    
    def mouseDoubleClickEvent(self, event):
        if event.button()==Qt.MidButton:
            self.SetIn()
        if event.buttons()==Qt.LeftButton:
            self.Selector.x = event.x()-self.ox
            self.Selector.y = event.y()-self.oy
            self.mouseGetPoint()
            if self.Selector.selection:
                self.mouse_getSelection.emit((self.Selector.selection[0],))
                self.mouse_getDoubleClickEdit.emit(self.Selector.selection[0])
    
    def mouseGetPoint(self):
        self.Selector.selection.clear()
        for i, e in enumerate(self.Point):
            x = e.cx*self.zoom
            y = e.cy*-self.zoom
            if self.Selector.distance(x, y)<10:
                self.Selector.selection.append(i)
    
    def mouseReleaseEvent(self, event):
        #Only one clicked.
        if self.Selector.LeftButtonDrag:
            if QApplication.keyboardModifiers()==Qt.AltModifier:
                self.mouse_getDoubleClickAdd.emit()
            elif (
                (abs(event.x()-self.ox-self.Selector.x)<3) and
                (abs(event.y()-self.oy-self.Selector.y)<3)
            ):
                if (not self.Selector.selection and
                    (QApplication.keyboardModifiers()!=Qt.ControlModifier) and
                    (QApplication.keyboardModifiers()!=Qt.ShiftModifier)
                ):
                    self.mouse_noSelection.emit()
            elif self.freemove:
                self.mouse_freemoveSelection.emit(
                    tuple((row, (self.Point[row].cx, self.Point[row].cy)) for row in self.pointsSelection)
                )
        self.Selector.MiddleButtonDrag = False
        self.Selector.LeftButtonDrag = False
    
    def mouseMoveEvent(self, event):
        if self.Selector.MiddleButtonDrag:
            self.ox = event.x()-self.Selector.x
            self.oy = event.y()-self.Selector.y
            self.update()
        elif self.Selector.LeftButtonDrag and self.freemove:
            #Free move function.
            mouse_x = (event.x()-self.ox-self.Selector.x)/self.zoom
            mouse_y = -(event.y()-self.oy-self.Selector.y)/self.zoom
            for row in self.pointsSelection:
                vpoint = self.Point[row]
                vpoint.move((mouse_x + vpoint.x, mouse_y + vpoint.y))
            self.update()
        self.mouse_track.emit((event.x()-self.ox)/self.zoom, -((event.y()-self.oy)/self.zoom))
    
    def SetIn(self):
        width = self.width()
        height = self.height()
        height = height if not height==0 else 1
        if len(self.Point)<=1:
            self.zoom_change.emit(200)
            self.ox = width/2
            self.oy = height/2
        else:
            Xs = tuple(e.cx for e in self.Point) if self.Point else (0,)
            Ys = tuple(e.cy for e in self.Point) if self.Point else (0,)
            if self.Path.path:
                Path = self.Path.path
                Comparator = lambda fun, i: fun(fun(path[i] for path in point if point) for point in Path if point)
                pathMaxX = Comparator(max, 0)
                pathMinX = Comparator(min, 0)
                pathMaxY = Comparator(max, 1)
                pathMinY = Comparator(min, 1)
                diffX = max(max(Xs), pathMaxX)-min(min(Xs), pathMinX)
                diffY = max(max(Ys), pathMaxY)-min(min(Ys), pathMinY)
                cenx = (min(min(Xs), pathMinX)+max(max(Xs), pathMaxX))/2
                ceny = (min(min(Ys), pathMinY)+max(max(Ys), pathMaxY))/2
            else:
                diffX = max(Xs)-min(Xs)
                diffY = max(Ys)-min(Ys)
                cenx = (min(Xs)+max(Xs))/2
                ceny = (min(Ys)+max(Ys))/2
            diffY = diffY if diffY!=0 else 1
            height = height if height!=0 else 1
            cdiff = diffX/diffY > width/height
            self.zoom_change.emit(int((width if cdiff else height)/(diffX if cdiff else diffY)*0.95*50))
            self.ox = (width/2)-cenx*self.zoom
            self.oy = (height/2)+ceny*self.zoom
        self.update()
