# -*- coding: utf-8 -*-
from .modules import *
from .Ui_run_Drive_shaft import Ui_Form as Drive_Form

class Drive_shaft_show(QWidget, Drive_Form):
    Degree_change = pyqtSignal(int, float)
    Shaft_change = pyqtSignal(int)
    def __init__(self, table, parent=None):
        super(Drive_shaft_show, self).__init__(parent)
        self.setupUi(self)
        for i in range(table.rowCount()): self.Shaft.insertItem(i, QIcon(QPixmap(":/icons/circle.png")), table.item(i, 0).text())
    
    @pyqtSlot(int)
    def on_Degree_valueChanged(self, value):
        self.Degree_change.emit(self.Shaft.currentIndex(), float(value/100))
        self.Degree_text.setValue(float(value/100))
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index): self.Shaft_change.emit(index)
    @pyqtSlot(int)
    def progressbar_change(self, val): self.Degree.setValue(val)
    @pyqtSlot(float)
    def on_Degree_text_valueChanged(self, val): self.Degree.setValue(int(val*100))
