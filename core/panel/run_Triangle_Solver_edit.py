# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver_edit import Ui_Dialog

class Triangle_Solver_edit_show(QDialog, Ui_Dialog):
    def __init__(self, Point, row, name='PLAP', parent=None):
        super(Triangle_Solver_edit_show, self).__init__(parent)
        self.setupUi(self)
        print(row)
        for i in range(len(Point)):
            self.p1.addItem(QIcon(QPixmap(":/icons/point.png")), 'Point{}'.format(i))
            self.p2.addItem(QIcon(QPixmap(":/icons/point.png")), 'Point{}'.format(i))
        for i in range(row):
            self.r1.addItem(QIcon(QPixmap(":/icons/TS.png")), 'Result{}'.format(i))
            self.r2.addItem(QIcon(QPixmap(":/icons/TS.png")), 'Result{}'.format(i))
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.turnDict)
        self.p1Result.setEnabled(row>0)
        self.p2Result.setEnabled(row>0)
        self.p3Result.setEnabled(row>0)
        self.on_type_currentIndexChanged(0)
        self.type.setCurrentIndex(self.type.findText(name))
    
    @pyqtSlot(int)
    def on_type_currentIndexChanged(self, pos):
        self.anglePanel.setEnabled(pos==0)
        self.len2Panel.setEnabled(pos==1)
        self.p3Panel.setEnabled(pos==2)
        if pos==0: pic = ":/icons/preview/PLAP.png"
        elif pos==1: pic = ":/icons/preview/PLLP.png"
        elif pos==2: pic = ":/icons/preview/PLPP.png"
        self.triangleImage.setPixmap(QPixmap(pic).scaledToWidth(590))
    
    def turnDict(self):
        self.condition = {
            'Type':self.type.currentText(),
            'p1':(self.x1.value(), self.y1.value()) if self.p1Customize.isChecked() else
                self.p1.currentText() if self.p1Exist.isChecked() else self.r1.currentIndex(),
            'p2':(self.x2.value(), self.y2.value()) if self.p2Customize.isChecked() else
                self.p2.currentText() if self.p2Exist.isChecked() else self.r2.currentIndex(),
            'len1':self.len1.value(),
            'other':bool(self.other.checkStateSet()),
        }
        if self.type.currentIndex()==0:
            PLAP = {'angle':self.angle.value()}
            self.condition.update(PLAP)
        elif self.type.currentIndex()==1:
            PLLP = {'len2':self.len2.value()}
            self.condition.update(PLLP)
        elif self.type.currentIndex()==2:
            PLPP = {'p3':(self.x3.value(), self.y3.value()) if self.p3Customize.isChecked() else
                self.p3.currentText() if self.p3Exist.isChecked() else self.r3.currentIndex()}
            self.condition.update(PLPP)
