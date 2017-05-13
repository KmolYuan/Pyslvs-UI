# -*- coding: utf-8 -*-
from ..QtModules import *
from ..graphics.color import colorName, colorIcons
from .Ui_edit_point import Ui_Dialog as edit_point_Dialog

class edit_point_show(QDialog, edit_point_Dialog):
    def __init__(self, mask, Points, pos=False, parent=None):
        super(edit_point_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        self.Points = Points
        for i, e in enumerate(colorName()): self.Color.insertItem(i, colorIcons()[e], e)
        if pos is False:
            self.Point.addItem(icon, 'Point{}'.format(len(Points)))
            self.Point.setEnabled(False)
            self.Color.setCurrentIndex(self.Color.findText('Green'))
        else:
            for i in range(1, len(Points)): self.Point.insertItem(i, icon, 'Point{}'.format(i))
            self.Point.setCurrentIndex(pos-1)
        self.X_coordinate.setValidator(mask)
        self.Y_coordinate.setValidator(mask)
    
    @pyqtSlot(int)
    def on_Point_currentIndexChanged(self, index):
        if len(self.Points)-1>index:
            self.X_coordinate.setText(str(self.Points[index+1].x))
            self.X_coordinate.setPlaceholderText(str(self.Points[index+1].x))
            self.Y_coordinate.setText(str(self.Points[index+1].y))
            self.Y_coordinate.setPlaceholderText(str(self.Points[index+1].y))
            self.Fix_Point.setCheckState(Qt.Checked if self.Points[index+1].fix else Qt.Unchecked)
            self.Color.setCurrentIndex(self.Color.findText(self.Points[index+1].color))
