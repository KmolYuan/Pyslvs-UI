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
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    @pyqtSlot(int)
    def on_Start_Point_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_End_Point_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(str)
    def on_Length_textEdited(self, p0): self.isOk()
    def isOk(self):
        self.len = self.Length.text() if not self.Length.text()in['', "n"] else self.Length.placeholderText()
        n = self.Start_Point.currentIndex()!=self.End_Point.currentIndex() and float(self.len)!=0
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
