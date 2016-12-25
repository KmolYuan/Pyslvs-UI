# -*- coding: utf-8 -*-
from .modules import *

class chain_show(QDialog, chain_Dialog):
    def __init__(self, parent=None):
        super(chain_show, self).__init__(parent)
        self.setupUi(self)
    
    def setUI(self, mask, table, row):
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()):
            self.Point1.insertItem(i, icon, table.item(i, 0).text())
            self.Point2.insertItem(i, icon, table.item(i, 0).text())
            self.Point3.insertItem(i, icon, table.item(i, 0).text())
        self.Chain_num.insertPlainText("Chain"+str(row))
        self.p1_p2.setValidator(mask)
        self.p2_p3.setValidator(mask)
        self.p1_p3.setValidator(mask)
