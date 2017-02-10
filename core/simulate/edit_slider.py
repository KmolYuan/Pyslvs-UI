# -*- coding: utf-8 -*-
from .modules import *

class edit_slider_show(QDialog, edit_slider_Dialog):
    Another_slider = pyqtSignal(int)
    def __init__(self, table, table2, pos, parent=None):
        super(edit_slider_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()): self.Slider_Center.insertItem(i, icon, table1.item(i, 0).text())
        for i in range(table.rowCount()): self.Start.insertItem(i, icon, table.item(i, 0).text())
        for i in range(table.rowCount()): self.End.insertItem(i, icon, table.item(i, 0).text())
        for i in range(table2.rowCount()): self.Slider.insertItem(i, QIcon(QPixmap(":/icons/pointonx.png")), table3.item(i, 0).text())
        self.Slider.setCurrentIndex(pos)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    @pyqtSlot(int)
    def on_Slider_currentIndexChanged(self, index): self.Another_slider.emit(index)
    
    @pyqtSlot(int, int)
    def change_feedback(self, point, line):
        self.Slider_Center.setCurrentIndex(point)
        self.References.setCurrentIndex(line)
    
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
