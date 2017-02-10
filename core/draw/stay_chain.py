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
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    @pyqtSlot(int)
    def on_Point1_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Point2_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Point3_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(str)
    def on_p1_p2_textEdited(self, p0): self.isOk()
    @pyqtSlot(str)
    def on_p2_p3_textEdited(self, p0): self.isOk()
    @pyqtSlot(str)
    def on_p1_p3_textEdited(self, p0): self.isOk()
    def isOk(self):
        self.p1 = self.Point1.currentText()
        self.p2 = self.Point2.currentText()
        self.p3 = self.Point3.currentText()
        self.p1_p2Val = self.p1_p2.text() if not self.p1_p2.text()in['', "n"] else self.p1_p2.placeholderText()
        self.p2_p3Val = self.p2_p3.text() if not self.p2_p3.text()in['', "n"] else self.p2_p3.placeholderText()
        self.p1_p3Val = self.p1_p3.text() if not self.p1_p3.text()in['', "n"] else self.p1_p3.placeholderText()
        n = not((self.p1 == self.p2)|(self.p2 == self.p3)|(self.p1 == self.p3)) and (float(self.p1_p2Val)!=0 or float(self.p2_p3Val)!=0 or float(self.p1_p3Val)!=0)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
