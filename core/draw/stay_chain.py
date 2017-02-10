# -*- coding: utf-8 -*-
from .modules import *

class chain_show(QDialog, edit_chain_Dialog):
    def __init__(self, mask, table, row, parent=None):
        super(chain_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()):
            self.Point1.insertItem(i, icon, table.item(i, 0).text())
            self.Point2.insertItem(i, icon, table.item(i, 0).text())
            self.Point3.insertItem(i, icon, table.item(i, 0).text())
        self.Chain.addItem(QIcon(QPixmap(":/icons/line.png")), "Chain"+str(row))
        self.Chain.setEnabled(False)
        self.p1_p2.setValidator(mask)
        self.p2_p3.setValidator(mask)
        self.p1_p3.setValidator(mask)
        self.p1_p2.setPlaceholderText('30.0')
        self.p2_p3.setPlaceholderText('30.0')
        self.p1_p3.setPlaceholderText('30.0')
