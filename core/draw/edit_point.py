# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_edit_point import Ui_Dialog as edit_point_Dialog

class edit_point_show(QDialog, edit_point_Dialog):
    def __init__(self, mask, table, Points, pos=False, parent=None):
        super(edit_point_show, self).__init__(parent)
        self.setupUi(self)
        self.Points = Points
        if pos is False:
            self.Point.addItem(QIcon(QPixmap(":/icons/point.png")), "Point"+str(table.rowCount()))
            self.Point.setEnabled(False)
        else:
            for i in range(1, table.rowCount()): self.Point.insertItem(i, QIcon(QPixmap(":/icons/point.png")), table.item(i, 0).text())
            self.Point.setCurrentIndex(pos-1)
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index):
        self.X_coordinate.setText(str(self.Points[index-1]['x']))
        self.X_coordinate.setPlaceholderText(str(self.Points[index-1]['x']))
        self.Y_coordinate.setText(str(self.Points[index-1]['y']))
        self.Y_coordinate.setPlaceholderText(str(self.Points[index-1]['y']))
        self.Fix_Point.setCheckState(Qt.Checked if self.Points[index-1]['fix'] else Qt.Unchecked)
