# -*- coding: utf-8 -*-
from .modules import *

class rod_show(QDialog, rod_Dialog):
    def __init__(self, table, row, parent=None):
        super(rod_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table1.rowCount()):
            self.Start.insertItem(i, icon, table.item(i, 0).text())
            self.End.insertItem(i, icon, table.item(i, 0).text())
        self.Rod_num.insertPlainText("Rod"+str(row))
