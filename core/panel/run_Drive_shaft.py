# -*- coding: utf-8 -*-
from ..draw.modules import *
from .Ui_run_Drive_shaft import Ui_Form as Drive_Form

class Drive_shaft_show(QWidget, Drive_Form):
    def __init__(self, table, parent=None):
        super(Drive_shaft_show, self).__init__(parent)
        self.setupUi(self)
        self.Degree.setMinimum(int(table[0]['start']*100))
        self.Degree.setMaximum(int(table[0]['end']*100))
        self.Degree.setValue(int(table[0]['demo']*100))
    
    @pyqtSlot(int)
    def on_Degree_valueChanged(self, value): self.Degree_text.setValue(float(value/100))
    @pyqtSlot(float)
    def on_Degree_text_valueChanged(self, val): self.Degree.setValue(int(val*100))
