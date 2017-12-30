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
from math import (
    sin,
    cos,
    atan2,
    sqrt,
    isnan
)
from collections import deque
from heapq import nsmallest
from typing import TypeVar, List, Tuple
function = TypeVar("function")
from .color import colorQt

class Path:
    __slots__ = ('path', 'show', 'curve')
    
    def __init__(self):
        self.path = ()
        '''
        -1: show all
        -2: hide path.
        '''
        self.show = -1
        #Display mode: The path will be the curve, otherwise the points.
        self.curve = True

class Selector:
    #Use to record mouse clicked point.
    __slots__ = (
        'x', 'y', 'selection',
        'selection_rect', 'selection_old',
        'MiddleButtonDrag',
        'LeftButtonDrag',
        'sx', 'sy', 'RectangularSelection'
    )
    
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.selection = []
        self.selection_rect = []
        self.selection_old = []
        self.MiddleButtonDrag = False
        self.LeftButtonDrag = False
        self.RectangularSelection = False
        self.sx = 0.
        self.sy = 0.
    
    def distance(self, x, y):
        return round(sqrt((self.x-x)**2+(self.y-y)**2), 2)
    
    def inRect(self, x, y):
        x_in_range = lambda u: min(self.x, self.sx) <= u <= max(self.x, self.sx)
        y_in_range = lambda v: min(self.y, self.sy) <= v <= max(self.y, self.sy)
        return x_in_range(x) and y_in_range(y)

