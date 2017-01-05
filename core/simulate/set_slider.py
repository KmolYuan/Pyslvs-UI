# -*- coding: utf-8 -*-
from .modules import *

class slider_show(QDialog, slider_Dialog):
    def __init__(self, table1, table2, row, parent=None):
        super(slider_show, self).__init__(parent)
        self.setupUi(self)
        for i in range(table1.rowCount()): self.Slider_Center.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table1.item(i, 0).text())
        for i in range(table2.rowCount()): self.References.insertItem(i, QIcon(QPixmap(":/icons/line.png")), table2.item(i, 0).text())
        self.Slider_num.insertPlainText("Slider"+str(row))
