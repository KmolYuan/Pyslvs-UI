# -*- coding: utf-8 -*-
from .modules import *

class edit_point_show(QDialog, edit_point_Dialog):
    Another_point = pyqtSignal(int)
    def __init__(self, parent=None):
        super(edit_point_show, self).__init__(parent)
        self.setupUi(self)
    
    def setUI(self, mask, table, pos):
        for i in range(1, table.rowCount()): self.Point.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
        self.Point.setCurrentIndex(pos-1)
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index): self.Another_point.emit(index+1)
    
    @pyqtSlot(float, float, bool)
    def change_feedback(self, x, y, fix):
        self.X_coordinate.setPlaceholderText(str(x))
        self.Y_coordinate.setPlaceholderText(str(y))
        if fix: fixed = Qt.Checked
        else: fixed = Qt.Unchecked
        self.Fix_Point.setCheckState(fixed)
