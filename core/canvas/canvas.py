# -*- coding: utf-8 -*-
#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from ..calculation import Solvespace

class DynamicCanvas(QWidget):
    mouse_track = pyqtSignal(float, float)
    change_event = pyqtSignal()
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setParent(parent)
        self.setMouseTracking(True)
        self.Reset_Origin = False
        self.Solve_error = False
        self.Xval = []
        self.Yval = []
        self.style = {'Background':Qt.white, 'link':Qt.darkGray, 'chain':Qt.cyan, 'text':Qt.darkGray}
        self.origin = {'x':self.width()/2, 'y':self.height()/2}
        self.Drag = {'x':0, 'y':0, 'isDrag':False}
        self.showDimension = False
        self.Path = {'show':True, 'path':[], 'run_list':[]}
        self.penWidth = {'pen':2, 'path':1}
        self.AuxLine = {
            'show':False, 'pt':0,
            'horizontal':True, 'vertical':True,
            'Max':True, 'Min':True,
            'color':6, 'limit_color':8,
            'Max':{'x':0, 'y':0}, 'Min':{'x':0, 'y':0},
            }
        self.Reset_Aux_limit()
        self.Color = {
            'Red':Qt.red,
            'Green':Qt.green,
            'Blue':Qt.blue,
            'Cyan':Qt.cyan,
            'Magenta':Qt.magenta,
            'Yellow':Qt.yellow,
            'Gray':Qt.gray,
            'Orange':QColor(225, 165, 0),
            'Pink':QColor(225, 192, 230),
            'Black':Qt.black,
            'White':Qt.white,
            'Dark Red':Qt.darkRed,
            'Dark Green':Qt.darkGreen,
            'Dark Blue':Qt.darkBlue,
            'Dark Cyan':Qt.darkCyan,
            'Dark Magenta':Qt.darkMagenta,
            'Dark Yellow':Qt.darkYellow,
            'Dark Gray':Qt.darkGray,
            'Dark Orange':QColor(225, 140, 0),
            'Dark Pink':QColor(225, 20, 147),
            }
        self.re_Color = [e for e in self.Color]
    
    def update_figure(self, width, pathwidth,
            table_point, table_line,
            table_chain, table_shaft,
            table_slider, table_rod, table_parameter,
            table_style, zoom_rate,
            Font_size, showDimension, Point_mark, Blackground):
        slvs = Solvespace()
        table_point, table_line, table_chain, table_shaft, table_slider, table_rod = slvs.table_process(table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter)
        if not(self.Solve_error):
            if Blackground: self.style['Background'] = Qt.black
            else: self.style['Background'] = Qt.white
        else: self.style['Background'] = QColor(102, 0, 0)
        self.Font_size = Font_size
        self.showDimension = showDimension
        self.Point_mark = Point_mark
        self.penWidth['pen'] = width
        self.penWidth['path'] = pathwidth
        self.Xval = []
        self.Yval = []
        self.zoom = float(zoom_rate.replace("%", ""))/100
        self.rate_all = 2
        for i in range(len(table_point)):
            try:
                self.Xval += [table_point[i][3]*self.zoom*self.rate_all]
                self.Yval += [table_point[i][4]*self.zoom*self.rate_all*(-1)]
            except:
                self.Xval += [table_point[i][0]*self.zoom*self.rate_all]
                self.Yval += [table_point[i][1]*self.zoom*self.rate_all*(-1)]
        self.table_point = table_point
        self.table_line = table_line
        self.table_chain = table_chain
        self.table_shaft = table_shaft
        self.table_slider = table_slider
        self.table_rod = table_rod
        self.table_style = table_style
        self.update()
    
    def path_track(self, path, run_list):
        self.Path['path'] = path
        self.Path['run_list'] = run_list
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.style['Background']))
        painter.translate(self.origin['x'], self.origin['y'])
        for i in range(len(self.table_chain)):
            pa = self.table_chain[i][0]
            pb = self.table_chain[i][1]
            pc = self.table_chain[i][2]
            pen = QPen()
            pen.setWidth(self.penWidth['pen'])
            painter.setBrush(self.style['chain'])
            painter.drawPolygon(
                QPointF(self.Xval[pa], self.Yval[pa]),
                QPointF(self.Xval[pb], self.Yval[pb]),
                QPointF(self.Xval[pc], self.Yval[pc]), fillRule=Qt.OddEvenFill)
            painter.setBrush(Qt.NoBrush)
            if self.showDimension:
                pen.setColor(self.style['text'])
                painter.setPen(pen)
                painter.setFont(QFont("Arial", self.Font_size))
                mp = QPointF((self.Xval[pa]+self.Xval[pb])/2, (self.Yval[pa]+self.Yval[pb])/2)
                painter.drawText(mp, str(self.table_chain[i][3]))
                mp = QPointF((self.Xval[pb]+self.Xval[pc])/2, (self.Yval[pb]+self.Yval[pc])/2)
                painter.drawText(mp, str(self.table_chain[i][4]))
                mp = QPointF((self.Xval[pa]+self.Xval[pc])/2, (self.Yval[pa]+self.Yval[pc])/2)
                painter.drawText(mp, str(self.table_chain[i][5]))
        for i in range(len(self.table_line)):
            start = self.table_line[i][0]
            end = self.table_line[i][1]
            point_start = QPointF(self.Xval[start], self.Yval[start])
            point_end = QPointF(self.Xval[end], self.Yval[end])
            pen = QPen()
            pen.setWidth(self.penWidth['pen'])
            pen.setColor(self.style['link'])
            painter.setPen(pen)
            painter.drawLine(point_start, point_end)
            if self.showDimension:
                pen.setColor(self.style['text'])
                painter.setPen(pen)
                mp = QPointF((self.Xval[start]+self.Xval[end])/2, (self.Yval[start]+self.Yval[end])/2)
                painter.setFont(QFont("Arial", self.Font_size))
                painter.drawText(mp, str(self.table_line[i][2]))
        for i in range(len(self.table_shaft)):
            start = self.table_shaft[i][0]
            end = self.table_shaft[i][1]
            pen = QPen(Qt.DotLine)
            pen.setWidth(self.penWidth['pen']+2)
            pen.setColor(QColor(225, 140, 0))
            painter.setPen(pen)
            painter.drawLine(QPointF(int(self.Xval[start]), int(self.Yval[start])), QPointF(int(self.Xval[end]), int(self.Yval[end])))
        if self.AuxLine['show']:
            pen = QPen(Qt.DashDotLine)
            pen.setColor(self.Color[self.re_Color[self.AuxLine['limit_color']]])
            pen.setWidth(self.penWidth['pen'])
            painter.setPen(pen)
            if self.AuxLine['Max']:
                if self.AuxLine['Max']['x'] < self.table_point[self.AuxLine['pt']][3]: self.AuxLine['Max']['x'] = self.table_point[self.AuxLine['pt']][3]
                if self.AuxLine['Max']['y'] < self.table_point[self.AuxLine['pt']][4]: self.AuxLine['Max']['y'] = self.table_point[self.AuxLine['pt']][4]
                L_point = QPointF(self.width()*4, self.AuxLine['Max']['y']*self.zoom*self.rate_all*(-1))
                R_point = QPointF(self.width()*(-4), self.AuxLine['Max']['y']*self.zoom*self.rate_all*(-1))
                U_point = QPointF(self.AuxLine['Max']['x']*self.zoom*self.rate_all, self.height()*4)
                D_point = QPointF(self.AuxLine['Max']['x']*self.zoom*self.rate_all, self.height()*(-4))
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.showDimension:
                    text_center_x = QPointF(self.AuxLine['Max']['x']*self.zoom*self.rate_all+self.penWidth['pen'], self.origin['y']*(-1)+self.Font_size)
                    text_center_y = QPointF(self.origin['x']*(-1), self.AuxLine['Max']['y']*self.zoom*self.rate_all*(-1)-self.penWidth['pen'])
                    painter.setFont(QFont("Arial", self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine['Max']['x'])
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine['Max']['y'])
            if self.AuxLine['Min']:
                if self.AuxLine['Min']['x'] > self.table_point[self.AuxLine['pt']][3]: self.AuxLine['Min']['x'] = self.table_point[self.AuxLine['pt']][3]
                if self.AuxLine['Min']['y'] > self.table_point[self.AuxLine['pt']][4]: self.AuxLine['Min']['y'] = self.table_point[self.AuxLine['pt']][4]
                L_point = QPointF(self.width()*4, self.AuxLine['Min']['y']*self.zoom*self.rate_all*(-1))
                R_point = QPointF(self.width()*(-4), self.AuxLine['Min']['y']*self.zoom*self.rate_all*(-1))
                U_point = QPointF(self.AuxLine['Min']['x']*self.zoom*self.rate_all, self.height()*4)
                D_point = QPointF(self.AuxLine['Min']['x']*self.zoom*self.rate_all, self.height()*(-4))
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.showDimension:
                    text_center_x = QPointF(self.AuxLine['Min']['x']*self.zoom*self.rate_all+self.penWidth['pen'], self.origin['y']*(-1)+self.Font_size)
                    text_center_y = QPointF(self.origin['x']*(-1), self.AuxLine['Min']['y']*self.zoom*self.rate_all*(-1)-self.penWidth['pen'])
                    painter.setFont(QFont("Arial", self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine['Min']['x'])
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine['Min']['y'])
            pen.setColor(self.Color[self.re_Color[self.AuxLine['color']]])
            L_point = QPointF(self.width()*4, self.Yval[self.AuxLine['pt']])
            R_point = QPointF(self.width()*(-4), self.Yval[self.AuxLine['pt']])
            U_point = QPointF(self.Xval[self.AuxLine['pt']], self.height()*4)
            D_point = QPointF(self.Xval[self.AuxLine['pt']], self.height()*(-4))
            painter.setPen(pen)
            if self.AuxLine['horizontal']: painter.drawLine(L_point, R_point)
            if self.AuxLine['vertical']: painter.drawLine(U_point, D_point)
        for i in range(len(self.table_point)):
            pen = QPen()
            pen.setWidth(2)
            point_center = QPointF(int(self.Xval[i]), int(self.Yval[i]))
            text_center = QPointF(int(self.Xval[i]+6), int(self.Yval[i]-6))
            try:
                try: pen.setColor(self.Color[self.table_style.cellWidget(i, 3).currentText()])
                except: pen.setColor(self.Color[self.table_style.item(i, 3).text()])
            except: pen.setColor(Qt.green)
            painter.setPen(pen)
            r = float(self.table_style.item(i, 2).text())
            painter.drawEllipse(point_center, r, r)
            try:
                try: pen.setColor(self.Color[self.table_style.cellWidget(i, 1).currentText()])
                except: pen.setColor(self.Color[self.table_style.item(i, 1).text()])
            except: pen.setColor(Qt.green)
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawPoint(point_center)
            if self.Point_mark:
                pen.setColor(self.style['text'])
                pen.setWidth(2)
                painter.setPen(pen)
                painter.setFont(QFont("Arial", self.Font_size))
                painter.drawText(text_center, "[Point"+str(i)+"]")
        if self.Path['path'] and self.Path['show']:
            pen = QPen()
            pen.setWidth(self.penWidth['path'])
            for i in range(len(self.Path['path'])):
                nPath = self.Path['path'][i]
                for j in range(0, len(nPath), 2):
                    X_path = nPath[j]
                    Y_path = nPath[j+1]
                    point_color = self.table_style.cellWidget(int(self.Path['run_list'][int(j/2)].replace("Point", "")), 3).currentText()
                    pen.setColor(self.Color[point_color])
                    painter.setPen(pen)
                    for k in range(len(X_path)-1):
                        point_center = QPointF(X_path[k]*self.zoom*self.rate_all, Y_path[k]*self.zoom*self.rate_all*(-1))
                        painter.drawPoint(point_center)
        painter.end()
        self.change_event.emit()
    
    def Reset_Aux_limit(self):
        try:
            self.AuxLine['Max']['x'] = self.table_point[self.AuxLine['pt']][3]
            self.AuxLine['Max']['y'] = self.table_point[self.AuxLine['pt']][4]
            self.AuxLine['Min']['x'] = self.table_point[self.AuxLine['pt']][3]
            self.AuxLine['Min']['y'] = self.table_point[self.AuxLine['pt']][4]
        except:
            self.AuxLine['Max']['x'] = 0
            self.AuxLine['Max']['y'] = 0
            self.AuxLine['Min']['x'] = 0
            self.AuxLine['Min']['y'] = 0
    
    def removePath(self): self.Path['path'] = []
    
    def mousePressEvent(self, event):
        if event.buttons()==Qt.MiddleButton or event.buttons()==Qt.LeftButton: self.Drag['isDrag'] = True
    def mouseReleaseEvent(self, event): self.Drag['isDrag'] = False
    
    def mouseDoubleClickEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.origin['x'] = event.x()
            self.origin['y'] = event.y()
            self.update()
    def mouseMoveEvent(self, event):
        if self.Drag['isDrag']:
            self.origin['x'] = event.x()
            self.origin['y'] = event.y()
            self.update()
        self.mouse_track.emit(round((event.x()-self.origin['x'])/self.zoom/self.rate_all, 2), round((event.y()-self.origin['y'])*(-1)/self.zoom/self.rate_all, 2))
