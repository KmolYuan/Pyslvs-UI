# -*- coding: utf-8 -*-
from ..QtModules import *
from ..calculation.color import colorlist, colorName
_translate = QCoreApplication.translate

class DynamicCanvas(QWidget):
    mouse_track = pyqtSignal(float, float)
    mouse_getClick = pyqtSignal()
    change_event = pyqtSignal()
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.setMouseTracking(True)
        self.setStatusTip(_translate("MainWindow", "Use mouse wheel or middle button to look around."))
        self.points = {'origin':{'x':self.width()/2, 'y':self.height()/2}, 'rate':2,
            'style':{
                'Background':Qt.white, 'penWidth':{'pen':3, 'path':2},
                'link':Qt.darkGray, 'chain':QColor(226, 219, 190), 'text':Qt.darkGray, 'dimension':False},
            'Path':{'path':list(), 'run_list':list(), 'shaft_list':list(), 'show':True},
            'slvsPath':{'path':list(), 'show':False}, 'currentShaft':0,
            }
        self.Selector = {
            'Drag':{'x':0, 'y':0, 'isDrag':False},
            'Scanner':{'x':0, 'y':0, 'point':0, 'isClose':False}}
        self.reset_Auxline()
        self.Color = colorlist()
        self.re_Color = colorName()
    
    def update_figure(self, width, pathwidth, Point, Line, Chain, Shaft, Slider, Rod,
            table_style, zoom_rate, Font_size, showDimension, Point_mark,
            path, run_list, shaft_list):
        self.Font_size = Font_size
        self.points['style']['dimension'] = showDimension
        self.Point_mark = Point_mark
        self.points['style']['penWidth']['pen'] = width
        self.points['style']['penWidth']['path'] = pathwidth
        self.zoom = float(zoom_rate.replace("%", ""))/100
        self.Point = Point
        self.Line = Line
        self.Chain = Chain
        self.Shaft = Shaft
        self.Slider = Slider
        self.Rod = Rod
        self.table_style = table_style
        self.points['Path']['path'] = path
        self.points['Path']['run_list'] = run_list
        self.points['Path']['shaft_list'] = shaft_list
        self.update()
    
    def path_track(self, path, run_list, shaft_list):
        self.points['Path']['path'] = path
        self.points['Path']['run_list'] = run_list
        self.points['Path']['shaft_list'] = shaft_list
        self.update()
    def path_solving(self, path):
        self.points['slvsPath']['path'] = path
        self.update()
    def changeCurrentShaft(self, pos): self.points['currentShaft'] = pos
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.points['style']['Background']))
        painter.translate(self.points['origin']['x'], self.points['origin']['y'])
        Tp = self.zoom*self.points['rate']
        for i, e in enumerate(self.Chain):
            pen = QPen()
            pen.setWidth(self.points['style']['penWidth']['pen'])
            painter.setBrush(self.points['style']['chain'])
            painter.drawPolygon(
                QPointF(self.Point[e.p1].cx*Tp, self.Point[e.p1].cy*Tp*-1),
                QPointF(self.Point[e.p2].cx*Tp, self.Point[e.p2].cy*Tp*-1),
                QPointF(self.Point[e.p3].cx*Tp, self.Point[e.p3].cy*Tp*-1), fillRule=Qt.OddEvenFill)
            painter.setBrush(Qt.NoBrush)
            if self.Point_mark:
                pen.setColor(self.points['style']['text'])
                painter.setPen(pen)
                painter.setFont(QFont("Arial", self.Font_size))
                text = '[Chain{}]'.format(i)
                if self.points['style']['dimension']: text += ':({:.02f}/{:.02f}/{:.02f})'.format(e.p1p2, e.p2p3, e.p1p3)
                mp = QPointF((self.Point[e.p1].cx+self.Point[e.p2].cx+self.Point[e.p3].cx)*Tp/3,
                    (self.Point[e.p1].cy+self.Point[e.p2].cy+self.Point[e.p3].cy)*Tp*-1/3)
                painter.drawText(mp, text)
        for i, e in enumerate(self.Line):
            start = self.Point[e.start]
            end = self.Point[e.end]
            pen = QPen()
            pen.setWidth(self.points['style']['penWidth']['pen'])
            pen.setColor(self.points['style']['link'])
            painter.setPen(pen)
            painter.drawLine(QPointF(start.cx*Tp, start.cy*Tp*-1), QPointF(end.cx*Tp, end.cy*Tp*-1))
            if self.Point_mark:
                pen.setColor(self.points['style']['text'])
                painter.setPen(pen)
                mp = QPointF((start.cx+end.cx)*Tp/2, (start.cy+end.cy)*Tp*-1/2)
                painter.setFont(QFont('Arial', self.Font_size))
                text = '[Line{}]'.format(i)
                if self.points['style']['dimension']: text += ':{:.02f}'.format(e.len)
                painter.drawText(mp, text)
        for e in self.Slider:
            start = self.Point[e.start]
            end = self.Point[e.end]
            pen = QPen()
            pen.setWidth(self.points['style']['penWidth']['pen'])
            pen.setColor(Qt.darkMagenta)
            painter.setPen(pen)
            painter.drawLine(QPointF(start.cx*Tp, start.cy*Tp*-1), QPointF(end.cx*Tp, end.cy*Tp*-1))
        for e in self.Rod:
            start = self.Point[e.start]
            end = self.Point[e.end]
            pen = QPen()
            pen.setWidth(self.points['style']['penWidth']['pen'])
            pen.setColor(Qt.darkRed)
            painter.setPen(pen)
            painter.drawLine(QPointF(start.cx*Tp, start.cy*Tp*-1), QPointF(end.cx*Tp, end.cy*Tp*-1))
            if self.points['style']['dimension']:
                pen.setColor(self.points['style']['text'])
                painter.setPen(pen)
                mp = QPointF((start.cx*Tp+end.cx*Tp)/2, (start.cy*Tp+end.cy*Tp)/2*-1)
                painter.setFont(QFont("Arial", self.Font_size))
                painter.drawText(mp, '{{{}}}'.format(e['pos']))
        for i, e in enumerate(self.Shaft):
            cen = self.Point[e.cen]
            ref = self.Point[e.ref]
            pen = QPen()
            pen.setWidth(self.points['style']['penWidth']['pen']+2)
            pen.setColor(QColor(225, 140, 0) if i==self.points['currentShaft'] else QColor(175, 90, 0))
            painter.setPen(pen)
            painter.drawLine(QPointF(cen.cx*Tp, cen.cy*Tp*-1), QPointF(ref.cx*Tp, ref.cy*Tp*-1))
        if self.AuxLine['show']:
            pen = QPen(Qt.DashDotLine)
            pen.setColor(self.Color[self.re_Color[self.AuxLine['limit_color']]])
            pen.setWidth(self.points['style']['penWidth']['pen'])
            painter.setPen(pen)
            if self.AuxLine['isMax']:
                if self.AuxLine['Max']['x'] < self.Point[self.AuxLine['pt']].cx: self.AuxLine['Max']['x'] = self.Point[self.AuxLine['pt']].cx
                if self.AuxLine['Max']['y'] < self.Point[self.AuxLine['pt']].cy: self.AuxLine['Max']['y'] = self.Point[self.AuxLine['pt']].cy
                L_point = QPointF(self.width()*4, self.AuxLine['Max']['y']*Tp*(-1))
                R_point = QPointF(self.width()*(-4), self.AuxLine['Max']['y']*Tp*(-1))
                U_point = QPointF(self.AuxLine['Max']['x']*Tp, self.height()*4)
                D_point = QPointF(self.AuxLine['Max']['x']*Tp, self.height()*(-4))
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.points['style']['dimension']:
                    text_center_x = QPointF(self.AuxLine['Max']['x']*Tp+self.points['style']['penWidth']['pen'], self.points['origin']['y']*-1+self.Font_size)
                    text_center_y = QPointF(self.points['origin']['x']*(-1), self.AuxLine['Max']['y']*Tp*-1-self.points['style']['penWidth']['pen'])
                    painter.setFont(QFont("Arial", self.Font_size))
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
                if self.points['style']['dimension']:
                    text_center_x = QPointF(self.AuxLine['Min']['x']*Tp+self.points['style']['penWidth']['pen'], self.points['origin']['y']*-1+self.Font_size)
                    text_center_y = QPointF(self.points['origin']['x']*-1, self.AuxLine['Min']['y']*Tp*-1-self.points['style']['penWidth']['pen'])
                    painter.setFont(QFont("Arial", self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine['Min']['x'])
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine['Min']['y'])
            pen.setColor(self.Color[self.re_Color[self.AuxLine['color']]])
            L_point = QPointF(self.width()*4, self.Point[self.AuxLine['pt']].y*Tp*-1)
            R_point = QPointF(self.width()*-4, self.Point[self.AuxLine['pt']].y*Tp*-1)
            U_point = QPointF(self.Point[self.AuxLine['pt']].x*Tp, self.height()*4)
            D_point = QPointF(self.Point[self.AuxLine['pt']].x*Tp, self.height()*-4)
            painter.setPen(pen)
            if self.AuxLine['horizontal']: painter.drawLine(L_point, R_point)
            if self.AuxLine['vertical']: painter.drawLine(U_point, D_point)
        for i, e in enumerate(self.Point):
            cx = e.cx*Tp
            cy = e.cy*Tp*-1
            pen = QPen()
            pen.setWidth(2)
            if i!=0: pen.setColor(self.Color[self.table_style.cellWidget(i, 3).currentText()])
            else: pen.setColor(self.Color[self.table_style.item(i, 3).text()])
            painter.setPen(pen)
            r = float(self.table_style.item(i, 2).text())
            painter.drawEllipse(QPointF(cx, cy), r, r)
            if i!=0: pen.setColor(self.Color[self.table_style.cellWidget(i, 1).currentText()])
            else: pen.setColor(self.Color[self.table_style.item(i, 1).text()])
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawPoint(QPointF(cx, cy))
            if self.Point_mark:
                pen.setColor(self.points['style']['text'])
                pen.setWidth(2)
                painter.setPen(pen)
                painter.setFont(QFont("Arial", self.Font_size))
                text = '[Point{}]'.format(i)
                if self.points['style']['dimension']: text += ':({:.02f}, {:.02f})'.format(e.cx, e.cy)
                painter.drawText(QPointF(cx+6, cy-6), text)
        if self.points['Path']['path'] and self.points['Path']['show']:
            for i in range(len(self.points['Path']['path'])):
                l = self.points['Path']['path'][i]
                nPath = [[l[i],l[i+1]] for i in range(0,len(l),2)]
                for e in nPath:
                    pointNum = int(self.points['Path']['run_list'][int(nPath.index(e)/len(self.Shaft))].replace('Point', ''))
                    Xs = [x*self.zoom*self.points['rate'] if x!=None else False for x in e[0]]
                    Ys = [y*self.zoom*self.points['rate']*-1 if y!=None else False for y in e[1]]
                    pointPath = QPainterPath()
                    if self.points['Path']['shaft_list'][i]==self.points['currentShaft']:
                        pen.setWidth(self.points['style']['penWidth']['path'])
                        point_color = self.table_style.cellWidget(pointNum, 3).currentText()
                        pen.setColor(self.Color[point_color])
                    else:
                        pen.setWidth(self.points['style']['penWidth']['path'])
                        pen.setColor(self.Color['Gray'])
                    painter.setPen(pen)
                    error = False
                    for x, y in zip(Xs, Ys):
                        if x is False and y is False:
                            error = True
                            continue
                        if (Xs.index(x)==0 and Ys.index(y)==0) or error:
                            error = False
                            pointPath.moveTo(x, y)
                        else: pointPath.lineTo(QPointF(x, y))
                    painter.drawPath(pointPath)
        if self.points['slvsPath']['path'] and self.points['slvsPath']['show']:
            pen.setWidth(self.points['style']['penWidth']['path'])
            pen.setColor(self.Color['Gray'])
            painter.setPen(pen)
            for e in self.points['slvsPath']['path']: painter.drawPoint(QPointF(e['x']*self.zoom*self.points['rate'], e['y']*self.zoom*self.points['rate']*(-1)))
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
            self.Selector['Drag']['x'] = event.x()-self.points['origin']['x']
            self.Selector['Drag']['y'] = event.y()-self.points['origin']['y']
            self.Selector['Drag']['isDrag'] = True
        elif QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.Selector['Drag']['x'] = 0
            self.Selector['Drag']['y'] = 0
            self.Selector['Drag']['isDrag'] = True
    def mouseReleaseEvent(self, event): self.Selector['Drag']['isDrag'] = False
    def mouseDoubleClickEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.points['origin']['x'] = event.x()
            self.points['origin']['y'] = event.y()
            self.update()
        if event.button()==Qt.MidButton: self.SetIn()
        if QApplication.keyboardModifiers()==Qt.AltModifier: self.mouse_getClick.emit()
    def mouseMoveEvent(self, event):
        if self.Selector['Drag']['isDrag']:
            self.points['origin']['x'] = event.x()-self.Selector['Drag']['x']
            self.points['origin']['y'] = event.y()-self.Selector['Drag']['y']
            self.update()
        self.Selector['Scanner']['x'] = round((event.x()-self.points['origin']['x'])/self.zoom/self.points['rate'], 2)
        self.Selector['Scanner']['y'] = round((event.y()-self.points['origin']['y'])*(-1)/self.zoom/self.points['rate'], 2)
        self.mouse_track.emit(self.Selector['Scanner']['x'], self.Selector['Scanner']['y'])
        if QApplication.keyboardModifiers()==Qt.AltModifier: self.setCursor(Qt.CrossCursor)
        else: self.setCursor(Qt.ArrowCursor)
    
    def SetIn(self):
        self.points['origin']['x'] = self.width()/2
        self.points['origin']['y'] = self.height()/2
        self.update()
