# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_edit_slider import Ui_Dialog as edit_slider_Dialog

class edit_slider_show(QDialog, edit_slider_Dialog):
    def __init__(self, Point, Sliders, pos=False, parent=None):
        super(edit_slider_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/pointonx.png"))
        self.Sliders = Sliders
        for i in range(len(Point)):
            name = 'Point{}'.format(i)
            self.Slider_Center.insertItem(i, icon, name)
            self.Start.insertItem(i, icon, name)
            self.End.insertItem(i, icon, name)
        if pos is False:
            self.Slider.addItem(iconSelf, 'Slider{}'.format(len(Sliders)))
            self.Slider.setEnabled(False)
        else:
            for i in range(len(Sliders)): self.Slider.insertItem(i, iconSelf, 'Slider{}'.format(i))
            self.Slider.setCurrentIndex(pos)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Slider_currentIndexChanged(self, index):
        if len(self.Sliders)>index:
            self.Slider_Center.setCurrentIndex(self.Sliders[index].cen)
            self.Start.setCurrentIndex(self.Sliders[index].start)
            self.End.setCurrentIndex(self.Sliders[index].end)
    
    @pyqtSlot(int)
    def on_Slider_Center_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_Start_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_End_currentIndexChanged(self, index): self.isOk()
    def isOk(self):
        self.slider = self.Slider_Center.currentIndex()
        self.start = self.Start.currentIndex()
        self.end = self.End.currentIndex()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(self.slider!=self.start and self.start!=self.end and self.slider!=self.end)
