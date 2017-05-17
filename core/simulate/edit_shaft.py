# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_edit_shaft import Ui_Dialog as edit_shaft_Dialog

class edit_shaft_show(QDialog, edit_shaft_Dialog):
    def __init__(self, Point, Shafts, pos=False, parent=None):
        super(edit_shaft_show, self).__init__(parent)
        self.setupUi(self)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/circle.png"))
        self.Shafts = Shafts
        for i, p in enumerate(Point):
            name = 'Point{}'.format(i)
            if p.fix: self.Center.insertItem(i, icon, name)
            else: self.References.insertItem(i, icon, name)
        if pos is False:
            self.Shaft.addItem(iconSelf, 'Shaft{}'.format(len(Shafts)))
            self.Shaft.setEnabled(False)
        else:
            for i in range(len(Shafts)): self.Shaft.insertItem(i, iconSelf, 'Shaft{}'.format(i))
            self.Shaft.setCurrentIndex(pos)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index):
        if len(self.Shafts)>index:
            self.Center.setCurrentIndex(self.Center.findText('Point{}'.format(self.Shafts[index].cen)))
            self.References.setCurrentIndex(self.References.findText('Point{}'.format(self.Shafts[index].ref)))
            self.Start_Angle.setValue(self.Shafts[index].start)
            self.End_Angle.setValue(self.Shafts[index].end)
    
    @pyqtSlot(float)
    def on_Start_Angle_valueChanged(self, p0): self.isOk()
    @pyqtSlot(float)
    def on_End_Angle_valueChanged(self, p0): self.isOk()
    @pyqtSlot()
    def on_Start_Angle_editingFinished(self): self.isOk()
    @pyqtSlot()
    def on_End_Angle_editingFinished(self): self.isOk()
    @pyqtSlot(int)
    def on_Center_currentIndexChanged(self, index): self.isOk()
    @pyqtSlot(int)
    def on_References_currentIndexChanged(self, index): self.isOk()
    def isOk(self):
        try: self.center = int(self.Center.currentText().replace('Point', ''))
        except: self.center = None
        try: self.ref = int(self.References.currentText().replace('Point', ''))
        except: self.ref = None
        self.start = self.Start_Angle.text()
        self.end = self.End_Angle.text()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(
            self.center!=None and self.ref!=None and self.center!=self.ref and self.Start_Angle.value()<self.End_Angle.value())
