# -*- coding: utf-8 -*-
from .modules import *

class edit_slider_show(QDialog, edit_slider_Dialog):
    Another_slider = pyqtSignal(int)
    def __init__(self, table1, table2, table3, pos, parent=None):
        super(edit_slider_show, self).__init__(parent)
        self.setupUi(self)
        for i in range(table1.rowCount()): self.Slider_Center.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table1.item(i, 0).text())
        for i in range(table2.rowCount()): self.References.insertItem(i, QIcon(QPixmap(":/icons/line.png")), table2.item(i, 0).text())
        for i in range(table3.rowCount()): self.Slider.insertItem(i, QIcon(QPixmap(":/icons/pointonx.png")), table3.item(i, 0).text())
        self.Slider.setCurrentIndex(pos)
    
    @pyqtSlot(int)
    def on_Slider_currentIndexChanged(self, index): self.Another_slider.emit(index)
    
    @pyqtSlot(int, int)
    def change_feedback(self, point, line):
        self.Slider_Center.setCurrentIndex(point)
        self.References.setCurrentIndex(line)
