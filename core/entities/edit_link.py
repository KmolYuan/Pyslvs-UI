# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_edit_link import Ui_Dialog as edit_link_Dialog

class edit_link_show(QDialog, edit_link_Dialog):
    def __init__(self, mask, Point, Lines, pos=False, parent=None):
        super(edit_link_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/line.png"))
        self.Point = Point
        self.Lines = Lines
        for i in range(len(Point)):
            name = 'Point{}'.format(i)
            self.Start_Point.insertItem(i, icon, name)
            self.End_Point.insertItem(i, icon, name)
        if pos is False:
            self.Link.addItem(iconSelf, 'Line{}'.format(len(Lines)))
            self.Link.setEnabled(False)
        else:
            for i in range(len(Lines)): self.Link.insertItem(i, iconSelf, 'Line{}'.format(i))
            self.Link.setCurrentIndex(pos)
        self.Length.setValidator(mask)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Link_currentIndexChanged(self, index):
        if len(self.Lines)>index:
            self.Start_Point.setCurrentIndex(self.Lines[index].start)
            self.End_Point.setCurrentIndex(self.Lines[index].end)
            self.Length.setText(str(self.Lines[index].len))
            self.Length.setPlaceholderText(str(self.Lines[index].len))
    
    @pyqtSlot(int)
    def on_Start_Point_currentIndexChanged(self, index):
        self.demoLen()
        self.isOk()
    @pyqtSlot(int)
    def on_End_Point_currentIndexChanged(self, index):
        self.demoLen()
        self.isOk()
    @pyqtSlot(str)
    def on_Length_textEdited(self, p0): self.isOk()
    def demoLen(self):
        start = self.Point[self.Start_Point.currentIndex()]
        end = self.Point[self.End_Point.currentIndex()]
        leng = str(round(((start.cx-end.cx)**2+(start.cy-end.cy)**2)**(1/2), 2))
        self.Length.setText(leng)
        self.Length.setPlaceholderText(leng)
    def isOk(self):
        self.len = self.Length.text() if (not 'n' in self.Length.text()) or (self.Length.text()!='') else self.Length.placeholderText()
        n = self.Start_Point.currentIndex()!=self.End_Point.currentIndex() and self.len!=0
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
