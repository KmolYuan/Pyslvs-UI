# -*- coding: utf-8 -*-
from .modules import *
from .color import colorlist, colorName

class DynamicCanvas(QWidget):
    mouse_track = pyqtSignal(float, float)
    change_event = pyqtSignal()
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMouseTracking(True)
        self.points = {
            'x':[], 'y':[], 'origin':{'x':self.width()/2, 'y':self.height()/2}, 'rate':2,
            'style':{
                'Background':Qt.white, 'penWidth':{'pen':2, 'path':1},
                'pt':Qt.green, 'link':Qt.darkGray, 'chain':Qt.cyan, 'text':Qt.darkGray,
                'dimension':False,
                },
            'Path':{'path':[], 'run_list':[], 'shaft_list':[], 'show':True},
            }
        self.Selector = {
            'Drag':{'x':0, 'y':0, 'isDrag':False},
            'Scanner':{'x':0, 'y':0, 'point':0, 'isClose':False},
            }
        self.AuxLine = {
            'show':False, 'pt':0,
            'horizontal':True, 'vertical':True, 'isMax':True, 'isMin':True,
            'color':6, 'limit_color':8,
            'Max':{'x':0, 'y':0}, 'Min':{'x':0, 'y':0},
            }
        self.Reset_Aux_limit()
        self.Color = colorlist()
        self.re_Color = colorName()
    
    def update_figure(self,
            width, pathwidth,
            table_point, table_line,
            table_chain, table_shaft,
            table_slider, table_rod, table_parameter,
            table_style, zoom_rate,
            Font_size, showDimension, Point_mark, Blackground):
        if Blackground: self.points['style']['Background'] = Qt.black
        else: self.points['style']['Background'] = Qt.white
        self.Font_size = Font_size
        self.points['style']['dimension'] = showDimension
        self.Point_mark = Point_mark
        self.points['style']['penWidth']['pen'] = width
        self.points['style']['penWidth']['path'] = pathwidth
        self.zoom = float(zoom_rate.replace("%", ""))/100
        self.points['x'] = []
        self.points['y'] = []
        for i in range(len(table_point)):
            try:
                self.points['x'] += [table_point[i]['cx']*self.zoom*self.points['rate']]
                self.points['y'] += [table_point[i]['cy']*self.zoom*self.points['rate']*(-1)]
            except:
                self.points['x'] += [table_point[i]['x']*self.zoom*self.points['rate']]
                self.points['y'] += [table_point[i]['y']*self.zoom*self.points['rate']*(-1)]
        self.table_point = table_point
        self.table_line = table_line
        self.table_chain = table_chain
        self.table_shaft = table_shaft
        self.table_slider = table_slider
        self.table_rod = table_rod
        self.table_style = table_style
        self.update()
    
    def path_track(self, path, run_list, shaft_list):
        self.points['Path']['path'] = path
        self.points['Path']['run_list'] = run_list
        self.points['Path']['shaft_list'] = shaft_list
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.points['style']['Background']))
        painter.translate(self.points['origin']['x'], self.points['origin']['y'])
        for i in range(len(self.table_chain)):
            pa = self.table_chain[i]['p1']
            pb = self.table_chain[i]['p2']
            pc = self.table_chain[i]['p3']
            pen = QPen()
            pen.setWidth(self.points['style']['penWidth']['pen'])
            painter.setBrush(self.points['style']['chain'])
            painter.drawPolygon(
                QPointF(self.points['x'][pa], self.points['y'][pa]),
                QPointF(self.points['x'][pb], self.points['y'][pb]),
                QPointF(self.points['x'][pc], self.points['y'][pc]), fillRule=Qt.OddEvenFill)
            painter.setBrush(Qt.NoBrush)
            if self.points['style']['dimension']:
                pen.setColor(self.points['style']['text'])
                painter.setPen(pen)
                painter.setFont(QFont("Arial", self.Font_size))
                mp = QPointF((self.points['x'][pa]+self.points['x'][pb])/2, (self.points['y'][pa]+self.points['y'][pb])/2)
                painter.drawText(mp, str(self.table_chain[i]['p1p2']))
                mp = QPointF((self.points['x'][pb]+self.points['x'][pc])/2, (self.points['y'][pb]+self.points['y'][pc])/2)
                painter.drawText(mp, str(self.table_chain[i]['p2p3']))
                mp = QPointF((self.points['x'][pa]+self.points['x'][pc])/2, (self.points['y'][pa]+self.points['y'][pc])/2)
                painter.drawText(mp, str(self.table_chain[i]['p1p3']))
        for i in range(len(self.table_line)):
            start = self.table_line[i]['start']
            end = self.table_line[i]['end']
            point_start = QPointF(self.points['x'][start], self.points['y'][start])
            point_end = QPointF(self.points['x'][end], self.points['y'][end])
            pen = QPen()
            pen.setWidth(self.points['style']['penWidth']['pen'])
            pen.setColor(self.points['style']['link'])
            painter.setPen(pen)
            painter.drawLine(point_start, point_end)
            if self.points['style']['dimension']:
                pen.setColor(self.points['style']['text'])
                painter.setPen(pen)
                mp = QPointF((self.points['x'][start]+self.points['x'][end])/2, (self.points['y'][start]+self.points['y'][end])/2)
                painter.setFont(QFont("Arial", self.Font_size))
                painter.drawText(mp, str(self.table_line[i]['len']))
        for i in range(len(self.table_shaft)):
            start = self.table_shaft[i]['cen']
            end = self.table_shaft[i]['ref']
            pen = QPen(Qt.DotLine)
            pen.setWidth(self.points['style']['penWidth']['pen']+2)
            pen.setColor(QColor(225, 140, 0))
            painter.setPen(pen)
            painter.drawLine(QPointF(int(self.points['x'][start]), int(self.points['y'][start])), QPointF(int(self.points['x'][end]), int(self.points['y'][end])))
        if self.AuxLine['show']:
            pen = QPen(Qt.DashDotLine)
            pen.setColor(self.Color[self.re_Color[self.AuxLine['limit_color']]])
            pen.setWidth(self.points['style']['penWidth']['pen'])
            painter.setPen(pen)
            if self.AuxLine['isMax']:
                if self.AuxLine['Max']['x'] < self.table_point[self.AuxLine['pt']]['cx']: self.AuxLine['Max']['x'] = self.table_point[self.AuxLine['pt']]['cx']
                if self.AuxLine['Max']['y'] < self.table_point[self.AuxLine['pt']]['cy']: self.AuxLine['Max']['y'] = self.table_point[self.AuxLine['pt']]['cy']
                L_point = QPointF(self.width()*4, self.AuxLine['Max']['y']*self.zoom*self.points['rate']*(-1))
                R_point = QPointF(self.width()*(-4), self.AuxLine['Max']['y']*self.zoom*self.points['rate']*(-1))
                U_point = QPointF(self.AuxLine['Max']['x']*self.zoom*self.points['rate'], self.height()*4)
                D_point = QPointF(self.AuxLine['Max']['x']*self.zoom*self.points['rate'], self.height()*(-4))
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.points['style']['dimension']:
                    text_center_x = QPointF(self.AuxLine['Max']['x']*self.zoom*self.points['rate']+self.points['style']['penWidth']['pen'], self.points['origin']['y']*(-1)+self.Font_size)
                    text_center_y = QPointF(self.points['origin']['x']*(-1), self.AuxLine['Max']['y']*self.zoom*self.points['rate']*(-1)-self.points['style']['penWidth']['pen'])
                    painter.setFont(QFont("Arial", self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine['Max']['x'])
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine['Max']['y'])
            if self.AuxLine['isMin']:
                if self.AuxLine['Min']['x'] > self.table_point[self.AuxLine['pt']]['cx']: self.AuxLine['Min']['x'] = self.table_point[self.AuxLine['pt']]['cx']
                if self.AuxLine['Min']['y'] > self.table_point[self.AuxLine['pt']]['cy']: self.AuxLine['Min']['y'] = self.table_point[self.AuxLine['pt']]['cy']
                L_point = QPointF(self.width()*4, self.AuxLine['Min']['y']*self.zoom*self.points['rate']*(-1))
                R_point = QPointF(self.width()*(-4), self.AuxLine['Min']['y']*self.zoom*self.points['rate']*(-1))
                U_point = QPointF(self.AuxLine['Min']['x']*self.zoom*self.points['rate'], self.height()*4)
                D_point = QPointF(self.AuxLine['Min']['x']*self.zoom*self.points['rate'], self.height()*(-4))
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.points['style']['dimension']:
                    text_center_x = QPointF(self.AuxLine['Min']['x']*self.zoom*self.points['rate']+self.points['style']['penWidth']['pen'], self.points['origin']['y']*(-1)+self.Font_size)
                    text_center_y = QPointF(self.points['origin']['x']*(-1), self.AuxLine['Min']['y']*self.zoom*self.points['rate']*(-1)-self.points['style']['penWidth']['pen'])
                    painter.setFont(QFont("Arial", self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine['Min']['x'])
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine['Min']['y'])
            pen.setColor(self.Color[self.re_Color[self.AuxLine['color']]])
            L_point = QPointF(self.width()*4, self.points['y'][self.AuxLine['pt']])
            R_point = QPointF(self.width()*(-4), self.points['y'][self.AuxLine['pt']])
            U_point = QPointF(self.points['x'][self.AuxLine['pt']], self.height()*4)
            D_point = QPointF(self.points['x'][self.AuxLine['pt']], self.height()*(-4))
            painter.setPen(pen)
            if self.AuxLine['horizontal']: painter.drawLine(L_point, R_point)
            if self.AuxLine['vertical']: painter.drawLine(U_point, D_point)
        for i in range(len(self.table_point)):
            pen = QPen()
            pen.setWidth(2)
            point_center = QPointF(int(self.points['x'][i]), int(self.points['y'][i]))
            text_center = QPointF(int(self.points['x'][i]+6), int(self.points['y'][i]-6))
            try:
                try: pen.setColor(self.Color[self.table_style.cellWidget(i, 3).currentText()])
                except: pen.setColor(self.Color[self.table_style.item(i, 3).text()])
            except: pen.setColor(self.points['style']['pt'])
            painter.setPen(pen)
            r = float(self.table_style.item(i, 2).text())
            painter.drawEllipse(point_center, r, r)
            try:
                try: pen.setColor(self.Color[self.table_style.cellWidget(i, 1).currentText()])
                except: pen.setColor(self.Color[self.table_style.item(i, 1).text()])
            except: pen.setColor(self.points['style']['pt'])
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawPoint(point_center)
            if self.Point_mark:
                pen.setColor(self.points['style']['text'])
                pen.setWidth(2)
                painter.setPen(pen)
                painter.setFont(QFont("Arial", self.Font_size))
                painter.drawText(text_center, "[Point"+str(i)+"]")
        if self.points['Path']['path'] and self.points['Path']['show']:
            pen = QPen()
            for i in range(len(self.points['Path']['path'])):
                nPath = self.points['Path']['path'][i]
                for j in range(0, len(nPath), 2):
                    X_path = nPath[j]
                    Y_path = nPath[j+1]
                    if self.points['Path']['shaft_list'][i]==0:
                        pen.setWidth(3)
                        point_color = self.table_style.cellWidget(int(self.points['Path']['run_list'][int(j/2)].replace("Point", "")), 3).currentText()
                        pen.setColor(self.Color[point_color])
                    else:
                        pen.setWidth(1)
                        pen.setColor(self.Color['Gray'])
                    painter.setPen(pen)
                    for k in range(len(X_path)-1):
                        point_center = QPointF(X_path[k]*self.zoom*self.points['rate'], Y_path[k]*self.zoom*self.points['rate']*(-1))
                        painter.drawPoint(point_center)
        painter.end()
        self.change_event.emit()
    
    def Reset_Aux_limit(self):
        try:
            self.AuxLine['Max']['x'] = self.table_point[self.AuxLine['pt']]['cx']
            self.AuxLine['Max']['y'] = self.table_point[self.AuxLine['pt']]['cy']
            self.AuxLine['Min']['x'] = self.table_point[self.AuxLine['pt']]['cx']
            self.AuxLine['Min']['y'] = self.table_point[self.AuxLine['pt']]['cy']
        except:
            self.AuxLine['Max']['x'] = 0
            self.AuxLine['Max']['y'] = 0
            self.AuxLine['Min']['x'] = 0
            self.AuxLine['Min']['y'] = 0
    def removePath(self): self.points['Path']['path'] = []
    
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
    def mouseMoveEvent(self, event):
        if self.Selector['Drag']['isDrag']:
            self.points['origin']['x'] = event.x()-self.Selector['Drag']['x']
            self.points['origin']['y'] = event.y()-self.Selector['Drag']['y']
            self.update()
        self.Selector['Scanner']['x'] = round((event.x()-self.points['origin']['x'])/self.zoom/self.points['rate'], 2)
        self.Selector['Scanner']['y'] = round((event.y()-self.points['origin']['y'])*(-1)/self.zoom/self.points['rate'], 2)
        self.mouse_track.emit(self.Selector['Scanner']['x'], self.Selector['Scanner']['y'])
    
    def closePoint(self):
        deviation = 3
        '''
        xVal = [e for e in ]
        for i in range(self.table_point):
            x = min(self.table_point[i], key=lambda k:abs(k-self.Selector['Scanner']['x']))
            y = min(self.table_point[i], key=lambda k:abs(k-self.Selector['Scanner']['y']))
            x = abs(self.table_point[i][3]-self.Selector['Scanner']['x'])
            y = abs(self.table_point[i][4]-self.Selector['Scanner']['y'])
            if x<=deviation and y<=deviation:
                self.Selector['Scanner']['point'] = i
        '''
