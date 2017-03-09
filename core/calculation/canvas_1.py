# -*- coding: utf-8 -*-
from ..QtModules import *
from .color import colorlist, colorName
_translate = QCoreApplication.translate

class DynamicCanvas(QGraphicsScene):
    mouse_track = pyqtSignal(float, float)
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        text = self.addText("Hello, world!")
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setPos(QPointF(10, 20))
        self.PointItemList = list()
        self.LineItemList = list()
        self.ChainItemList = list()

class DynamicCanvasView(QGraphicsView):
    mouse_track = pyqtSignal(float, float)
    def __init__(self, parent=None):
        super(DynamicCanvasView, self).__init__(DynamicCanvas(), parent)
        #self.setSceneRect(-100000000, 100000000, 100000000, -100000000)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.isDrag = False
        self.m_originX = 0
        self.m_originY = 0
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    
    def update_figure(self, width, pathwidth, Point, Line, Chain, Shaft, Slider, Rod,
            table_style, zoom_rate, Font_size, showDimension, Point_mark, Blackground,
            path, run_list, shaft_list):
        self.zoom = float(zoom_rate.replace("%", ""))/100
        
    
    def path_track(self, path, run_list, shaft_list):
        pass
    
    def path_solving(self, path):
        pass
    
    def Reset_Aux_limit(self):
        pass
    
    def reset_Auxline(self):
        pass
    
    def SetIn(self):
        pass
    
    def wheelEvent(self, event):
        if event.angleDelta().y()>0: self.scale(1.1, 1.1)
        if event.angleDelta().y()<0: self.scale(1/1.1, 1/1.1)
    
    def mouseMoveEvent(self, event):
        if event.buttons()==Qt.MiddleButton:
            self.mouse_track.emit(event.x(), event.y())
            print(event.x(), event.y())
            self.centerOn(event.pos())
            self.m_originX, self.m_originY = event.x(), event.y()
