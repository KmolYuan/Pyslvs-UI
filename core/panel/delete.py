# -*- coding: utf-8 -*-
from .modules import *

class deleteDlg(QDialog, delete_Dialog):
    def __init__(self, parent=None):
        super(deleteDlg, self).__init__(parent)
        self.setupUi(self)
    
    def setUI(self, deleteIcon, icon, table, pos):
        self.setWindowIcon(deleteIcon)
        for i in range(table.rowCount()):
            self.Entity.insertItem(i, icon, table.item(i, 0).text())
        self.Entity.setCurrentIndex(pos)
