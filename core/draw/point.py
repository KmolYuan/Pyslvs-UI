# -*- coding: utf-8 -*-
from .modules import *

class New_point(QDialog, edit_point_Dialog):
    def __init__(self, mask, table, parent=None):
        super(New_point, self).__init__(parent)
        self.setupUi(self)
        self.Point.addItem(QIcon(QPixmap(":/icons/point.png")), "Point"+str(table.rowCount()))
        self.Point.setEnabled(False)
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
        self.X_coordinate.setPlaceholderText('0.0')
        self.Y_coordinate.setPlaceholderText('0.0')