class BaseCanvas(QWidget):
    def __init__(self, parent=None):
        super(BaseCanvas, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        #Origin coordinate
        self.ox = self.width()/2
        self.oy = self.height()/2
        #Canvas zoom rate
        self.rate = 2
        self.zoom = 2 * self.rate
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
        #Draw origin lines.
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.painter.setPen(pen)
        x_l = -self.ox
        x_r = self.width()-self.ox
        self.painter.drawLine(QPointF(x_l, 0), QPointF(x_r, 0))
        y_t = self.height()-self.oy
        y_b = -self.oy
        self.painter.drawLine(QPointF(0, y_b), QPointF(0, y_t))
        #Draw tick.
        Indexing = lambda v: int(v/self.zoom - (v/self.zoom)%5)
        for x in range(Indexing(x_l), Indexing(x_r)+1, 5):
            self.painter.drawLine(QPointF(x*self.zoom, 0), QPointF(x*self.zoom, -10 if x%10==0 else -5))
        for y in range(Indexing(y_b), Indexing(y_t)+1, 5):
            self.painter.drawLine(QPointF(0, y*self.zoom), QPointF(10 if y%10==0 else 5, y*self.zoom))
    
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
        pen = QPen(color)
        pen.setWidth(2)
        self.painter.setPen(pen)
        x = cx*self.zoom
        y = cy*-self.zoom
        if fix:
            bottom = y + 20
            width = 10
            self.painter.drawPolygon(QPointF(x, y), QPointF(x - width, bottom), QPointF(x + width, bottom))
            self.painter.drawEllipse(QPointF(x, y), width, width)
        else:
            self.painter.drawEllipse(QPointF(x, y), 5, 5)
        if self.showPointMark:
            pen.setColor(Qt.darkGray)
            pen.setWidth(2)
            self.painter.setPen(pen)
            self.painter.setFont(QFont("Arial", self.fontSize))
            text = "[{}]".format(i) if type(i)==str else "[Point{}]".format(i)
            if self.showDimension:
                text += ":({:.02f}, {:.02f})".format(cx, cy)
            self.painter.drawText(QPointF(x+6, y-6), text)

class DynamicCanvas(BaseCanvas):
    mouse_track = pyqtSignal(float, float)
    mouse_browse_track = pyqtSignal(float, float)
    mouse_getSelection = pyqtSignal(tuple, bool)
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
        #Entities.
        self.Point = ()
        self.Link = ()
        #Point selection.
        self.selectionRadius = 10
        self.pointsSelection = []
        #Linkage transparency.
        self.transparency = 1.
        #Path solving range.
        defult_range = QRectF(QPointF(-50., 50.), QSizeF(100., 100.))
        self.ranges = (defult_range, defult_range)
        #Set showDimension to False.
        self.showDimension = False
        #Free move mode. (0: no free move. 1: translate. 2: rotate.)
        self.freemove = 0
        #Set zoom bar function
        self.setZoomValue = lambda a: parent.ZoomBar.setValue(parent.ZoomBar.value() + parent.ScaleFactor.value()*a/abs(a))
    
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
    
    @pyqtSlot(bool)
    def setCurveMode(self, curve):
        self.Path.curve = curve
        self.update()
    
    @pyqtSlot(int)
    def setFontSize(self, fontSize):
        self.fontSize = fontSize
        self.update()
    
    @pyqtSlot(int)
    def setZoom(self, zoom):
        self.zoom = zoom/100*self.rate
        self.update()
    
    def setShowSlvsPath(self, showSlvsPath):
        self.showSlvsPath = showSlvsPath
        self.update()
    
    def setFreeMove(self, freemove):
        self.freemove = freemove
        self.update()
    
    @pyqtSlot(int)
    def setSelectionRadius(self, selectionRadius):
        self.selectionRadius = selectionRadius
    
    @pyqtSlot(int)
    def setTransparency(self, transparency):
        self.transparency = (100 - transparency)/100
        self.update()
    
    def changePointsSelection(self, pointsSelection):
        self.pointsSelection = pointsSelection
        self.update()
    
    def path_solving(self, slvsPath: Tuple[Tuple[float, float]]):
        self.slvsPath = slvsPath
        self.update()
    
    def setPathShow(self, p: int):
        self.Path.show = p
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
        if self.freemove:
            #Draw a colored frame for free move mode.
            pen = QPen()
            if self.freemove==1:
                pen.setColor(QColor(161, 105, 229))
            elif self.freemove==2:
                pen.setColor(QColor(219, 162, 6))
            elif self.freemove==3:
                pen.setColor(QColor(79, 249, 193))
            pen.setWidth(8)
            self.painter.setPen(pen)
            self.drawFrame(pen)
        if self.Selector.RectangularSelection:
            pen = QPen(Qt.gray)
            pen.setWidth(1)
            self.painter.setPen(pen)
            self.painter.drawRect(QRectF(
                QPointF(self.Selector.x, self.Selector.y),
                QPointF(self.Selector.sx, self.Selector.sy)
            ))
        #Draw links.
        for vlink in self.Link[1:]:
            self.drawLink(vlink)
        #Draw path.
        self.drawPath()
        #Draw points.
        for i, vpoint in enumerate(self.Point):
            self.drawPoint(i, vpoint)
        self.painter.end()
        self.change_event.emit()
    
    def drawPoint(self, i, vpoint):
        if vpoint.type==1 or vpoint.type==2:
            #Draw slider
            silder_points = vpoint.c
            for j, (cx, cy) in enumerate(silder_points):
                if vpoint.type==1:
                    if j==0:
                        super(DynamicCanvas, self).drawPoint(i, cx, cy, vpoint.links[j]=='ground', vpoint.color)
                    else:
                        pen = QPen(vpoint.color)
                        pen.setWidth(2)
                        self.painter.setPen(pen)
                        r = 5
                        self.painter.drawRect(QRectF(
                            QPointF(cx*self.zoom + r, cy*-self.zoom + r),
                            QPointF(cx*self.zoom - r, cy*-self.zoom - r)
                        ))
                elif vpoint.type==2:
                    if j==0:
                        super(DynamicCanvas, self).drawPoint(i, cx, cy, vpoint.links[j]=='ground', vpoint.color)
                    else:
                        #Turn off point mark.
                        showPointMark = self.showPointMark
                        self.showPointMark = False
                        super(DynamicCanvas, self).drawPoint(i, cx, cy, vpoint.links[j]=='ground', vpoint.color)
                        self.showPointMark = showPointMark
            pen = QPen(vpoint.color.darker())
            pen.setWidth(2)
            self.painter.setPen(pen)
            x_all = tuple(cx for cx, cy in silder_points)
            if x_all:
                p_left = silder_points[x_all.index(min(x_all))]
                p_right = silder_points[x_all.index(max(x_all))]
                if p_left==p_right:
                    y_all = tuple(cy for cx, cy in silder_points)
                    p_left = silder_points[y_all.index(min(y_all))]
                    p_right = silder_points[y_all.index(max(y_all))]
                self.painter.drawLine(QPointF(p_left[0]*self.zoom, p_left[1]*-self.zoom), QPointF(p_right[0]*self.zoom, p_right[1]*-self.zoom))
        else:
            super(DynamicCanvas, self).drawPoint(i, vpoint.cx, vpoint.cy, 'ground' in vpoint.links, vpoint.color)
        #For selects function.
        if i in self.pointsSelection:
            pen = QPen(QColor(161, 16, 239))
            pen.setWidth(3)
            self.painter.setPen(pen)
            self.painter.drawRect(vpoint.cx*self.zoom - 12, vpoint.cy*-self.zoom - 12, 24, 24)
    
    def drawLink(self, vlink):
        points = []
        for i in vlink.points:
            vpoint = self.Point[i]
            if vpoint.type==1 or vpoint.type==2:
                coordinate = vpoint.c[vpoint.links.index(vlink.name)]
                x = coordinate[0]
                y = coordinate[1]
            else:
                x = vpoint.cx
                y = vpoint.cy
            points.append((x, y))
        pen = QPen(vlink.color)
        pen.setWidth(self.linkWidth)
        self.painter.setPen(pen)
        brush = QColor(226, 219, 190)
        brush.setAlphaF(self.transparency)
        self.painter.setBrush(brush)
        #Rearrange: Put the nearest point to the next position.
        distance = lambda p1, p2: sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
        for i in range(len(points)):
            if i==len(points)-1:
                break
            distanceList = [distance(points[i], p) for p in points]
            j = i + nsmallest(2, range(len(distanceList)-i), key=distanceList[i:].__getitem__)[-1]
            points[i+1], points[j] = points[j], points[i+1]
        qpoints = [QPointF(p[0]*self.zoom, p[1]*-self.zoom) for p in points]
        if qpoints:
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.showPointMark and vlink.name!='ground' and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.fontSize))
            text = '[{}]'.format(vlink.name)
            cenX = sum([p[0] for p in points])/len(points)
            cenY = sum([p[1] for p in points])/len(points)
            self.painter.drawText(QPointF(cenX*self.zoom, cenY*-self.zoom), text)
    
    def drawPath(self):
        if self.Path.show>-2:
            #draw paths.
            def drawPath(path):
                pointPath = QPainterPath()
                for i, (x, y) in enumerate(path):
                    if isnan(x):
                        continue
                    else:
                        if i==0:
                            pointPath.moveTo(x*self.zoom, y*-self.zoom)
                        else:
                            pointPath.lineTo(QPointF(x*self.zoom, y*-self.zoom))
                self.painter.drawPath(pointPath)
            def drawDot(path):
                for i, (x, y) in enumerate(path):
                    if isnan(x):
                        continue
                    else:
                        self.painter.drawPoint(QPointF(x*self.zoom, y*-self.zoom))
            draw = drawPath if self.Path.curve else drawDot
            if hasattr(self, 'PathRecord'):
                Path = self.PathRecord
            else:
                Path = self.Path.path
            for i, path in enumerate(Path):
                if self.Path.show!=i and self.Path.show!=-1:
                    continue
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
                self.painter.setBrush(range_color)
                range_color.setAlpha(255)
                pen = QPen(range_color)
                pen.setWidth(5)
                self.painter.setPen(pen)
                cx = rect.x()*self.zoom
                cy = rect.y()*-self.zoom
                if rect.width():
                    self.painter.drawRect(QRectF(cx, cy, rect.width()*self.zoom, rect.height()*self.zoom))
                else:
                    self.painter.drawEllipse(QPointF(cx, cy), 3, 3)
                self.painter.setFont(QFont("Arial", self.fontSize+5))
                range_color.setAlpha(255)
                pen.setColor(range_color)
                self.painter.setPen(pen)
                if i==0:
                    self.painter.drawText(QPointF(cx-70+rect.width()*self.zoom, cy-6), "Driver")
                else:
                    self.painter.drawText(QPointF(cx+6, cy-6), "Follower")
                self.painter.setBrush(Qt.NoBrush)
            #Draw solving path.
            if self.slvsPath:
                pen = QPen(QColor(3, 163, 120))
                pen.setWidth(self.pathWidth)
                self.painter.setPen(pen)
                self.painter.setBrush(QColor(74, 178, 176, 30))
                if len(self.slvsPath)>1:
                    pointPath = QPainterPath()
                    for i, (x, y) in enumerate(self.slvsPath):
                        x *= self.zoom
                        y *= -self.zoom
                        self.painter.drawEllipse(QPointF(x, y), 3, 3)
                        if i==0:
                            pointPath.moveTo(x, y)
                        else:
                            pointPath.lineTo(QPointF(x, y))
                    pen.setColor(QColor(69, 247, 232))
                    self.painter.setPen(pen)
                    self.painter.drawPath(pointPath)
                elif len(self.slvsPath)==1:
                    self.painter.drawEllipse(QPointF(self.slvsPath[0][0]*self.zoom, self.slvsPath[0][1]*-self.zoom), 3, 3)
                self.painter.setBrush(Qt.NoBrush)
    
    def recordStart(self, limit):
        self.PathRecord = [deque([], limit) for i in range(len(self.Point))]
    
    #Recording path.
    def recordPath(self):
        for i, vpoint in enumerate(self.Point):
            self.PathRecord[i].append((vpoint.cx, vpoint.cy))
    
    #Return paths.
    def getRecordPath(self):
        path = tuple(tuple(path) if len(set(path))>1 else () for path in self.PathRecord)
        del self.PathRecord
        return path
    
    def wheelEvent(self, event):
        self.setZoomValue(event.angleDelta().y())
    
    def mousePressEvent(self, event):
        self.Selector.x = event.x() - self.ox
        self.Selector.y = event.y() - self.oy
        if event.buttons()==Qt.MiddleButton:
            self.Selector.MiddleButtonDrag = True
            x = self.Selector.x / self.zoom
            y = self.Selector.y / -self.zoom
            self.mouse_browse_track.emit(x, y)
        if event.buttons()==Qt.LeftButton:
            self.Selector.LeftButtonDrag = True
            self.mouseSelectedPoint()
            if self.Selector.selection:
                self.mouse_getSelection.emit(tuple(self.Selector.selection), True)
    
    def mouseDoubleClickEvent(self, event):
        if event.button()==Qt.MidButton:
            self.SetIn()
        if event.buttons()==Qt.LeftButton:
            self.Selector.x = event.x() - self.ox
            self.Selector.y = event.y() - self.oy
            self.mouseSelectedPoint()
            if self.Selector.selection:
                self.mouse_getSelection.emit((self.Selector.selection[0],), True)
                self.mouse_getDoubleClickEdit.emit(self.Selector.selection[0])
    
    def mouseSelectedPoint(self):
        self.selectedPointFunc(
            self.Selector.selection,
            lambda *args: self.Selector.distance(*args) < self.selectionRadius
        )
    
    def RectangularSelectedPoint(self):
        self.selectedPointFunc(
            self.Selector.selection_rect,
            self.Selector.inRect
        )
    
    def selectedPointFunc(self, selection: List[int], inSelection: function):
        selection.clear()
        for i, vpoint in enumerate(self.Point):
            if inSelection(vpoint.cx * self.zoom, vpoint.cy * -self.zoom):
                if i not in selection:
                    selection.append(i)
    
    def mouseReleaseEvent(self, event):
        if self.Selector.LeftButtonDrag:
            self.Selector.selection_old = list(self.pointsSelection)
            km = QApplication.keyboardModifiers()
            #Add Point
            if km==Qt.AltModifier:
                self.mouse_getDoubleClickAdd.emit()
            #Only one clicked.
            elif (
                (abs(event.x() - self.ox - self.Selector.x) < self.selectionRadius/2) and
                (abs(event.y() - self.oy - self.Selector.y) < self.selectionRadius/2)
            ):
                if (not self.Selector.selection) and km!=Qt.ControlModifier and km!=Qt.ShiftModifier:
                    self.mouse_noSelection.emit()
            #Edit point coordinates.
            elif self.freemove:
                self.mouse_freemoveSelection.emit(
                    tuple((row, (self.Point[row].cx, self.Point[row].cy)) for row in self.pointsSelection)
                )
        self.Selector.selection_rect.clear()
        self.Selector.MiddleButtonDrag = False
        self.Selector.LeftButtonDrag = False
        self.Selector.RectangularSelection = False
        self.update()
    
    def mouseMoveEvent(self, event):
        x = (event.x() - self.ox)/self.zoom
        y = (event.y() - self.oy)/-self.zoom
        if self.Selector.MiddleButtonDrag:
            self.ox = event.x() - self.Selector.x
            self.oy = event.y() - self.Selector.y
        elif self.Selector.LeftButtonDrag:
            if self.freemove:
                if self.pointsSelection:
                    if self.freemove==1:
                        #Free move translate function.
                        mouse_x = x - self.Selector.x/self.zoom
                        mouse_y = y - self.Selector.y/-self.zoom
                        for row in self.pointsSelection:
                            vpoint = self.Point[row]
                            vpoint.move((mouse_x + vpoint.x, mouse_y + vpoint.y))
                    elif self.freemove==2:
                        #Free move rotate function.
                        alpha = atan2(y, x) - atan2(self.Selector.y/-self.zoom, self.Selector.x/self.zoom)
                        for row in self.pointsSelection:
                            vpoint = self.Point[row]
                            r = sqrt(vpoint.x**2 + vpoint.y**2)
                            beta = atan2(vpoint.y, vpoint.x)
                            vpoint.move((r*cos(alpha + beta), r*sin(alpha + beta)))
                    elif self.freemove==3:
                        #Free move reflect function.
                        factor_x = 1 if x > 0 else -1
                        factor_y = 1 if y > 0 else -1
                        for row in self.pointsSelection:
                            vpoint = self.Point[row]
                            vpoint.move((vpoint.x*factor_x, vpoint.y*factor_y))
            else:
                #Rectangular selection
                self.Selector.RectangularSelection = True
                self.Selector.sx = event.x() - self.ox
                self.Selector.sy = event.y() - self.oy
                self.RectangularSelectedPoint()
                km = QApplication.keyboardModifiers()
                if self.Selector.selection_rect:
                    if km==Qt.ControlModifier or km==Qt.ShiftModifier:
                        self.mouse_getSelection.emit(tuple(set(self.Selector.selection_old + self.Selector.selection_rect)), False)
                    else:
                        self.mouse_getSelection.emit(tuple(self.Selector.selection_rect), False)
                else:
                    self.mouse_noSelection.emit()
        self.update()
        self.mouse_track.emit(x, y)
    
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
                Comparator = lambda fun, i, d: fun(
                    fun(fun(path[i] for path in point if not isnan(path[i])) for point in self.Path.path if point),
                    fun(d)
                )
                pathMaxX = Comparator(max, 0, Xs)
                pathMinX = Comparator(min, 0, Xs)
                pathMaxY = Comparator(max, 1, Ys)
                pathMinY = Comparator(min, 1, Ys)
                diffX = pathMaxX - pathMinX
                diffY = pathMaxY - pathMinY
                cenx = (pathMinX + pathMaxX)/2
                ceny = (pathMinY + pathMaxY)/2
            else:
                diffX = max(Xs) - min(Xs)
                diffY = max(Ys) - min(Ys)
                cenx = (min(Xs) + max(Xs))/2
                ceny = (min(Ys) + max(Ys))/2
            diffY = diffY if diffY!=0 else 1
            height = height if height!=0 else 1
            diff = diffX/diffY > width/height
            self.zoom_change.emit(int((width if diff else height)/(diffX if diff else diffY)*0.95*50))
            self.ox = width/2 - cenx*self.zoom
            self.oy = height/2 + ceny*self.zoom
        self.update()
