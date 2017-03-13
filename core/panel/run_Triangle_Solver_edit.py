# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver_edit import Ui_Dialog

class Triangle_Solver_edit_show(QDialog, Ui_Dialog):
    def __init__(self, Point, name='PLAP', parent=None):
        super(Triangle_Solver_edit_show, self).__init__(parent)
        self.setupUi(self)
        self.type.setCurrentIndex(0 if name=='PLAP' else 1)
        for i in range(len(Point)):
            self.p1.addItem(QIcon(QPixmap(":/icons/point.png")), 'Point{}'.format(i))
            self.p2.addItem(QIcon(QPixmap(":/icons/point.png")), 'Point{}'.format(i))
    
    @pyqtSlot(int)
    def on_type_currentIndexChanged(self, pos):
        self.anglePanel.setEnabled(pos==0)
        self.len2Panel.setEnabled(pos==1)
