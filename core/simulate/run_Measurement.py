# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_run_Measurement import Ui_Form

class Measurement_show(QWidget, Ui_Form):
    point_change = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(Measurement_show, self).__init__(parent)
        self.setupUi(self)
        self.Distance.setPlainText("0.0")
        self.Detection = True
        self.First_Detection = True
    
    @pyqtSlot(float, float)
    def show_mouse_track(self, x, y): self.Mouse.setPlainText("("+str(x)+", "+str(y)+")")
    
    @pyqtSlot(int)
    def on_Start_currentIndexChanged(self, index):
        self.First_Detection = True
        self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
    
    @pyqtSlot(int)
    def on_End_currentIndexChanged(self, index):
        self.First_Detection = True
        self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
    
    @pyqtSlot(float)
    def change_distance(self, val): self.Distance.setPlainText(str(val))
    
    @pyqtSlot(bool)
    def on_Keep_Detection_toggled(self, checked): self.Detection = checked
    
    @pyqtSlot()
    def Detection_do(self):
        if self.First_Detection:
            self.First_Detection = False
            self.Max_val.setPlainText(self.Distance.toPlainText())
            self.Min_val.setPlainText(self.Distance.toPlainText())
        else:
            if float(self.Max_val.toPlainText())<float(self.Distance.toPlainText()): self.Max_val.setPlainText(self.Distance.toPlainText())
            if float(self.Min_val.toPlainText())>float(self.Distance.toPlainText()): self.Min_val.setPlainText(self.Distance.toPlainText())
        if self.Detection: self.point_change.emit(self.Start.currentIndex(), self.End.currentIndex())
