# -*- coding: utf-8 -*-
from .modules import *

class edit_rod_show(QDialog, edit_rod_Dialog):
    Another_rod = pyqtSignal(int)
    def __init__(self, table1, table2, pos, parent=None):
        super(edit_rod_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table1.rowCount()):
            self.Center.insertItem(i, icon, table1.item(i, 0).text())
            self.Start.insertItem(i, icon, table1.item(i, 0).text())
            self.End.insertItem(i, icon, table1.item(i, 0).text())
        for i in range(table2.rowCount()): self.Rod.insertItem(i, QIcon(QPixmap(":/icons/spring.png")), table2.item(i, 0).text())
        self.Rod.setCurrentIndex(pos)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    @pyqtSlot(int)
    def on_Rod_currentIndexChanged(self, index): self.Another_rod.emit(index)
    
    @pyqtSlot(int, int, int, float)
    def change_feedback(self, center, start, end, position):
        self.Center.setCurrentIndex(center)
        self.Start.setCurrentIndex(start)
        self.End.setCurrentIndex(end)
        self.Position.setValue(position)
    
    @pyqtSlot(int)
    def on_Center_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Start_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_End_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(float)
    def on_Position_valueChanged(self, p0): self.isOk()
    @pyqtSlot()
    def on_Position_editingFinished(self): self.isOk()
    def isOk(self):
        self.cen = self.Center.currentText()
        self.start = self.Start.currentText()
        self.end = self.End.currentText()
        self.pos = self.Position.text()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.cen!=self.start and self.start!=self.end and self.cen!=self.end)
