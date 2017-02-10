# -*- coding: utf-8 -*-
from .modules import *

class slider_show(QDialog, edit_slider_Dialog):
    def __init__(self, table, row, parent=None):
        super(slider_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()): self.Slider_Center.insertItem(i, icon, table.item(i, 0).text())
        for i in range(table.rowCount()): self.Start.insertItem(i, icon, table.item(i, 0).text())
        for i in range(table.rowCount()): self.End.insertItem(i, icon, table.item(i, 0).text())
        self.Slider.addItem(QIcon(QPixmap(":/icons/pointonx.png")), "Slider"+str(row))
        self.Slider.setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    @pyqtSlot(int)
    def on_Slider_Center_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Start_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_End_currentIndexChanged(self, index): self.isOk()
    def isOk(self):
        self.slider = self.Slider_Center.currentText()
        self.start = self.Start.currentText()
        self.end = self.End.currentText()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.slider!=self.start and self.start!=self.end and self.slider!=self.end)
