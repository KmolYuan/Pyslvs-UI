# -*- coding: utf-8 -*-
from .modules import *

class rod_show(QDialog, edit_rod_Dialog):
    def __init__(self, table, row, parent=None):
        super(rod_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()):
            self.Center.insertItem(i, icon, table.item(i, 0).text())
            self.Start.insertItem(i, icon, table.item(i, 0).text())
            self.End.insertItem(i, icon, table.item(i, 0).text())
        self.Rod.addItem(QIcon(QPixmap(":/icons/spring.png")), "Rod"+str(row))
        self.Rod.setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    @pyqtSlot(int)
    def on_Center_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Start_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_End_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(float)
    def on_Position_valueChanged(self, p0): self.isOk()
    @pyqtSlot()
    def on_Position_editingFinished(self): self.isOk()
    def isOk(self):
        self.cen = self.Center.currentText()
        self.start = self.Start.currentText()
        self.end = self.End.currentText()
        self.pos = self.Position.text()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.cen!=self.start and self.start!=self.end and self.cen!=self.end)
