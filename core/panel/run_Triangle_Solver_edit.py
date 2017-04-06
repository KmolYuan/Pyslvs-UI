# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Triangle_Solver_edit import Ui_Dialog

class Triangle_Solver_edit_show(QDialog, Ui_Dialog):
    def __init__(self, Point, row, Type='PLAP', parent=None, **condition):
        super(Triangle_Solver_edit_show, self).__init__(parent)
        self.setupUi(self)
        self.Point = Point
        for i in range(len(Point)):
            for e in [self.p1, self.p2, self.p3]: e.addItem(QIcon(QPixmap(":/icons/point.png")), 'Point{}'.format(i))
        if len(Point)>1:
            for i in range(1, len(Point)): self.R1.addItem(QIcon(QPixmap(":/icons/point.png")), 'Point{}'.format(i))
        for i in range(row):
            for e in [self.r1, self.r2, self.r3]: e.addItem(QIcon(QPixmap(":/icons/TS.png")), 'Result{}'.format(i+1))
        self.R1Exist.setEnabled(len(Point)>1)
        self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.turn2Dict)
        self.p1Result.setEnabled(row>0)
        self.p2Result.setEnabled(row>0)
        self.p3Result.setEnabled(row>0)
        self.on_type_currentIndexChanged(0)
        self.type.setCurrentIndex(self.type.findText(Type))
        if condition:
            if type(condition['p1'])==tuple:
                self.p1Customize.setChecked(True)
                self.x1.setValue(condition['p1'][0])
                self.y1.setValue(condition['p1'][1])
            elif type(condition['p1'])==int:
                self.p1Result.setChecked(True)
                self.r1.setCurrentIndex(condition['p1'])
            elif type(condition['p1'])==str:
                self.p1Exist.setChecked(True)
                self.p1.setCurrentIndex(int(condition['p1'].replace('Point', '')))
            if type(condition['p2'])==tuple:
                self.p2Customize.setChecked(True)
                self.x2.setValue(condition['p2'][0])
                self.y2.setValue(condition['p2'][1])
            elif type(condition['p2'])==int:
                self.p2Result.setChecked(True)
                self.r2.setCurrentIndex(condition['p2'])
            elif type(condition['p2'])==str:
                self.p2Exist.setChecked(True)
                self.p2.setCurrentIndex(int(condition['p2'].replace('Point', '')))
            self.len1.setValue(condition['len1'])
            self.other.setCheckState(Qt.Checked if condition['other'] else Qt.Unchecked)
            self.merge.setCurrentIndex(condition['merge'])
            if Type=='PLAP': self.angle.setValue(condition['angle'])
            elif Type=='PLLP': self.len2.setValue(condition['len2'])
            elif Type=='PLPP':
                if type(condition['p3'])==tuple:
                    self.p3Customize.setChecked(True)
                    self.x3.setValue(condition['p3'][0])
                    self.y3.setValue(condition['p3'][1])
                elif type(condition['p3'])==int:
                    self.p3Result.setChecked(True)
                    self.r3.setCurrentIndex(condition['p3'])
                elif type(condition['p3'])==str:
                    self.p3Exist.setChecked(True)
                    self.p3.setCurrentIndex(int(condition['p3'].replace('Point', '')))
    
    @pyqtSlot(int)
    def on_type_currentIndexChanged(self, pos):
        self.anglePanel.setEnabled(pos==0)
        self.len2Panel.setEnabled(pos==1)
        self.p3Panel.setEnabled(pos==2)
        if pos==0: pic = ":/icons/preview/PLAP.png"
        elif pos==1: pic = ":/icons/preview/PLLP.png"
        elif pos==2: pic = ":/icons/preview/PLPP.png"
        self.triangleImage.setPixmap(QPixmap(pic).scaledToWidth(560))
        for i in range(self.merge.count()): self.merge.removeItem(0)
        if pos==2: self.merge.insertItems(0, ["Points only", "Slider"])
        else: self.merge.insertItems(0, ["Points only", "Linking L0", "Linking R0", "Stay Chain", "Linking L0 & R0"])
        self.merge.setCurrentIndex(0)
    
    @pyqtSlot(int)
    def on_merge_currentIndexChanged(self, pos):
        if pos!=-1:
            if self.type.currentIndex()!=2:
                if pos==0: pic = ":/icons/preview/TSMergePointsOnly.png"
                elif pos==1: pic = ":/icons/preview/TSMergeL0.png"
                elif pos==2: pic = ":/icons/preview/TSMergeR0.png"
                elif pos==3: pic = ":/icons/preview/TSMergeChain.png"
                elif pos==4: pic = ":/icons/preview/TSMergeL0R0.png"
            else:
                if pos==0: pic = ":/icons/preview/TSMergeSliderPointsOnly.png"
                elif pos==1: pic = ":/icons/preview/TSMergeSlider.png"
            self.mergeImage.setPixmap(QPixmap(pic).scaledToWidth(560))
    
    def turn2Dict(self):
        self.condition = {
            'Type':self.type.currentText(),
            'p1':(self.x1.value(), self.y1.value()) if self.p1Customize.isChecked() else
                self.p1.currentText() if self.p1Exist.isChecked() else self.r1.currentIndex(),
            'p2':(self.x2.value(), self.y2.value()) if self.p2Customize.isChecked() else
                self.p2.currentText() if self.p2Exist.isChecked() else self.r2.currentIndex(),
            'len1':self.len1.value() if self.len1Customize.isChecked() else False,
            'other':bool(self.other.checkState()),
            'merge':self.merge.currentIndex(),
            'result':self.R1.currentIndex()+1 if self.R1Exist.isChecked() else False,
        }
        if self.type.currentIndex()==0:
            PLAP = {'angle':self.angle.value() if self.angleCustomize.isChecked() else False}
            self.condition.update(PLAP)
        elif self.type.currentIndex()==1:
            PLLP = {'len2':self.len2.value() if self.len2Customize.isChecked() else False}
            self.condition.update(PLLP)
        elif self.type.currentIndex()==2:
            PLPP = {'p3':(self.x3.value(), self.y3.value()) if self.p3Customize.isChecked() else
                self.p3.currentText() if self.p3Exist.isChecked() else self.r3.currentIndex()}
            self.condition.update(PLPP)
