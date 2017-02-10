# -*- coding: utf-8 -*-
from .modules import *

class edit_stay_chain_show(QDialog, edit_chain_Dialog):
    Another_chain = pyqtSignal(int)
    def __init__(self, mask, table1, table2, pos, parent=None):
        super(edit_stay_chain_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        for i in range(table1.rowCount()):
            self.Point1.insertItem(i, icon, table1.item(i, 0).text())
            self.Point2.insertItem(i, icon, table1.item(i, 0).text())
            self.Point3.insertItem(i, icon, table1.item(i, 0).text())
        for i in range(table2.rowCount()): self.Chain.insertItem(i, QIcon(QPixmap(":/icons/equal.png")), table2.item(i, 0).text())
        self.Chain.setCurrentIndex(pos)
        self.p1_p2.setValidator(mask)
        self.p2_p3.setValidator(mask)
        self.p1_p3.setValidator(mask)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
    
    @pyqtSlot(int)
    def on_Chain_currentIndexChanged(self, index): self.Another_chain.emit(index)
    
    @pyqtSlot(int, int, int, float, float, float)
    def change_feedback(self, Point1, Point2, Point3, p1_p2, p2_p3, p1_p3):
        self.Point1.setCurrentIndex(Point1)
        self.Point2.setCurrentIndex(Point2)
        self.Point3.setCurrentIndex(Point3)
        self.p1_p2.setText(str(p1_p2))
        self.p1_p2.setPlaceholderText(str(p1_p2))
        self.p2_p3.setText(str(p2_p3))
        self.p2_p3.setPlaceholderText(str(p2_p3))
        self.p1_p3.setText(str(p1_p3))
        self.p1_p3.setPlaceholderText(str(p1_p3))
    
    @pyqtSlot(int)
    def on_Point1_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Point2_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Point3_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(str)
    def on_p1_p2_textEdited(self, p0): self.isOk()
    @pyqtSlot(str)
    def on_p2_p3_textEdited(self, p0): self.isOk()
    @pyqtSlot(str)
    def on_p1_p3_textEdited(self, p0): self.isOk()
    def isOk(self):
        self.p1 = self.Point1.currentIndex()
        self.p2 = self.Point2.currentIndex()
        self.p3 = self.Point3.currentIndex()
        self.p1_p2Val = self.p1_p2.text() if not self.p1_p2.text()in['', "n"] else self.p1_p2.placeholderText()
        self.p2_p3Val = self.p2_p3.text() if not self.p2_p3.text()in['', "n"] else self.p2_p3.placeholderText()
        self.p1_p3Val = self.p1_p3.text() if not self.p1_p3.text()in['', "n"] else self.p1_p3.placeholderText()
        n = not((self.p1 == self.p2)|(self.p2 == self.p3)|(self.p1 == self.p3)) and (float(self.p1_p2Val)!=0 or float(self.p2_p3Val)!=0 or float(self.p1_p3Val)!=0)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
