# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver_template import Ui_Dialog

class Triangle_Solver_template_show(QDialog, Ui_Dialog):
    def __init__(self, Point, row, template='4-bar linkage', parent=None):
        super(Triangle_Solver_template_show, self).__init__(parent)
        self.setupUi(self)
        self.Point = Point
        self.on_templateType_currentIndexChanged(0)
        self.templateType.setCurrentIndex(self.templateType.findText(template))
    
    @pyqtSlot(int)
    def on_templateType_currentIndexChanged(self, pos):
        if pos==0: pic = ":/icons/preview/4Bar.png"
        elif pos==1: pic = ":/icons/preview/8Bar.png"
        self.templateImage.setPixmap(QPixmap(pic).scaledToWidth(500))
