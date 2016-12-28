# -*- coding: utf-8 -*-
from .modules import *

class edit_rod_show(QDialog, edit_rod_Dialog):
    Another_rod = pyqtSignal(int)
    def __init__(self, parent=None):
        super(edit_rod_show, self).__init__(parent)
        self.setupUi(self)
    
    def setUI(self, table1, table2, pos):
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table1.rowCount()):
            self.Start.insertItem(i, icon, table1.item(i, 0).text())
            self.End.insertItem(i, icon, table1.item(i, 0).text())
        for i in range(table2.rowCount()): self.Rod.insertItem(i, QIcon(QPixmap(":/icons/spring.png")), table2.item(i, 0).text())
        self.Rod.setCurrentIndex(pos)
    
    @pyqtSlot(int)
    def on_Rod_currentIndexChanged(self, index): self.Another_rod.emit(index)
    
    @pyqtSlot(int, int, int, float)
    def change_feedback(self, center, start, end, position):
        self.Center.setCurrentIndex(center)
        self.Start.setCurrentIndex(start)
        self.End.setCurrentIndex(end)
        self.Position.setValue(position)
