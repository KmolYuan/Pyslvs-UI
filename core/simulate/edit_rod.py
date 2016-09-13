# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_edit_rod import Ui_Dialog

class edit_rod_show(QDialog, Ui_Dialog):
    Another_rod = pyqtSignal(int)
    def __init__(self, parent=None):
        super(edit_rod_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_Rod_currentIndexChanged(self, index): self.Another_rod.emit(index)
    
    @pyqtSlot(int, int, int, float)
    def change_feedback(self, center, start, end, position):
        self.Center.setCurrentIndex(center)
        self.Start.setCurrentIndex(start)
        self.End.setCurrentIndex(end)
        self.Position.setValue(position)
