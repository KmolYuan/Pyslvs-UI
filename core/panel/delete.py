# -*- coding: utf-8 -*-
from .modules import *

class deleteDlg(QDialog, delete_Dialog):
    def __init__(self, deleteIcon, icon, table, pos, parent=None):
        super(deleteDlg, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(deleteIcon)
        for i in range(table.rowCount()): self.Entity.insertItem(i, icon, table.item(i, 0).text())
        self.Entity.setCurrentIndex(pos)
