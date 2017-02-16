# -*- coding: utf-8 -*-
from .modules import *
from .Ui_batchMoving import Ui_Dialog as batchMoving_Dialog

class batchMoving_show(QDialog, batchMoving_Dialog):
    def __init__(self, Point, Parameter, parent=None):
        super(batchMoving_show, self).__init__(parent)
        self.setupUi(self)
        for i in range(1, len(Point)):
            self.Point_list.addItem('Point{}'.format(i))
        self.isReady()
    
    @pyqtSlot()
    def on_add_button_clicked(self):
        try:
            self.Move_list.addItem(self.Point_list.currentItem().text())
            self.Point_list.takeItem(self.Point_list.currentRow())
        except: pass
        self.isReady()
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        try:
            self.Point_list.addItem(self.Move_list.currentItem().text())
            self.Move_list.takeItem(self.Move_list.currentRow())
        except: pass
        self.isReady()
    @pyqtSlot(float)
    def on_XIncrease_valueChanged(self, p0): self.isReady()
    @pyqtSlot(float)
    def on_YIncrease_valueChanged(self, p0): self.isReady()
    @pyqtSlot()
    def isReady(self):
        n = self.XIncrease.value()!=0 or self.YIncrease.value()!=0
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n and self.Move_list.count()>=1)
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        moveList = [int(self.Move_list.item(e).text().replace("Point", "")) for e in range(self.Move_list.count())]
