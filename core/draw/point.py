# -*- coding: utf-8 -*-
from .modules import *

class New_point(QDialog, point_Dialog):
    def __init__(self, mask, table, parent=None):
        super(New_point, self).__init__(parent)
        self.setupUi(self)
        self.Point_num.insertPlainText("Point"+str(table.rowCount()))
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
