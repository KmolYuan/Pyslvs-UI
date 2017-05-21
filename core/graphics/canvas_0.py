# -*- coding: utf-8 -*-
from ..QtModules import *
from ..graphics.color import colorlist, colorName
_translate = QCoreApplication.translate

class PointOptions:
    def __init__(self, width, height):
        self.origin = {'x':width/2, 'y':height/2}
        self.rate = 2
        self.style = {
            'Background':Qt.white, 'penWidth':{'pen':3, 'path':2},
            'link':Qt.darkGray, 'chain':QColor(226, 219, 190), 'text':Qt.darkGray, 'dimension':False}
        self.Path = Path()
        self.slvsPath = {'path':list(), 'show':False}
        self.currentShaft = 0

class Path:
    def __init__(self):
        self.path = list()
        self.demo = 0.
        self.show = True
        self.mode = True
        self.Drivemode = False

class Selector:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._isDrag = False
    @property
    def x(self): return self._x
    @x.setter
    def x(self, x): self._x = x
    @property
    def y(self): return self._y
    @y.setter
    def y(self, y): self._y = y
    @property
    def isDrag(self): return self._isDrag
    @isDrag.setter
    def isDrag(self, isDrag): self._isDrag = isDrag

class DynamicCanvas(QWidget):
    mouse_track = pyqtSignal(float, float)
    mouse_getClick = pyqtSignal()
    change_event = pyqtSignal()
    zoom_change = pyqtSignal(int)
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStatusTip(_translate("DynamicCanvas", "Use mouse wheel or middle button to look around."))
        self.options = PointOptions(self.width(), self.height())
        self.Selector = Selector()
        self.reset_Auxline()
        self.Color = colorlist()
        self.re_Color = colorName()
    
    def changePathCurrentShaft(self):
        if self.Shaft: self.options.Path.demo = self.Shaft[self.options.currentShaft].demo
    def changeCurrentShaft(self, pos=0):
        self.options.currentShaft = pos
        self.update()
    
    def path_solving(self, path=list()):
        self.options.slvsPath['path'] = path
        self.update()
    
    def update_figure(self, width, pathwidth, Point, Line, Chain, Shaft, Slider, Rod,
            zoom_rate, Font_size, showDimension, Point_mark, path):
        self.Font_size = Font_size
        self.options.style['dimension'] = showDimension
        self.Point_mark = Point_mark
        self.options.style['penWidth']['pen'] = width
        self.options.style['penWidth']['path'] = pathwidth
        self.zoom = zoom_rate/100
        self.Point = Point
        self.Line = Line
        self.Chain = Chain
        self.Shaft = Shaft
        self.Slider = Slider
        self.Rod = Rod
        self.options.Path.path = path
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.options.style['Background']))
        painter.translate(self.options.origin['x'], self.options.origin['y'])
        Tp = self.zoom*self.options.rate
        pen = QPen()
        pathShaft = None
        if self.options.Path.path and self.options.Path.Drivemode:
            for vpaths in self.options.Path.path:
                if vpaths.shaft==self.options.currentShaft: pathShaft = vpaths
        if not pathShaft==None:
            shaft = self.Shaft[pathShaft.shaft]
            resolution = abs(shaft.end-shaft.start)/(len(pathShaft.paths[0].path)-1)
            resolutionIndex = int(round(self.options.Path.demo/resolution))
            Points = {e.point:e for e in pathShaft.paths}
            for i, e in enumerate(self.Chain):
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(self.options.style['link'])
                painter.setBrush(self.options.style['chain'])
                p1x = (self.Point[e.p1].cx if self.Point[e.p1].fix else Points[e.p1].path[resolutionIndex][0])*Tp
                p1y = (self.Point[e.p1].cy if self.Point[e.p1].fix else Points[e.p1].path[resolutionIndex][1])*Tp*-1
                p2x = (self.Point[e.p2].cx if self.Point[e.p2].fix else Points[e.p2].path[resolutionIndex][0])*Tp
                p2y = (self.Point[e.p2].cy if self.Point[e.p2].fix else Points[e.p2].path[resolutionIndex][1])*Tp*-1
                p3x = (self.Point[e.p3].cx if self.Point[e.p3].fix else Points[e.p3].path[resolutionIndex][0])*Tp
                p3y = (self.Point[e.p3].cy if self.Point[e.p3].fix else Points[e.p3].path[resolutionIndex][1])*Tp*-1
                painter.drawPolygon(QPointF(p1x, p1y), QPointF(p2x, p2y), QPointF(p3x, p3y))
                painter.setBrush(Qt.NoBrush)
                if self.Point_mark:
                    pen.setColor(self.options.style['text'])
                    painter.setPen(pen)
                    painter.setFont(QFont('Arial', self.Font_size))
                    text = '[Chain{}]'.format(i)
                    if self.options.style['dimension']: text += ':({:.02f}/{:.02f}/{:.02f})'.format(e.p1p2, e.p2p3, e.p1p3)
                    mp = QPointF((p1x+p2x+p3x)/3, (p1y+p2y+p3y)/3)
                    painter.drawText(mp, text)
            for i, e in enumerate(self.Line):
                p1x = (self.Point[e.start].cx if self.Point[e.start].fix else Points[e.start].path[resolutionIndex][0])*Tp
                p1y = (self.Point[e.start].cy if self.Point[e.start].fix else Points[e.start].path[resolutionIndex][1])*Tp*-1
                p2x = (self.Point[e.end].cx if self.Point[e.end].fix else Points[e.end].path[resolutionIndex][0])*Tp
                p2y = (self.Point[e.end].cy if self.Point[e.end].fix else Points[e.end].path[resolutionIndex][1])*Tp*-1
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(self.options.style['link'])
                painter.setPen(pen)
                painter.drawLine(QPointF(p1x, p1y), QPointF(p2x, p2y))
                if self.Point_mark:
                    pen.setColor(self.options.style['text'])
                    painter.setPen(pen)
                    mp = QPointF((p1x+p2x)/2, (p1y+p2y)/2)
                    painter.setFont(QFont('Arial', self.Font_size))
                    text = '[Line{}]'.format(i)
                    if self.options.style['dimension']: text += ':{:.02f}'.format(e.len)
                    painter.drawText(mp, text)
            for e in self.Slider:
                p1x = (self.Point[e.start].cx if self.Point[e.start].fix else Points[e.start].path[resolutionIndex][0])*Tp
                p1y = (self.Point[e.start].cy if self.Point[e.start].fix else Points[e.start].path[resolutionIndex][1])*Tp*-1
                p2x = (self.Point[e.end].cx if self.Point[e.end].fix else Points[e.end].path[resolutionIndex][0])*Tp
                p2y = (self.Point[e.end].cy if self.Point[e.end].fix else Points[e.end].path[resolutionIndex][1])*Tp*-1
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(Qt.darkMagenta)
                painter.setPen(pen)
                painter.drawLine(QPointF(p1x, p1y), QPointF(p2x, p2y))
            for e in self.Rod:
                p1x = (self.Point[e.start].cx if self.Point[e.start].fix else Points[e.start].path[resolutionIndex][0])*Tp
                p1y = (self.Point[e.start].cy if self.Point[e.start].fix else Points[e.start].path[resolutionIndex][1])*Tp*-1
                p2x = (self.Point[e.end].cx if self.Point[e.end].fix else Points[e.end].path[resolutionIndex][0])*Tp
                p2y = (self.Point[e.end].cy if self.Point[e.end].fix else Points[e.end].path[resolutionIndex][1])*Tp*-1
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(Qt.darkRed)
                painter.setPen(pen)
                painter.drawLine(QPointF(p1x, p1y), QPointF(p2x, p2y))
                if self.options.style['dimension']:
                    pen.setColor(self.options.style['text'])
                    painter.setPen(pen)
                    mp = QPointF((p1x+p2x)/2, (p1y+p2y)/2)
                    painter.setFont(QFont('Arial', self.Font_size))
                    painter.drawText(mp, '{{{}}}'.format(e['pos']))
            for i, e in enumerate(self.Shaft):
                p1x = (self.Point[e.cen].cx if self.Point[e.cen].fix else Points[e.cen].path[resolutionIndex][0])*Tp
                p1y = (self.Point[e.cen].cy if self.Point[e.cen].fix else Points[e.cen].path[resolutionIndex][1])*Tp*-1
                p2x = (self.Point[e.ref].cx if self.Point[e.ref].fix else Points[e.ref].path[resolutionIndex][0])*Tp
                p2y = (self.Point[e.ref].cy if self.Point[e.ref].fix else Points[e.ref].path[resolutionIndex][1])*Tp*-1
                pen.setWidth(self.options.style['penWidth']['pen']+2)
                pen.setColor(QColor(225, 140, 0) if i==self.options.currentShaft else QColor(175, 90, 0))
                painter.setPen(pen)
                painter.drawLine(QPointF(p1x, p1y), QPointF(p2x, p2y))
            if self.AuxLine['show']:
                Auxpen = QPen(Qt.DashDotLine)
                Auxpen.setColor(self.Color[self.re_Color[self.AuxLine['limit_color']]])
                Auxpen.setWidth(self.options.style['penWidth']['pen'])
                painter.setPen(Auxpen)
                x = (self.Point[self.AuxLine['pt']].cx if self.Point[self.AuxLine['pt']].fix else Points[self.AuxLine['pt']].path[resolutionIndex][0])
                y = (self.Point[self.AuxLine['pt']].cy if self.Point[self.AuxLine['pt']].fix else Points[self.AuxLine['pt']].path[resolutionIndex][1])
                for status in ['Max', 'Min']:
                    if self.AuxLine['is'+status]:
                        if status=='Max':
                            if self.AuxLine['Max']['x']<x: self.AuxLine['Max']['x'] = x
                            if self.AuxLine['Max']['y']<y: self.AuxLine['Max']['y'] = y
                        else:
                            if self.AuxLine['Min']['x']>x: self.AuxLine['Min']['x'] = x
                            if self.AuxLine['Min']['y']>y: self.AuxLine['Min']['y'] = y
                        L_point = QPointF(self.width()*4, self.AuxLine[status]['y']*Tp*-1)
                        R_point = QPointF(self.width()*-4, self.AuxLine[status]['y']*Tp*-1)
                        U_point = QPointF(self.AuxLine[status]['x']*Tp, self.height()*4)
                        D_point = QPointF(self.AuxLine[status]['x']*Tp, self.height()*-4)
                        painter.drawLine(L_point, R_point)
                        painter.drawLine(U_point, D_point)
                        if self.options.style['dimension']:
                            text_center_x = QPointF(self.AuxLine[status]['x']*Tp+self.options.style['penWidth']['pen'], self.options.origin['y']*-1+self.Font_size)
                            text_center_y = QPointF(self.options.origin['x']*-1, self.AuxLine[status]['y']*Tp*-1-self.options.style['penWidth']['pen'])
                            painter.setFont(QFont('Arial', self.Font_size))
                            painter.drawText(text_center_x, '{:.6f}'.format(self.AuxLine[status]['x']))
                            painter.drawText(text_center_y, '{:.6f}'.format(self.AuxLine[status]['y']))
                pen.setColor(self.Color[self.re_Color[self.AuxLine['color']]])
                L_point = QPointF(self.width()*4, y*Tp*-1)
                R_point = QPointF(self.width()*-4, y*Tp*-1)
                U_point = QPointF(x*Tp, self.height()*4)
                D_point = QPointF(x*Tp, self.height()*-4)
                painter.setPen(pen)
                if self.AuxLine['horizontal']: painter.drawLine(L_point, R_point)
                if self.AuxLine['vertical']: painter.drawLine(U_point, D_point)
            for path in pathShaft.paths:
                x = path.path[resolutionIndex][0]*Tp
                y = path.path[resolutionIndex][1]*Tp*-1
                pen.setWidth(2)
                pen.setColor(self.Color[self.Point[path.point].color])
                painter.setPen(pen)
                r = 10. if self.Point[path.point].fix else 5.
                painter.drawEllipse(QPointF(x, y), r, r)
                pen.setWidth(5)
                painter.setPen(pen)
                painter.drawPoint(QPointF(x, y))
                if self.Point_mark:
                    pen.setColor(self.options.style['text'])
                    pen.setWidth(2)
                    painter.setPen(pen)
                    painter.setFont(QFont('Arial', self.Font_size))
                    text = '[Point{}]'.format(path.point)
                    if self.options.style['dimension']: text += ':({:.02f}, {:.02f})'.format(x/Tp, y/Tp*-1)
                    painter.drawText(QPointF(x+6, y-6), text)
            for i, e in enumerate(self.Point):
                if i in Points: continue
                cx = e.cx*Tp
                cy = e.cy*Tp*-1
                pen.setWidth(2)
                pen.setColor(self.Color[e.color])
                painter.setPen(pen)
                r = 10. if e.fix else 5.
                painter.drawEllipse(QPointF(cx, cy), r, r)
                pen.setWidth(5)
                painter.setPen(pen)
                painter.drawPoint(QPointF(cx, cy))
                if self.Point_mark:
                    pen.setColor(self.options.style['text'])
                    pen.setWidth(2)
                    painter.setPen(pen)
                    painter.setFont(QFont('Arial', self.Font_size))
                    text = '[Point{}]'.format(i)
                    if self.options.style['dimension']: text += ':({:.02f}, {:.02f})'.format(e.cx, e.cy)
                    painter.drawText(QPointF(cx+6, cy-6), text)
        else:
            for i, e in enumerate(self.Chain):
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(self.options.style['link'])
                painter.setBrush(self.options.style['chain'])
                p1x = self.Point[e.p1].cx*Tp
                p1y = self.Point[e.p1].cy*Tp*-1
                p2x = self.Point[e.p2].cx*Tp
                p2y = self.Point[e.p2].cy*Tp*-1
                p3x = self.Point[e.p3].cx*Tp
                p3y = self.Point[e.p3].cy*Tp*-1
                painter.drawPolygon(QPointF(p1x, p1y), QPointF(p2x, p2y), QPointF(p3x, p3y))
                painter.setBrush(Qt.NoBrush)
                if self.Point_mark:
                    pen.setColor(self.options.style['text'])
                    painter.setPen(pen)
                    painter.setFont(QFont('Arial', self.Font_size))
                    text = '[Chain{}]'.format(i)
                    if self.options.style['dimension']: text += ':({:.02f}/{:.02f}/{:.02f})'.format(e.p1p2, e.p2p3, e.p1p3)
                    mp = QPointF((p1x+p2x+p3x)/3, (p1y+p2y+p3y)/3)
                    painter.drawText(mp, text)
            for i, e in enumerate(self.Line):
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(self.options.style['link'])
                painter.setPen(pen)
                p1x = self.Point[e.start].cx*Tp
                p1y = self.Point[e.start].cy*Tp*-1
                p2x = self.Point[e.end].cx*Tp
                p2y = self.Point[e.end].cy*Tp*-1
                painter.drawLine(QPointF(p1x, p1y), QPointF(p2x, p2y))
                if self.Point_mark:
                    pen.setColor(self.options.style['text'])
                    painter.setPen(pen)
                    mp = QPointF((p1x+p2x)/2, (p1y+p2y)/2)
                    painter.setFont(QFont('Arial', self.Font_size))
                    text = '[Line{}]'.format(i)
                    if self.options.style['dimension']: text += ':{:.02f}'.format(e.len)
                    painter.drawText(mp, text)
            for e in self.Slider:
                p1x = self.Point[e.start].cx*Tp
                p1y = self.Point[e.start].cy*Tp*-1
                p2x = self.Point[e.end].cx*Tp
                p2y = self.Point[e.end].cy*Tp*-1
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(Qt.darkMagenta)
                painter.setPen(pen)
                painter.drawLine(QPointF(p1x, p1y), QPointF(p2x, p2y))
            for e in self.Rod:
                p1x = self.Point[e.start].cx*Tp
                p1y = self.Point[e.start].cy*Tp*-1
                p2x = self.Point[e.end].cx*Tp
                p2y = self.Point[e.end].cy*Tp*-1
                pen.setWidth(self.options.style['penWidth']['pen'])
                pen.setColor(Qt.darkRed)
                painter.setPen(pen)
                painter.drawLine(QPointF(p1x, p1y), QPointF(p2x, p2y))
                if self.options.style['dimension']:
                    pen.setColor(self.options.style['text'])
                    painter.setPen(pen)
                    mp = QPointF((p1x+p2x)/2, (p1y+p2y)/2)
                    painter.setFont(QFont('Arial', self.Font_size))
                    painter.drawText(mp, '{{{}}}'.format(e['pos']))
            for i, e in enumerate(self.Shaft):
                p1x = self.Point[e.cen].cx*Tp
                p1y = self.Point[e.cen].cy*Tp*-1
                p2x = self.Point[e.ref].cx*Tp
                p2y = self.Point[e.ref].cy*Tp*-1
                pen.setWidth(self.options.style['penWidth']['pen']+2)
                pen.setColor(QColor(225, 140, 0) if i==self.options.currentShaft else QColor(175, 90, 0))
                painter.setPen(pen)
                painter.drawLine(QPointF(p1x, p1y), QPointF(p2x, p2y))
            if self.AuxLine['show']:
                Auxpen = QPen(Qt.DashDotLine)
                Auxpen.setColor(self.Color[self.re_Color[self.AuxLine['limit_color']]])
                Auxpen.setWidth(self.options.style['penWidth']['pen'])
                painter.setPen(Auxpen)
                x = self.Point[self.AuxLine['pt']].cx
                y = self.Point[self.AuxLine['pt']].cy
                for status in ['Max', 'Min']:
                    if self.AuxLine['is'+status]:
                        if status=='Max':
                            if self.AuxLine['Max']['x']<x: self.AuxLine['Max']['x'] = x
                            if self.AuxLine['Max']['y']<y: self.AuxLine['Max']['y'] = y
                        else:
                            if self.AuxLine['Min']['x']>x: self.AuxLine['Min']['x'] = x
                            if self.AuxLine['Min']['y']>y: self.AuxLine['Min']['y'] = y
                        L_point = QPointF(self.width()*4, self.AuxLine[status]['y']*Tp*-1)
                        R_point = QPointF(self.width()*-4, self.AuxLine[status]['y']*Tp*-1)
                        U_point = QPointF(self.AuxLine[status]['x']*Tp, self.height()*4)
                        D_point = QPointF(self.AuxLine[status]['x']*Tp, self.height()*-4)
                        painter.drawLine(L_point, R_point)
                        painter.drawLine(U_point, D_point)
                        if self.options.style['dimension']:
                            text_center_x = QPointF(self.AuxLine[status]['x']*Tp+self.options.style['penWidth']['pen'], self.options.origin['y']*-1+self.Font_size)
                            text_center_y = QPointF(self.options.origin['x']*-1, self.AuxLine[status]['y']*Tp*-1-self.options.style['penWidth']['pen'])
                            painter.setFont(QFont('Arial', self.Font_size))
                            painter.drawText(text_center_x, '{:.6f}'.format(self.AuxLine[status]['x']))
                            painter.drawText(text_center_y, '{:.6f}'.format(self.AuxLine[status]['y']))
                pen.setColor(self.Color[self.re_Color[self.AuxLine['color']]])
                L_point = QPointF(self.width()*4, y*Tp*-1)
                R_point = QPointF(self.width()*-4, y*Tp*-1)
                U_point = QPointF(x*Tp, self.height()*4)
                D_point = QPointF(x*Tp, self.height()*-4)
                painter.setPen(pen)
                if self.AuxLine['horizontal']: painter.drawLine(L_point, R_point)
                if self.AuxLine['vertical']: painter.drawLine(U_point, D_point)
            for i, e in enumerate(self.Point):
                cx = e.cx*Tp
                cy = e.cy*Tp*-1
                pen.setWidth(2)
                pen.setColor(self.Color[e.color])
                painter.setPen(pen)
                r = 10. if e.fix else 5.
                painter.drawEllipse(QPointF(cx, cy), r, r)
                pen.setWidth(5)
                painter.setPen(pen)
                painter.drawPoint(QPointF(cx, cy))
                if self.Point_mark:
                    pen.setColor(self.options.style['text'])
                    pen.setWidth(2)
                    painter.setPen(pen)
                    painter.setFont(QFont('Arial', self.Font_size))
                    text = '[Point{}]'.format(i)
                    if self.options.style['dimension']: text += ':({:.02f}, {:.02f})'.format(e.cx, e.cy)
                    painter.drawText(QPointF(cx+6, cy-6), text)
        if self.options.Path.path and self.options.Path.show:
            for vpaths in self.options.Path.path:
                for vpath in vpaths.paths:
                    if vpath.show:
                        if vpaths.shaft==self.options.currentShaft:
                            pen.setWidth(self.options.style['penWidth']['path'])
                            pen.setColor(self.Color[self.Point[vpath.point].color])
                        else:
                            pen.setWidth(self.options.style['penWidth']['path'])
                            pen.setColor(self.Color['Gray'])
                        painter.setPen(pen)
                        if self.options.Path.mode==True:
                            error = False
                            pointPath = QPainterPath()
                            for i, point in enumerate(vpath.path):
                                if point[0] is None or point[0] is False:
                                    error = True
                                    continue
                                x = point[0]*Tp
                                y = point[1]*Tp*-1
                                if i==0 or error:
                                    pointPath.moveTo(x, y)
                                    error = False
                                else: pointPath.lineTo(QPointF(x, y))
                            painter.drawPath(pointPath)
                        else:
                            for i, point in enumerate(vpath.path):
                                if point[0] is None or point[0] is False: continue
                                x = point[0]*Tp
                                y = point[1]*Tp*-1
                                painter.drawPoint(QPointF(x, y))
        if self.options.slvsPath['path'] and self.options.slvsPath['show']:
            pathData = self.options.slvsPath['path']
            pen.setWidth(self.options.style['penWidth']['path'])
            pen.setColor(self.Color['Gray'])
            painter.setPen(pen)
            if self.options.Path.mode==True:
                if len(pathData)>1:
                    pointPath = QPainterPath()
                    for i, e in enumerate(pathData):
                        x = e['x']*Tp
                        y = e['y']*Tp*-1
                        if i==0: pointPath.moveTo(x, y)
                        else: pointPath.lineTo(QPointF(x, y))
                    painter.drawPath(pointPath)
                elif len(pathData)==1: painter.drawPoint(QPointF(pathData[0]['x']*Tp, pathData[0]['y']*Tp*-1))
            else:
                for i, e in enumerate(pathData):
                    x = e['x']*Tp
                    y = e['y']*Tp*-1
                    painter.drawPoint(QPointF(x, y))
        painter.end()
        self.change_event.emit()
    
    def Reset_Aux_limit(self):
        self.AuxLine['Max']['x'] = self.Point[self.AuxLine['pt']].cx
        self.AuxLine['Max']['y'] = self.Point[self.AuxLine['pt']].cy
        self.AuxLine['Min']['x'] = self.Point[self.AuxLine['pt']].cx
        self.AuxLine['Min']['y'] = self.Point[self.AuxLine['pt']].cy
    
    def reset_Auxline(self):
        self.AuxLine = {'show':False, 'pt':0,
            'horizontal':True, 'vertical':True, 'isMax':True, 'isMin':True,
            'color':6, 'limit_color':8,
            'Max':{'x':0, 'y':0}, 'Min':{'x':0, 'y':0}}
    
    def mousePressEvent(self, event):
        if event.buttons()==Qt.MiddleButton:
            self.Selector.x = event.x()-self.options.origin['x']
            self.Selector.y = event.y()-self.options.origin['y']
            self.Selector.isDrag = True
        elif QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.Selector.x = 0
            self.Selector.y = 0
            self.Selector.isDrag = True
    def mouseReleaseEvent(self, event): self.Selector.isDrag = False
    def mouseDoubleClickEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.options.origin['x'] = event.x()
            self.options.origin['y'] = event.y()
            self.update()
        if event.button()==Qt.MidButton: self.SetIn()
        if QApplication.keyboardModifiers()==Qt.AltModifier: self.mouse_getClick.emit()
    def mouseMoveEvent(self, event):
        if self.Selector.isDrag:
            self.options.origin['x'] = event.x()-self.Selector.x
            self.options.origin['y'] = event.y()-self.Selector.y
            self.update()
        self.mouse_track.emit(
            round((event.x()-self.options.origin['x'])/self.zoom/self.options.rate, 2),
            -round((event.y()-self.options.origin['y'])/self.zoom/self.options.rate, 2))
        if QApplication.keyboardModifiers()==Qt.AltModifier: self.setCursor(Qt.CrossCursor)
        else: self.setCursor(Qt.ArrowCursor)
    
    def SetIn(self):
        width = self.width()
        height = self.height()
        if len(self.Point)==1:
            self.zoom_change.emit(200)
            self.options.origin['x'] = width/2
            self.options.origin['y'] = height/2
        else:
            Xs = [e.cx for e in self.Point]
            Ys = [e.cy for e in self.Point]
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
            event = diffX/diffY > width/height
            self.zoom_change.emit(int((width if event else height)/((diffX if event else diffY))*0.95*50))
            Tp = self.zoom*self.options.rate
            self.options.origin['x'] = (width/2)-cenx*Tp
            self.options.origin['y'] = (height/2)+ceny*Tp
        self.update()
