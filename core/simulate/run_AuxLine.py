# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_run_AuxLine import Ui_Form

class AuxLine_show(QWidget, Ui_Form):
    Point_change = pyqtSignal(int, int, bool, bool)
    def __init__(self, parent=None):
        super(AuxLine_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index): self.Point_change.emit(index, self.Color.currentIndex(), self.H_line.checkState(), self.V_line.checkState())
    
    @pyqtSlot(int)
    def on_Color_currentIndexChanged(self, index): self.Point_change.emit(self.Point.currentIndex(), index, self.H_line.checkState(), self.V_line.checkState())
    
    @pyqtSlot()
    def on_H_line_clicked(self): self.Point_change.emit(self.Point.currentIndex(), self.Color.currentIndex(), self.H_line.checkState(), self.V_line.checkState())
    
    @pyqtSlot()
    def on_V_line_clicked(self): self.Point_change.emit(self.Point.currentIndex(), self.Color.currentIndex(), self.H_line.checkState(), self.V_line.checkState())
