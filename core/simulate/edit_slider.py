# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_edit_slider import Ui_Dialog

class edit_slider_show(QDialog, Ui_Dialog):
    Another_slider = pyqtSignal(int)
    def __init__(self, parent=None):
        super(edit_slider_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_Slider_currentIndexChanged(self, index): self.Another_slider.emit(index)
    
    @pyqtSlot(int, int)
    def change_feedback(self, point, line):
        self.Slider_Center.setCurrentIndex(point)
        self.References.setCurrentIndex(line)
