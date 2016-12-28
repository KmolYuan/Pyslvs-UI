# -*- coding: utf-8 -*-
from .modules import *

class shaft_show(QDialog, shaft_Dialog):
    def __init__(self, parent=None):
        super(shaft_show, self).__init__(parent)
        self.setupUi(self)
    
    def setUI(self, table, row, cen, ref):
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table1.rowCount()):
            self.Shaft_Center.insertItem(i, icon, table1.item(i, 0).text())
            self.References.insertItem(i, icon, table1.item(i, 0).text())
        self.Shaft_num.insertPlainText("Shaft"+str(row))
        self.Shaft_Center.setCurrentIndex(cen)
        self.References.setCurrentIndex(ref)
    
    @pyqtSlot(float)
    def on_Start_Angle_valueChanged(self, p0):
        self.Demo_angle.setMinimum(p0)
        self.Demo_angle.setValue(self.Demo_angle.minimum())
    
    @pyqtSlot(float)
    def on_End_Angle_valueChanged(self, p0):
        self.Demo_angle.setMaximum(p0)
        self.Demo_angle.setValue(self.Demo_angle.minimum())
    
    @pyqtSlot(bool)
    def on_Demo_angle_enable_toggled(self, checked): self.Demo_angle.setEnabled(checked)
