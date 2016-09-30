# -*- coding: utf-8 -*-
#PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .calculation import Solvespace

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
        self.Blackground = Qt.white
        self.origin_x = self.width()/2
        self.origin_y = self.height()/2
        self.drag = False
        self.Dimension = False
        self.Path = []
        self.Path_show = True
        self.run_list = []
        self.pen_width = 2
        self.path_width = 1
        self.AuxLine_show = False
        self.AuxLine_pt = 0
        self.AuxLine_color = 6
        self.AuxLine_limit_color = 8
        self.AuxLine_H = True
        self.AuxLine_V = True
        self.AuxLine_Max = True
        self.AuxLine_Max_x = 0
        self.AuxLine_Max_y = 0
        self.AuxLine_Min = True
        self.AuxLine_Min_x = 0
        self.AuxLine_Min_y = 0
        self.re_Color = ['Red', 'Green', 'Blue', 'Cyan', 'Magenta', 'Yellow', 'Gray', 'Orange', 'Pink',
            'Black', 'White',
            'Dark Red', 'Dark Green', 'Dark Blue', 'Dark Cyan', 'Dark Magenta', 'Dark Yellow', 'Dark Gray', 'Dark Orange', 'Dark Pink']
        val_Color = [Qt.red, Qt.green, Qt.blue, Qt.cyan, Qt.magenta, Qt.yellow, Qt.gray, QColor(225, 165, 0), QColor(225, 192, 230),
            Qt.black, Qt.white,
            Qt.darkRed, Qt.darkGreen, Qt.darkBlue, Qt.darkMagenta, Qt.darkCyan, Qt.darkYellow, Qt.darkGray, QColor(225, 140, 0), QColor(225, 20, 147)]
        self.Color = dict(zip(self.re_Color, val_Color))
    
    def update_figure(self, width, pathwidth,
            table_point, table_line,
            table_chain, table_shaft,
            table_slider, table_rod, table_parameter,
            table_style, zoom_rate,
            Font_size, Dimension, Point_mark, Blackground):
        slvs = Solvespace()
        table_point, table_line, table_chain, table_shaft, table_slider, table_rod = slvs.table_process(table_point, table_line, table_chain, table_shaft, table_slider, table_rod, table_parameter)
        if not(self.Solve_error):
            if Blackground: self.Blackground = Qt.black
            else: self.Blackground = Qt.white
        else: self.Blackground = QColor(102, 0, 0)
        self.Font_size = Font_size
        self.Dimension = Dimension
        self.Point_mark = Point_mark
        self.pen_width = width
        self.path_width = pathwidth
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
        self.Path = path
        self.run_list = run_list
        self.update()
    
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QBrush(self.Blackground))
        painter.translate(self.origin_x, self.origin_y)
        for i in range(len(self.table_chain)):
            pa = self.table_chain[i][0]
            pb = self.table_chain[i][1]
            pc = self.table_chain[i][2]
            pen = QPen()
            pen.setWidth(self.pen_width)
            painter.setBrush(Qt.cyan)
            painter.drawPolygon(
                QPointF(self.Xval[pa], self.Yval[pa]),
                QPointF(self.Xval[pb], self.Yval[pb]),
                QPointF(self.Xval[pc], self.Yval[pc]), fillRule=Qt.OddEvenFill)
            painter.setBrush(Qt.NoBrush)
            if self.Dimension:
                pen.setColor(Qt.darkGray)
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
            pen.setWidth(self.pen_width)
            pen.setColor(Qt.darkGray)
            painter.setPen(pen)
            painter.drawLine(point_start, point_end)
            if self.Dimension:
                pen.setColor(Qt.darkGray)
                painter.setPen(pen)
                mp = QPointF((self.Xval[start]+self.Xval[end])/2, (self.Yval[start]+self.Yval[end])/2)
                painter.setFont(QFont("Arial", self.Font_size))
                painter.drawText(mp, str(self.table_line[i][2]))
        for i in range(len(self.table_shaft)):
            start = self.table_shaft[i][0]
            end = self.table_shaft[i][1]
            pen = QPen(Qt.DotLine)
            pen.setWidth(self.pen_width+2)
            pen.setColor(QColor(225, 140, 0))
            painter.setPen(pen)
            painter.drawLine(QPointF(int(self.Xval[start]), int(self.Yval[start])), QPointF(int(self.Xval[end]), int(self.Yval[end])))
        if self.AuxLine_show:
            pen = QPen(Qt.DashDotLine)
            pen.setColor(self.Color[self.re_Color[self.AuxLine_limit_color]])
            pen.setWidth(self.pen_width)
            painter.setPen(pen)
            if self.AuxLine_Max:
                if self.AuxLine_Max_x < self.table_point[self.AuxLine_pt][3]: self.AuxLine_Max_x = self.table_point[self.AuxLine_pt][3]
                if self.AuxLine_Max_y < self.table_point[self.AuxLine_pt][4]: self.AuxLine_Max_y = self.table_point[self.AuxLine_pt][4]
                L_point = QPointF(self.width()*4, self.AuxLine_Max_y*self.zoom*self.rate_all*(-1))
                R_point = QPointF(self.width()*(-4), self.AuxLine_Max_y*self.zoom*self.rate_all*(-1))
                U_point = QPointF(self.AuxLine_Max_x*self.zoom*self.rate_all, self.height()*4)
                D_point = QPointF(self.AuxLine_Max_x*self.zoom*self.rate_all, self.height()*(-4))
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.Dimension:
                    text_center_x = QPointF(self.AuxLine_Max_x*self.zoom*self.rate_all+self.pen_width, self.origin_y*(-1)+self.Font_size)
                    text_center_y = QPointF(self.origin_x*(-1), self.AuxLine_Max_y*self.zoom*self.rate_all*(-1)-self.pen_width)
                    painter.setFont(QFont("Arial", self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine_Max_x)
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine_Max_y)
            if self.AuxLine_Min:
                if self.AuxLine_Min_x > self.table_point[self.AuxLine_pt][3]: self.AuxLine_Min_x = self.table_point[self.AuxLine_pt][3]
                if self.AuxLine_Min_y > self.table_point[self.AuxLine_pt][4]: self.AuxLine_Min_y = self.table_point[self.AuxLine_pt][4]
                L_point = QPointF(self.width()*4, self.AuxLine_Min_y*self.zoom*self.rate_all*(-1))
                R_point = QPointF(self.width()*(-4), self.AuxLine_Min_y*self.zoom*self.rate_all*(-1))
                U_point = QPointF(self.AuxLine_Min_x*self.zoom*self.rate_all, self.height()*4)
                D_point = QPointF(self.AuxLine_Min_x*self.zoom*self.rate_all, self.height()*(-4))
                painter.drawLine(L_point, R_point)
                painter.drawLine(U_point, D_point)
                if self.Dimension:
                    text_center_x = QPointF(self.AuxLine_Min_x*self.zoom*self.rate_all+self.pen_width, self.origin_y*(-1)+self.Font_size)
                    text_center_y = QPointF(self.origin_x*(-1), self.AuxLine_Min_y*self.zoom*self.rate_all*(-1)-self.pen_width)
                    painter.setFont(QFont("Arial", self.Font_size))
                    painter.drawText(text_center_x, "%.6f"%self.AuxLine_Min_x)
                    painter.drawText(text_center_y, "%.6f"%self.AuxLine_Min_y)
            pen.setColor(self.Color[self.re_Color[self.AuxLine_color]])
            L_point = QPointF(self.width()*4, self.Yval[self.AuxLine_pt])
            R_point = QPointF(self.width()*(-4), self.Yval[self.AuxLine_pt])
            U_point = QPointF(self.Xval[self.AuxLine_pt], self.height()*4)
            D_point = QPointF(self.Xval[self.AuxLine_pt], self.height()*(-4))
            painter.setPen(pen)
            if self.AuxLine_H: painter.drawLine(L_point, R_point)
            if self.AuxLine_V: painter.drawLine(U_point, D_point)
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
                pen.setColor(Qt.darkGray)
                pen.setWidth(2)
                painter.setPen(pen)
                painter.setFont(QFont("Arial", self.Font_size))
                painter.drawText(text_center, "[Point"+str(i)+"]")
        if self.Path and self.Path_show:
            pen = QPen()
            pen.setWidth(self.path_width)
            for i in range(len(self.Path)):
                nPath = self.Path[i]
                for j in range(0, len(nPath), 2):
                    X_path = nPath[j]
                    Y_path = nPath[j+1]
                    point_color = self.table_style.cellWidget(int(self.run_list[int(j/2)].replace("Point", "")), 3).currentText()
                    pen.setColor(self.Color[point_color])
                    painter.setPen(pen)
                    for k in range(len(X_path)-1):
                        point_center = QPointF(X_path[k]*self.zoom*self.rate_all, Y_path[k]*self.zoom*self.rate_all*(-1))
                        painter.drawPoint(point_center)
        painter.end()
        self.change_event.emit()
    
    def Reset_Aux_limit(self):
        self.AuxLine_Max_x = self.table_point[self.AuxLine_pt][3]
        self.AuxLine_Max_y = self.table_point[self.AuxLine_pt][4]
        self.AuxLine_Min_x = self.table_point[self.AuxLine_pt][3]
        self.AuxLine_Min_y = self.table_point[self.AuxLine_pt][4]
    
    def removePath(self): self.Path = []
    
    def mousePressEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier: self.drag = True
    
    def mouseReleaseEvent(self, event): self.drag = False
    def mouseDoubleClickEvent(self, event):
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.update()
    def mouseMoveEvent(self, event):
        if self.drag:
            self.origin_x = event.x()
            self.origin_y = event.y()
            self.update()
        self.mouse_track.emit(round((event.x()-self.origin_x)/self.zoom/self.rate_all, 2), round((event.y()-self.origin_y)*(-1)/self.zoom/self.rate_all, 2))
