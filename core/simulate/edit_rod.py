# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_edit_rod import Ui_Dialog as edit_rod_Dialog

class edit_rod_show(QDialog, edit_rod_Dialog):
    def __init__(self, Point, Rods, pos=False, parent=None):
        super(edit_rod_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/spring.png"))
        self.Rods = Rods
        for i in range(len(Point)):
            name = 'Point{}'.format(i)
            self.Center.insertItem(i, icon, name)
            self.Start.insertItem(i, icon, name)
            self.End.insertItem(i, icon, name)
        if pos is False:
            self.Rod.addItem(iconSelf, 'Rod{}'.format(len(Rods)))
            self.Rod.setEnabled(False)
        else:
            for i in range(len(Rods)): self.Rod.insertItem(i, iconSelf, 'Rod{}'.format(i))
            self.Rod.setCurrentIndex(pos)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Rod_currentIndexChanged(self, index):
        if len(self.Rods)>index:
            self.Center.setCurrentIndex(self.Rods[index].cen)
            self.Start.setCurrentIndex(self.Rods[index].start)
            self.End.setCurrentIndex(self.Rods[index].end)
            self.Position.setValue(self.Rods[index].pos)
    
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
        self.cen = self.Center.currentIndex()
        self.start = self.Start.currentIndex()
        self.end = self.End.currentIndex()
        self.pos = self.Position.text()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.cen!=self.start and self.start!=self.end and self.cen!=self.end)
