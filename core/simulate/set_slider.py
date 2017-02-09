# -*- coding: utf-8 -*-
from .modules import *

class slider_show(QDialog, slider_Dialog):
    def __init__(self, table, row, parent=None):
        super(slider_show, self).__init__(parent)
        self.setupUi(self)
        for i in range(table.rowCount()): self.Slider_Center.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
        for i in range(table.rowCount()): self.Start.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
        for i in range(table.rowCount()): self.End.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
        self.Slider_num.insertPlainText("Slider"+str(row))
