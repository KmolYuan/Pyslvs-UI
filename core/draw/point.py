# -*- coding: utf-8 -*-
from .modules import *

class New_point(QDialog, point_Dialog):
    def __init__(self, parent=None):
        super(New_point, self).__init__(parent)
        self.setupUi(self)
    
    def setUI(self, mask, table):
        self.Point_num.insertPlainText("Point"+str(table.rowCount()))
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
