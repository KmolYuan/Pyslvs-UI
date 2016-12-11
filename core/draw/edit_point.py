# -*- coding: utf-8 -*-
from .__init__ import *

class edit_point_show(QDialog, edit_point_Dialog):
    Another_point = pyqtSignal(int)
    def __init__(self, parent=None):
        super(edit_point_show, self).__init__(parent)
        self.setupUi(self)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index): self.Another_point.emit(index+1)
    
    @pyqtSlot(float, float, bool)
    def change_feedback(self, x, y, fix):
        self.X_coordinate.setPlaceholderText(str(x))
        self.Y_coordinate.setPlaceholderText(str(y))
        if fix: fixed = Qt.Checked
        else: fixed = Qt.Unchecked
        self.Fix_Point.setCheckState(fixed)
