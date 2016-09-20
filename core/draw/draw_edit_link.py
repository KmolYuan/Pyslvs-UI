# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_draw_edit_link import Ui_Dialog

class edit_link_show(QDialog, Ui_Dialog):
    Another_line = pyqtSignal(int)
    def __init__(self, parent=None):
        super(edit_link_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_Link_currentIndexChanged(self, index): self.Another_line.emit(index)
    
    @pyqtSlot(int, int, float)
    def change_feedback(self, start, end, len):
        self.Start_Point.setCurrentIndex(start)
        self.End_Point.setCurrentIndex(end)
        self.Length.setPlaceholderText(str(len))
