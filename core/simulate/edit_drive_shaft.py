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
    
    def setUI(self, table1, table2, pos):
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table1.rowCount()):
            self.Shaft_Center.insertItem(i, icon, table1.item(i, 0).text())
            self.References.insertItem(i, icon, table1.item(i, 0).text())
        for i in range(table2.rowCount()): self.Shaft.insertItem(i, QIcon(QPixmap(":/icons/circle.png")), table2.item(i, 0).text())
        self.Shaft.setCurrentIndex(pos)
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index): self.Another_shaft.emit(index)
    
    @pyqtSlot(int, int, float, float)
    def change_feedback(self, center, references, start, end):
        self.Shaft_Center.setCurrentIndex(center)
        self.References.setCurrentIndex(references)
        self.Start_Angle.setValue(start)
        self.End_Angle.setValue(end)
