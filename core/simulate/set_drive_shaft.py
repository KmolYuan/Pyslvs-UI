# -*- coding: utf-8 -*-
from .modules import *

class shaft_show(QDialog, edit_shaft_Dialog):
    def __init__(self, table, row, cen, ref, parent=None):
        super(shaft_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table.rowCount()):
            self.Shaft_Center.insertItem(i, icon, table.item(i, 0).text())
            self.References.insertItem(i, icon, table.item(i, 0).text())
        self.Shaft.addItem(QIcon(QPixmap(":/icons/circle.png")), "Shaft"+str(row))
        self.Shaft.setEnabled(False)
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
