# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_replacePoint import Ui_Dialog as replacePoint_Dialog

class replacePoint_show(QDialog, replacePoint_Dialog):
    def __init__(self, icon, table, pos, parent=None):
        super(replacePoint_show, self).__init__(parent)
        self.setupUi(self)
        for i in range(table.rowCount()): self.Prv.insertItem(i, icon, table.item(i, 0).text())
        for i in range(table.rowCount()): self.Next.insertItem(i, icon, table.item(i, 0).text())
        self.Prv.setCurrentIndex(pos)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Prv_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Next_currentIndexChanged(self, index): self.isOk()
    def isOk(self): self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.Prv.currentIndex()!=self.Next.currentIndex())
