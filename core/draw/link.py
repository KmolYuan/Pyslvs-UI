# -*- coding: utf-8 -*-
from .modules import *

class New_link(QDialog, edit_link_Dialog):
    def __init__(self, mask, table, row, parent=None):
        super(New_link, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()):
            self.Start_Point.insertItem(i, icon, table.item(i, 0).text())
            self.End_Point.insertItem(i, icon, table.item(i, 0).text())
        self.Link.addItem(QIcon(QPixmap(":/icons/line.png")), "Line"+str(row))
        self.Link.setEnabled(False)
        self.Length.setValidator(mask)
        self.Length.setPlaceholderText('30.0')
