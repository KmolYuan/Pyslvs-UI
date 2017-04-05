# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_template import Ui_Dialog

class templatePreview(QGraphicsScene):
    def __init__(self, Ax, Ay, Bx, By, parent=None):
        super(templatePreview, self).__init__(parent)
        self.pen = QPen()
        self.pen.setWidth(3)
        self.Ax = Ax
        self.Ay = Ay
        self.Bx = Bx
        self.By = By
        self.setBase()
    
    def setBase(self):
        self.pen.setColor(QColor(172, 68, 68))
        self.A = self.addEllipse(QRectF(20., 20., 20., 20.), self.pen, QBrush(Qt.NoBrush))
        self.A.setFlag(QGraphicsItem.ItemIsSelectable)
        self.A.setPos(QPointF(self.Ax, -self.Ay))
        self.pen.setColor(QColor(68, 120, 172))
        self.B = self.addEllipse(QRectF(20., 20., 20., 20.), self.pen, QBrush(Qt.NoBrush))
        self.B.setFlag(QGraphicsItem.ItemIsSelectable)
        self.B.setPos(QPointF(self.Bx, -self.By))
    
    @pyqtSlot(float)
    def setAx(self, x): self.A.setPos(QPointF(x, self.A.y()))
    @pyqtSlot(float)
    def setAy(self, y): self.A.setPos(QPointF(self.A.x(), -y))
    @pyqtSlot(float)
    def setBx(self, x): self.B.setPos(QPointF(x, self.B.y()))
    @pyqtSlot(float)
    def setBy(self, y): self.B.setPos(QPointF(self.B.x(), -y))
    
    def setTemplate(self, p0): pass

class template_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(template_show, self).__init__(parent)
        self.setupUi(self)
        self.previewScene = templatePreview(self.Ax.value(), self.Ay.value(), self.Bx.value(), self.By.value())
        self.preview.setScene(self.previewScene)
        self.Ax.valueChanged.connect(self.previewScene.setAx)
        self.Ay.valueChanged.connect(self.previewScene.setAy)
        self.Bx.valueChanged.connect(self.previewScene.setBx)
        self.By.valueChanged.connect(self.previewScene.setBy)
    
    @pyqtSlot(int)
    def on_templateChoose_currentIndexChanged(self, p0): self.previewScene.setTemplate(p0)
