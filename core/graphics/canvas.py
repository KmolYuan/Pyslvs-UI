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
from ..graphics.color import colorlist, colorName
tr = QCoreApplication.translate

class PointOptions:
    def __init__(self, width, height):
        self.ox = width/2
        self.oy = height/2
        self.rate = 2
        self.Path = Path()
        self.slvsPath = {'path':[], 'show':False}
        self.currentShaft = ()

class Path:
    def __init__(self):
        self.path = []
        self.demo = 0.
        self.show = True
        self.mode = True
        self.drive_mode = False
        defult_range = QRectF(QPointF(-50., 50.), QSizeF(100., 100.))
        self.ranges = [defult_range, defult_range]

class Selector:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.MiddleButtonDrag = False
    
    def distance(self, x, y):
        return round(sqrt((self.x-x)**2+(self.y-y)**2), 2)

class BaseCanvas(QWidget):
    def __init__(self, parent=None):
        super(BaseCanvas, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.options = PointOptions(self.width(), self.height())
        self.linkWidth = 3
        self.pathWidth = 3
        self.Color = colorlist()
        self.Font_size = 10
        self.Point_mark = True
        self.showDimension = True
    
    def paintEvent(self, event):
        self.painter = QPainter()
        self.painter.begin(self)
        self.painter.fillRect(event.rect(), QBrush(Qt.white))
    
    def drawPoint(self,
        i: int,
        cx,
        cy,
        fix: bool,
        color: QColor
    ):
        x = cx*self.zoom
        y = cy*self.zoom*-1
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(color)
        self.painter.setPen(pen)
        if fix:
            self.painter.drawPolygon(QPointF(x, y), QPointF(x-10, y+20), QPointF(x+10, y+20))
            self.painter.drawEllipse(QPointF(x, y), 10., 10.)
        else:
            self.painter.drawEllipse(QPointF(x, y), 5., 5.)
        if self.Point_mark:
            pen.setColor(Qt.darkGray)
            pen.setWidth(2)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.Font_size))
            text = '[{}]'.format(i) if type(i)==str else '[Point{}]'.format(i)
            if self.showDimension:
                text += ':({:.02f}, {:.02f})'.format(cx, cy)
            self.painter.drawText(QPointF(x+6, y-6), text)
    
    def drawLink(self,
        name: str,
        color: QColor,
        points: List['VPoint']
    ):
        pen = QPen()
        pen.setWidth(self.linkWidth)
        pen.setColor(color)
        self.painter.setPen(pen)
        self.painter.setBrush(QColor(226, 219, 190))
        #Rearrange: Put the nearest point to the next position.
        for i in range(len(points)):
            if i==len(points)-1:
                break
            distanceList = [points[i].distance(p) for p in points]
            j = i + nsmallest(2, range(len(distanceList)-i), key=distanceList[i:].__getitem__)[-1]
            points[i+1], points[j] = points[j], points[i+1]
        qpoints = [QPointF(vpoint.cx*self.zoom, vpoint.cy*self.zoom*-1) for vpoint in points]
        if qpoints:
            self.painter.drawPolygon(*qpoints)
        self.painter.setBrush(Qt.NoBrush)
        if self.Point_mark and name!='ground' and qpoints:
            pen.setColor(Qt.darkGray)
            self.painter.setPen(pen)
            self.painter.setFont(QFont('Arial', self.Font_size))
            text = '[{}]'.format(name)
            cenX = sum([vpoint.cx for vpoint in points])/len(points)
            cenY = sum([vpoint.cy for vpoint in points])/len(points)
            self.painter.drawText(QPointF(cenX*self.zoom, cenY*self.zoom*-1), text)
    
    def drawShaft(self, i, x0, y0, x1, y1):
        pen = QPen()
        pen.setWidth(self.linkWidth+2)
        pen.setColor(QColor(225, 140, 0) if i==self.options.currentShaft else QColor(175, 90, 0))
        self.painter.setPen(pen)
        self.painter.drawLine(QPointF(x0, y0), QPointF(x1, y1))

