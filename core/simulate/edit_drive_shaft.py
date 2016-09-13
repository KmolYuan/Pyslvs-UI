# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .Ui_edit_drive_shaft import Ui_Dialog

class edit_shaft_show(QDialog, Ui_Dialog):
    Another_shaft = pyqtSignal(int)
    def __init__(self, parent=None):
        super(edit_shaft_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index): self.Another_shaft.emit(index)
    
    @pyqtSlot(int, int, float, float)
    def change_feedback(self, center, references, start, end):
        self.Shaft_Center.setCurrentIndex(center)
        self.References.setCurrentIndex(references)
        self.Start_Angle.setValue(start)
        self.End_Angle.setValue(end)
