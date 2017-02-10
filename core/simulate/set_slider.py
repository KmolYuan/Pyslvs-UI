# -*- coding: utf-8 -*-
from .modules import *

class slider_show(QDialog, edit_slider_Dialog):
    def __init__(self, table, row, parent=None):
        super(slider_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()): self.Slider_Center.insertItem(i, icon, table.item(i, 0).text())
        for i in range(table.rowCount()): self.Start.insertItem(i, icon, table.item(i, 0).text())
        for i in range(table.rowCount()): self.End.insertItem(i, icon, table.item(i, 0).text())
        self.Slider.addItem(QIcon(QPixmap(":/icons/pointonx.png")), "Slider"+str(row))
        self.Slider.setEnabled(False)
