# -*- coding: utf-8 -*-
from ..QtModules import *
from ..calculation.color import colorlist, colorName

class pointItem(QGraphicsItem):
    def __init__(self, pen, fix, parent=None):
        super(pointItem, self).__init__(parent)
        self.pen = pen
        self.fix = fix
    
    def paintEvent(self, event):
        super(pointItem, self).paintEvent(event)
        painter = QPainter()
        painter.begin(self)
        painter.setPen(self.pen)
        r = 10 if self.fix else 5
        painter.drawEllipse(QPointF(0., 0.), r, r)
        painter.drawPoint(QPointF(0., 0.))
