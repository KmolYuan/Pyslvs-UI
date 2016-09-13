# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_set_drive_shaft import Ui_Dialog

class shaft_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(shaft_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(float)
    def on_Start_Angle_valueChanged(self, p0):
        self.Demo_angle.setMinimum(p0)
        self.Demo_angle.setValue((self.Demo_angle.maximum()+self.Demo_angle.minimum())/2)
    
    @pyqtSlot(float)
    def on_End_Angle_valueChanged(self, p0):
        self.Demo_angle.setMaximum(p0)
        self.Demo_angle.setValue(int((self.Demo_angle.maximum()+self.Demo_angle.minimum())/2))
    
    @pyqtSlot(bool)
    def on_Demo_angle_enable_toggled(self, checked): self.Demo_angle.setEnabled(checked)