class DynamicCanvas(BaseCanvas):
    mouse_track = pyqtSignal(float, float)
    mouse_getSelection = pyqtSignal(tuple)
    mouse_noSelection = pyqtSignal()
    mouse_getDoubleClickAdd = pyqtSignal()
    mouse_getDoubleClickEdit = pyqtSignal(int)
    change_event = pyqtSignal()
    zoom_change = pyqtSignal(int)
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStatusTip(tr("DynamicCanvas", "Use mouse wheel or middle button to look around."))
        self.rotateAngle = 0
        self.Selector = Selector()
        self.re_Color = colorName()
        self.pointsSelection = []
        self.zoom = 2*self.options.rate
        self.linkWidth = 3
        self.pathWidth = 3
        self.rotateAngle = 0.
        self.showDimension = False
    
    def update_figure(self, Point, Link, path):
        self.Point = Point
        self.Link = Link
        self.options.Path.path = path
        self.update()
    
    @pyqtSlot(int)
    def setLinkWidth(self, linkWidth):
        self.linkWidth = linkWidth
        self.update()
    
    @pyqtSlot(int)
    def setPathWidth(self, pathWidth):
        self.pathWidth = pathWidth
        self.update()
    
    @pyqtSlot(float)
    def setRotateAngle(self, rotateAngle):
        self.rotateAngle = rotateAngle
        self.update()
    
    @pyqtSlot(bool)
    def setPointMark(self, PointMark):
        self.Point_mark = PointMark
        self.update()
    
    @pyqtSlot(bool)
    def setShowDimension(self, showDimension):
        self.showDimension = showDimension
        self.update()
    
    @pyqtSlot(int)
    def setFontSize(self, fontSize):
        self.Font_size = fontSize
        self.update()
    
    @pyqtSlot(int)
    def setZoom(self, zoom):
        self.zoom = zoom/100*self.options.rate
        self.update()
    
    def changePointsSelection(self, pointsSelection):
        self.pointsSelection = pointsSelection
        self.update()
    
    @pyqtSlot(int, float, int)
    def changeCurrentShaft(self, point=0, angle=0., link=0):
        self.options.currentShaft = (point, angle, link)
        self.update()
    
    def resetCurrentShaft(self):
        self.options.currentShaft = ()
        self.update()
    
    def path_solving(self, path=[]):
        self.options.slvsPath['path'] = path
        self.update()
    
    @pyqtSlot(tuple, float, tuple, float)
    def update_ranges(self, point1, range1, point2, range2):
        self.options.Path.ranges[0] = QRectF(QPointF(point1[0]-range1/2, point1[1]+range1/2), QSizeF(range1, range1))
        self.options.Path.ranges[1] = QRectF(QPointF(point2[0]-range2/2, point2[1]+range2/2), QSizeF(range2, range2))
        self.update()
    
    def paintEvent(self, event):
        super(DynamicCanvas, self).paintEvent(event)
        self.painter.translate(self.options.ox, self.options.oy)
        self.painter.rotate(self.rotateAngle)
        pathShaft = None
        if self.options.Path.drive_mode:
            for vpaths in self.options.Path.path:
                if vpaths.shaft==self.options.currentShaft:
                    pathShaft = vpaths
        if (not pathShaft==None) and (not pathShaft.isBroken()):
            shaft = self.Shaft[pathShaft.shaft]
            resolution = abs(shaft.end-shaft.start)/(len(pathShaft.paths[0].path)-1)
            resolutionIndex = int(round(self.options.Path.demo/resolution))
            pathPoints = {e.point:e for e in pathShaft.paths}
            for i, vlink in enumerate(self.Link):
                p1x = (self.Point[e.start].cx if self.Point[e.start].fix else pathPoints[e.start].path[resolutionIndex][0])*self.zoom
                p1y = (self.Point[e.start].cy if self.Point[e.start].fix else pathPoints[e.start].path[resolutionIndex][1])*self.zoom*-1
                p2x = (self.Point[e.end].cx if self.Point[e.end].fix else pathPoints[e.end].path[resolutionIndex][0])*self.zoom
                p2y = (self.Point[e.end].cy if self.Point[e.end].fix else pathPoints[e.end].path[resolutionIndex][1])*self.zoom*-1
                self.drawLink(i, p1x, p1y, p2x, p2y, e.len)
            self.drawPath()
            for path in pathShaft.paths:
                point = path.path[resolutionIndex]
                fix = 'ground' in self.Point[path.point].Links
                self.drawPoint(path.point, point[0], point[1], fix, self.Point[path.point].color)
            for i, vpoint in enumerate(self.Point):
                if i in pathPoints:
                    continue
                fix = 'ground' in vpoint.Links
                self.drawPoint(i, vpoint.cx, vpoint.cy, fix, vpoint.color)
        else:
            for i, vlink in enumerate(self.Link):
                points = [self.Point[i] for i in vlink.Points]
                self.drawLink(vlink.name, vlink.color, points)
            self.drawPath()
            for i, vpoint in enumerate(self.Point):
                fix = 'ground' in vpoint.Links
                self.drawPoint(i, vpoint.cx, vpoint.cy, fix, vpoint.color)
        if self.options.slvsPath['path'] and self.options.slvsPath['show']:
            pen = QPen()
            pathData = self.options.slvsPath['path']
            pen.setWidth(self.pathWidth)
            pen.setColor(QColor(69, 247, 232))
            self.painter.setPen(pen)
            if self.options.Path.mode==True:
                if len(pathData)>1:
                    pointPath = QPainterPath()
                    for i, e in enumerate(pathData):
                        x = e['x']*self.zoom
                        y = e['y']*self.zoom*-1
                        if i==0:
                            pointPath.moveTo(x, y)
                        else:
                            pointPath.lineTo(QPointF(x, y))
                    self.painter.drawPath(pointPath)
                elif len(pathData)==1:
                    self.painter.drawPoint(QPointF(pathData[0]['x']*self.zoom, pathData[0]['y']*self.zoom*-1))
            else:
                for i, e in enumerate(pathData):
                    x = e['x']*self.zoom
                    y = e['y']*self.zoom*-1
                    self.painter.drawPoint(QPointF(x, y))
        self.painter.end()
        self.change_event.emit()
    
    def drawPoint(self, i, cx, cy, fix, color):
        super(DynamicCanvas, self).drawPoint(i, cx, cy, fix, color)
        if i in self.pointsSelection:
            pen = QPen()
            pen.setWidth(3)
            pen.setColor(QColor(161, 16, 239))
            self.painter.setPen(pen)
            self.painter.drawRect(cx*self.zoom-12, cy*self.zoom*(-1)-12, 24, 24)
    
    def drawPath(self):
        if self.options.Path.show:
            for vpaths in self.options.Path.path:
                for vpath in vpaths.paths:
                    if vpath.show:
                        pen = QPen()
                        pen.setWidth(self.pathWidth)
                        if vpaths.shaft==self.options.currentShaft:
                            pen.setColor(self.Color[self.Point[vpath.point].color])
                        else:
                            pen.setColor(self.Color['Gray'])
                        self.painter.setPen(pen)
                        if self.options.Path.mode==True:
                            error = False
                            pointPath = QPainterPath()
                            for i, point in enumerate(vpath.path):
                                if point is None or point[0] is None or point[0] is False:
                                    error = True
                                    continue
                                x = point[0]*self.zoom
                                y = point[1]*self.zoom*-1
                                if i==0 or error:
                                    pointPath.moveTo(x, y)
                                    error = False
                                else:
                                    pointPath.lineTo(QPointF(x, y))
                            self.painter.drawPath(pointPath)
                        else:
                            for i, point in enumerate(vpath.path):
                                if point[0] is None or point[0] is False:
                                    continue
                                x = point[0]*self.zoom
                                y = point[1]*self.zoom*-1
                                self.painter.drawPoint(QPointF(x, y))
        if self.options.slvsPath['show']:
            for (i, rect), range_color in zip(enumerate(self.options.Path.ranges), [QColor(138, 21, 196, 30), QColor(74, 178, 176, 30)]):
                pen = QPen()
                pen.setColor(range_color)
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
                self.painter.setFont(QFont('Arial', self.Font_size+5))
                range_color.setAlpha(255)
                pen.setColor(range_color)
                self.painter.setPen(pen)
                if i==0:
                    self.painter.drawText(QPointF(cx-70+rect.width()*self.zoom, cy-6), 'Driver')
                else:
                    self.painter.drawText(QPointF(cx+6, cy-6), 'Follower')
    
    def mousePressEvent(self, event):
        self.Selector.x = event.x()-self.options.ox
        self.Selector.y = event.y()-self.options.oy
        if event.buttons()==Qt.MiddleButton:
            self.Selector.MiddleButtonDrag = True
        if event.buttons()==Qt.LeftButton:
            if QApplication.keyboardModifiers()==Qt.AltModifier:
                self.mouse_getDoubleClickAdd.emit()
            else:
                selection = []
                for i, e in enumerate(self.Point):
                    x = e.cx*self.zoom
                    y = e.cy*self.zoom*-1
                    if self.Selector.distance(x, y)<10:
                        selection.append(i)
                if selection:
                    self.mouse_getSelection.emit(tuple(selection))
                elif not QApplication.keyboardModifiers()==Qt.ControlModifier:
                    self.mouse_noSelection.emit()
    
    def mouseDoubleClickEvent(self, event):
        if event.button()==Qt.MidButton:
            self.SetIn()
        if event.buttons()==Qt.LeftButton:
            self.Selector.x = event.x()-self.options.ox
            self.Selector.y = event.y()-self.options.oy
            for i, e in enumerate(self.Point):
                x = e.cx*self.zoom
                y = e.cy*self.zoom*-1
                if self.Selector.distance(x, y)<10:
                    self.mouse_getDoubleClickEdit.emit(i)
                    break
    
    def mouseReleaseEvent(self, event):
        self.Selector.MiddleButtonDrag = False
    
    def mouseMoveEvent(self, event):
        if self.Selector.MiddleButtonDrag:
            self.options.ox = event.x()-self.Selector.x
            self.options.oy = event.y()-self.Selector.y
            self.update()
        self.mouse_track.emit((event.x()-self.options.ox)/self.zoom, -((event.y()-self.options.oy)/self.zoom))
        if QApplication.keyboardModifiers()==Qt.AltModifier:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
    
    def resizeEvent(self, event):
        self.SetIn()
    
    def SetIn(self):
        width = self.width()
        height = self.height()
        height = height if not height==0 else 1
        if len(self.Point)==1:
            self.zoom_change.emit(200)
            self.options.ox = width/2
            self.options.oy = height/2
        else:
            Xs = [e.cx for e in self.Point] if self.Point else [0]
            Ys = [e.cy for e in self.Point] if self.Point else [0]
            if self.options.Path.path:
                Path = self.options.Path.path
                pathMaxX = max([max([max([dot[0] for dot in vpath.path]) for vpath in vpaths.paths]) for vpaths in Path])
                pathMinX = min([min([min([dot[0] for dot in vpath.path]) for vpath in vpaths.paths]) for vpaths in Path])
                pathMaxY = max([max([max([dot[1] for dot in vpath.path]) for vpath in vpaths.paths]) for vpaths in Path])
                pathMinY = min([min([min([dot[1] for dot in vpath.path]) for vpath in vpaths.paths]) for vpaths in Path])
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
            self.options.ox = (width/2)-cenx*self.zoom
            self.options.oy = (height/2)+ceny*self.zoom
        self.update()
