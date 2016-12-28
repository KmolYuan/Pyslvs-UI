# -*- coding: utf-8 -*-
from .modules import *

class slider_show(QDialog, slider_Dialog):
    def __init__(self, parent=None):
        super(slider_show, self).__init__(parent)
        self.setupUi(self)
    
    def setUI(self, table1, table2, row):
        for i in range(table1.rowCount()): self.Slider_Center.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table1.item(i, 0).text())
        for i in range(table2.rowCount()): self.References.insertItem(i, QIcon(QPixmap(":/icons/line.png")), table2.item(i, 0).text())
        self.Slider_num.insertPlainText("Slider"+str(row))
