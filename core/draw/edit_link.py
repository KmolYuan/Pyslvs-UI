# -*- coding: utf-8 -*-
from .modules import *

class edit_link_show(QDialog, edit_link_Dialog):
    Another_line = pyqtSignal(int)
    def __init__(self, mask, table1, table2, pos, parent=None):
        super(edit_link_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table1.rowCount()):
            self.Start_Point.insertItem(i, icon, table1.item(i, 0).text())
            self.End_Point.insertItem(i, icon, table1.item(i, 0).text())
        for i in range(table2.rowCount()): self.Link.insertItem(i, QIcon(QPixmap(":/icons/line.png")), table2.item(i, 0).text())
        self.Link.setCurrentIndex(pos)
        self.Length.setValidator(mask)
    
    @pyqtSlot(int)
    def on_Link_currentIndexChanged(self, index): self.Another_line.emit(index)
    
    @pyqtSlot(int, int, float)
    def change_feedback(self, start, end, len):
        self.Start_Point.setCurrentIndex(start)
        self.End_Point.setCurrentIndex(end)
        self.Length.setText(str(len))
        self.Length.setPlaceholderText(str(len))
