# -*- coding: utf-8 -*-
from ..QtModules import *
from .color import colorlist, colorName
_translate = QCoreApplication.translate

class DynamicCanvas(QGraphicsScene):
    mouse_track = pyqtSignal(float, float)
    def __init__(self, parent=None):
        super(DynamicCanvas, self).__init__(parent)
        self.setSceneRect(-10000, -10000, 20000, 20000)
        text = self.addText("Hello, world!")
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setPos(QPointF(0., 0.))
        self.PointItemList = list()
        self.LineItemList = list()
        self.ChainItemList = list()

class DynamicCanvasView(QGraphicsView):
    mouse_track = pyqtSignal(float, float)
    def __init__(self, parent=None):
        super(DynamicCanvasView, self).__init__(DynamicCanvas(), parent)
        self.setViewportUpdateMode(QGraphicsView.MinimalViewportUpdate)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.originPos = self.mapToScene(QPoint(self.width()/2, self.height()/2))
        self.SetIn()
        self.Factor = 2.
        self.minFactor = .25
        self.maxFactor = 8.
    
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
        self.resetTransform()
        self.centerOn(QPoint(0, 0))
    
    def mouseDoubleClickEvent(self, event):
        super(DynamicCanvasView, self).mouseDoubleClickEvent(event)
        if event.buttons()==Qt.MiddleButton: self.SetIn
    
    def mousePressEvent(self, event):
        super(DynamicCanvasView, self).mousePressEvent(event)
        if event.buttons()==Qt.MiddleButton:
            self.originPos = event.pos()
            print("+Origin: {}, {}".format(self.originPos.x(), self.originPos.y()))
            self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
    
    def wheelEvent(self, event):
        super(DynamicCanvasView, self).wheelEvent(event)
        if event.angleDelta().y()>0 and self.Factor<=8.:
            self.Factor += .1
            self.scale(1.1, 1.1)
        elif event.angleDelta().y()<0 and self.Factor>=.25:
            self.Factor -= .1
            self.scale(1/1.1, 1/1.1)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
    
    def mouseMoveEvent(self, event):
        super(DynamicCanvasView, self).mouseMoveEvent(event)
        self.mouse_track.emit(event.x(), event.y())
        if event.buttons()==Qt.MiddleButton:
            self.centerOn(self.viewport().rect().center()-event.pos())
            self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
