# -*- coding: utf-8 -*-
from .modules import *
from .canvasItem import canvasPoint, canvasLine, canvasChain

class DynamicScene(QGraphicsScene):
    def __init__(self, parent=None):
        QGraphicsScene.__init__(self, parent)
        self.addText("Hallo world!\nTesting~")
    
    def addPoint(self):
        ''''''
    
    def addLine(self):
        ''''''
    
    def addChain(self):
        ''''''
