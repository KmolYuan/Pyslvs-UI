# -*- coding: utf-8 -*-
from .modules import *

class New_link(QDialog, link_Dialog):
    def __init__(self, mask, table, row, parent=None):
        super(New_link, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()):
            self.Start_Point.insertItem(i, icon, table.item(i, 0).text())
            self.End_Point.insertItem(i, icon, table.item(i, 0).text())
        self.Link_num.insertPlainText("Line"+str(row))
        self.Length.setValidator(mask)
