# -*- coding: utf-8 -*-
from ..QtModules import *
from ..graphics.color import colorIcons
from .Ui_batchMoving import Ui_Dialog as batchMoving_Dialog

class batchMoving_show(QDialog, batchMoving_Dialog):
    def __init__(self, Point, Parameter, parent=None):
        super(batchMoving_show, self).__init__(parent)
        self.setupUi(self)
        self.Point = Point
        for i, e in enumerate(self.Point): self.Point_list.addItem(
            QListWidgetItem(colorIcons()[e.color], 'Point{}'.format(i)))
        self.isReady()
    
    @pyqtSlot()
    def on_add_button_clicked(self):
        try:
            item = self.Point_list.currentItem()
            self.Move_list.addItem(QListWidgetItem(item.icon(), item.text()))
            self.Point_list.takeItem(self.Point_list.currentRow())
        except: pass
        self.isReady()
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        try:
            item = self.Move_list.currentItem()
            self.Point_list.addItem(QListWidgetItem(item.icon(), item.text()))
            self.Move_list.takeItem(self.Move_list.currentRow())
        except: pass
        self.isReady()
    @pyqtSlot()
    def on_addAll_button_clicked(self):
        for i in range(self.Point_list.count()):
            item = self.Point_list.item(0)
            self.Move_list.addItem(QListWidgetItem(item.icon(), item.text()))
            self.Point_list.takeItem(0)
        self.isReady()
    @pyqtSlot()
    def on_removeAll_botton_clicked(self):
        for i in range(self.Move_list.count()):
            item = self.Move_list.item(0)
            self.Point_list.addItem(QListWidgetItem(item.icon(), item.text()))
            self.Move_list.takeItem(0)
        self.isReady()
    @pyqtSlot(QListWidgetItem)
    def on_Point_list_itemDoubleClicked(self, item): self.on_add_button_clicked()
    @pyqtSlot(QListWidgetItem)
    def on_Move_list_itemDoubleClicked(self, item): self.on_remove_botton_clicked()
    
    @pyqtSlot(float)
    def on_XIncrease_valueChanged(self, p0): self.isReady()
    @pyqtSlot(float)
    def on_YIncrease_valueChanged(self, p0): self.isReady()
    @pyqtSlot()
    def isReady(self):
        n = self.XIncrease.value()!=0 or self.YIncrease.value()!=0
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n and self.Move_list.count()>=1)
