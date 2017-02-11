# -*- coding: utf-8 -*-
from .modules import *

class edit_slider_show(QDialog, edit_slider_Dialog):
    Another_slider = pyqtSignal(int)
    def __init__(self, table1, table2, pos=False, parent=None):
        super(edit_slider_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/pointonx.png"))
        for i in range(table1.rowCount()):
            self.Slider_Center.insertItem(i, icon, table1.item(i, 0).text())
            self.Start.insertItem(i, icon, table1.item(i, 0).text())
            self.End.insertItem(i, icon, table1.item(i, 0).text())
        if pos is False:
            self.Slider.addItem(iconSelf, "Slider"+str(table2.rowCount()))
            self.Slider.setEnabled(False)
        else:
            for i in range(table2.rowCount()): self.Slider.insertItem(i, iconSelf, table2.item(i, 0).text())
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
