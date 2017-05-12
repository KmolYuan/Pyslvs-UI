# -*- coding: utf-8 -*-
from ..QtModules import *
from ..graphics.color import colorlist, colorName
_translate = QCoreApplication.translate

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
        self.show = True
        self.mode = True

class DynamicCanvas(QWidget):
    mouse_track = pyqtSignal(float, float)
    mouse_getClick = pyqtSignal()
    change_event = pyqtSignal()
    zoom_change = pyqtSignal(int)
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStatusTip(_translate("MainWindow", "Use mouse wheel or middle button to look around."))
        self.options = PointOptions(self.width(), self.height())
        self.Selector = Selector()
        self.reset_Auxline()
        self.Color = colorlist()
        self.re_Color = colorName()
    
    def update_figure(self, width, pathwidth, Point, Line, Chain, Shaft, Slider, Rod,
            zoom_rate, Font_size, showDimension, Point_mark, path):
        self.Font_size = Font_size
        self.options.style['dimension'] = showDimension
        self.Point_mark = Point_mark
        self.options.style['penWidth']['pen'] = width
        self.options.style['penWidth']['path'] = pathwidth
        self.zoom = float(zoom_rate.replace("%", ""))/100
        self.Point = Point
        self.Line = Line
        self.Chain = Chain
        self.Shaft = Shaft
        self.Slider = Slider
        self.Rod = Rod
        self.options.Path.path = path
        self.update()
    
    def path_solving(self, path=list()):
        self.options.slvsPath['path'] = path
        self.update()
    def changeCurrentShaft(self, pos=0): self.options.currentShaft = pos
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.options.style['Background']))
        painter.translate(self.options.origin['x'], self.options.origin['y'])
        Tp = self.zoom*self.options.rate
        for i, e in enumerate(self.Line):
            start = self.Point[e.start]
            end = self.Point[e.end]
            pen = QPen()
            pen.setWidth(self.options.style['penWidth']['pen'])
            pen.setColor(self.options.style['link'])
            painter.setPen(pen)
            painter.drawLine(QPointF(start.cx*Tp, start.cy*Tp*-1), QPointF(end.cx*Tp, end.cy*Tp*-1))
            if self.Point_mark:
                pen.setColor(self.options.style['text'])
                painter.setPen(pen)
                mp = QPointF((start.cx+end.cx)*Tp/2, (start.cy+end.cy)*Tp*-1/2)
                painter.setFont(QFont('Arial', self.Font_size))
                text = '[Line{}]'.format(i)
                if self.options.style['dimension']: text += ':{:.02f}'.format(e.len)
                painter.drawText(mp, text)
        for i, e in enumerate(self.Chain):
            pen = QPen()
            pen.setWidth(self.options.style['penWidth']['pen'])
            pen.setColor(self.options.style['link'])
            painter.setBrush(self.options.style['chain'])
            painter.drawPolygon(
                QPointF(self.Point[e.p1].cx*Tp, self.Point[e.p1].cy*Tp*-1),
                QPointF(self.Point[e.p2].cx*Tp, self.Point[e.p2].cy*Tp*-1),
                QPointF(self.Point[e.p3].cx*Tp, self.Point[e.p3].cy*Tp*-1))
            painter.setBrush(Qt.NoBrush)
            if self.Point_mark:
                pen.setColor(self.options.style['text'])
                painter.setPen(pen)
                painter.setFont(QFont('Arial', self.Font_size))
                text = '[Chain{}]'.format(i)
                if self.options.style['dimension']: text += ':({:.02f}/{:.02f}/{:.02f})'.format(e.p1p2, e.p2p3, e.p1p3)
                mp = QPointF((self.Point[e.p1].cx+self.Point[e.p2].cx+self.Point[e.p3].cx)*Tp/3,
                    (self.Point[e.p1].cy+self.Point[e.p2].cy+self.Point[e.p3].cy)*Tp*-1/3)
                painter.drawText(mp, text)
        for e in self.Slider:
            start = self.Point[e.start]
            end = self.Point[e.end]
            pen = QPen()
            pen.setWidth(self.options.style['penWidth']['pen'])
            pen.setColor(Qt.darkMagenta)
            painter.setPen(pen)
            painter.drawLine(QPointF(start.cx*Tp, start.cy*Tp*-1), QPointF(end.cx*Tp, end.cy*Tp*-1))
        for e in self.Rod:
            start = self.Point[e.start]
            end = self.Point[e.end]
            pen = QPen()
            pen.setWidth(self.options.style['penWidth']['pen'])
            pen.setColor(Qt.darkRed)
            painter.setPen(pen)
            painter.drawLine(QPointF(start.cx*Tp, start.cy*Tp*-1), QPointF(end.cx*Tp, end.cy*Tp*-1))
            if self.options.style['dimension']:
                pen.setColor(self.options.style['text'])
                painter.setPen(pen)
                mp = QPointF((start.cx*Tp+end.cx*Tp)/2, (start.cy*Tp+end.cy*Tp)/2*-1)
                painter.setFont(QFont('Arial', self.Font_size))
                painter.drawText(mp, '{{{}}}'.format(e['pos']))
        for i, e in enumerate(self.Shaft):
            cen = self.Point[e.cen]
            ref = self.Point[e.ref]
            pen = QPen()
            pen.setWidth(self.options.style['penWidth']['pen']+2)
            pen.setColor(QColor(225, 140, 0) if i==self.options.currentShaft else QColor(175, 90, 0))
            painter.setPen(pen)
            painter.drawLine(QPointF(cen.cx*Tp, cen.cy*Tp*-1), QPointF(ref.cx*Tp, ref.cy*Tp*-1))
        if self.AuxLine['show']:
            pen = QPen(Qt.DashDotLine)
            pen.setColor(self.Color[self.re_Color[self.AuxLine['limit_color']]])
            pen.setWidth(self.options.style['penWidth']['pen'])
            painter.setPen(pen)
            if self.AuxLine['isMax']:
                if self.AuxLine['Max']['x'] < self.Point[self.AuxLine['pt']].cx: self.AuxLine['Max']['x'] = self.Point[self.AuxLine['pt']].cx
                if self.AuxLine['Max']['y'] < self.Point[self.AuxLine['pt']].cy: self.AuxLine['Max']['y'] = self.Point[self.AuxLine['pt']].cy
                L_point = QPointF(self.width()*4, self.AuxLine['Max']['y']*Tp*(-1))
                R_point = QPointF(self.width()*(-4), self.AuxLine['Max']['y']*Tp*(-1))
                U_point = QPointF(self.AuxLine['Max']['x']*Tp, self.height()*4)
                D_point = QPointF(self.AuxLine['Max']['x']*Tp, self.height()*-4)
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.options.style['dimension']:
                    text_center_x = QPointF(self.AuxLine['Max']['x']*Tp+self.options.style['penWidth']['pen'], self.options.origin['y']*-1+self.Font_size)
                    text_center_y = QPointF(self.options.origin['x']*(-1), self.AuxLine['Max']['y']*Tp*-1-self.options.style['penWidth']['pen'])
                    painter.setFont(QFont('Arial', self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine['Max']['x'])
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine['Max']['y'])
            if self.AuxLine['isMin']:
                if self.AuxLine['Min']['x'] > self.Point[self.AuxLine['pt']].cx: self.AuxLine['Min']['x'] = self.Point[self.AuxLine['pt']].cx
                if self.AuxLine['Min']['y'] > self.Point[self.AuxLine['pt']].cy: self.AuxLine['Min']['y'] = self.Point[self.AuxLine['pt']].cy
                L_point = QPointF(self.width()*4, self.AuxLine['Min']['y']*Tp*-1)
                R_point = QPointF(self.width()*(-4), self.AuxLine['Min']['y']*Tp*-1)
                U_point = QPointF(self.AuxLine['Min']['x']*Tp, self.height()*4)
                D_point = QPointF(self.AuxLine['Min']['x']*Tp, self.height()*-4)
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.options.style['dimension']:
                    text_center_x = QPointF(self.AuxLine['Min']['x']*Tp+self.options.style['penWidth']['pen'], self.options.origin['y']*-1+self.Font_size)
                    text_center_y = QPointF(self.options.origin['x']*-1, self.AuxLine['Min']['y']*Tp*-1-self.options.style['penWidth']['pen'])
                    painter.setFont(QFont('Arial', self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine['Min']['x'])
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine['Min']['y'])
            pen.setColor(self.Color[self.re_Color[self.AuxLine['color']]])
            L_point = QPointF(self.width()*4, self.Point[self.AuxLine['pt']].cy*Tp*-1)
            R_point = QPointF(self.width()*-4, self.Point[self.AuxLine['pt']].cy*Tp*-1)
            U_point = QPointF(self.Point[self.AuxLine['pt']].cx*Tp, self.height()*4)
            D_point = QPointF(self.Point[self.AuxLine['pt']].cx*Tp, self.height()*-4)
            painter.setPen(pen)
            if self.AuxLine['horizontal']: painter.drawLine(L_point, R_point)
            if self.AuxLine['vertical']: painter.drawLine(U_point, D_point)
        for i, e in enumerate(self.Point):
            cx = e.cx*Tp
            cy = e.cy*Tp*-1
            pen = QPen()
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
            pen.setWidth(self.options.style['penWidth']['path'])
            pen.setColor(self.Color['Gray'])
            painter.setPen(pen)
            for e in self.options.slvsPath['path']: painter.drawPoint(QPointF(e['x']*self.zoom*self.options.rate, e['y']*self.zoom*self.options.rate*(-1)))
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
            diffX = max(Xs)-min(Xs)
            diffY = max(Ys)-min(Ys)
            event = diffX/diffY > width/height
            self.zoom_change.emit(int((width if event else height)/((diffX if event else diffY)+3)*50))
            Tp = self.zoom*self.options.rate
            cenx = (min(Xs)+max(Xs))/2
            ceny = (min(Ys)+max(Ys))/2
            self.options.origin['x'] = (width/2)-cenx*Tp
            self.options.origin['y'] = (height/2)+ceny*Tp
        self.update()
