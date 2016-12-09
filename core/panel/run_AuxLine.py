# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_run_AuxLine import Ui_Form

class AuxLine_show(QWidget, Ui_Form):
    Point_change = pyqtSignal(int, int, int, bool, bool, bool, bool, bool)
    def __init__(self, parent=None):
        super(AuxLine_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index): self.Change_set(True)
    @pyqtSlot(int)
    def on_Color_currentIndexChanged(self, index): self.Change_set()
    @pyqtSlot()
    def on_H_line_clicked(self): self.Change_set()
    @pyqtSlot()
    def on_V_line_clicked(self): self.Change_set()
    @pyqtSlot()
    def on_Max_Limit_clicked(self): self.Change_set()
    @pyqtSlot()
    def on_Min_Limit_clicked(self): self.Change_set()
    @pyqtSlot(int)
    def on_Color_l_currentIndexChanged(self, index): self.Change_set()
    
    def Change_set(self, pt = False):
        self.Point_change.emit(
            self.Point.currentIndex(),
            self.Color.currentIndex(),
            self.Color_l.currentIndex(),
            self.H_line.checkState(),
            self.V_line.checkState(),
            self.Max_Limit.checkState(),
            self.Min_Limit.checkState(),
            pt)
