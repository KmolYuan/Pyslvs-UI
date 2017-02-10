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
    def on_Start_Angle_valueChanged(self, p0): self.isOk()
    @pyqtSlot(float)
    def on_End_Angle_valueChanged(self, p0): self.isOk()
    @pyqtSlot()
    def on_Start_Angle_editingFinished(self): self.isOk()
    @pyqtSlot()
    def on_End_Angle_editingFinished(self): self.isOk()
    @pyqtSlot(int)
    def on_Shaft_Center_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_References_currentIndexChanged(self, index): self.isOk()
    def isOk(self):
        self.center = self.Shaft_Center.currentText()
        self.ref = self.References.currentText()
        self.start = self.Start_Angle.text()
        self.end = self.End_Angle.text()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.center!=self.ref and self.start!=self.end)
