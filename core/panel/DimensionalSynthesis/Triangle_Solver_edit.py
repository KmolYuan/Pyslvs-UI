# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2017 Yuan Chang
##E-mail: pyslvs@gmail.com
##
##This program is free software; you can redistribute it and/or modify
##it under the terms of the GNU Affero General Public License as published by
##the Free Software Foundation; either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU Affero General Public License for more details.
##
##You should have received a copy of the GNU Affero General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from ...QtModules import *
from .Ui_Triangle_Solver_edit import Ui_Dialog
from ...kernel.pyslvs_algorithm.TS import Direction

class Triangle_Solver_edit_show(QDialog, Ui_Dialog):
    def __init__(self, Point, row, Type='PLAP', parent=None, **condition):
        super(Triangle_Solver_edit_show, self).__init__(parent)
        self.setupUi(self)
        for i in range(len(Point)):
            for e in [self.p1, self.p2, self.p3]:
                e.addItem(QIcon(QPixmap(":/icons/point.png")), 'Point{}'.format(i))
        for i in range(row):
            for e in [self.r1, self.r2, self.r3]:
                e.addItem(QIcon(QPixmap(":/icons/TS.png")), 'Result{}'.format(i+1))
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
            if Type in ['PLAP', 'PLLP', 'PLPP']:
                self.len1.setValue(condition['len1'])
                self.other.setCheckState(Qt.Checked if condition['other'] else Qt.Unchecked)
            self.merge.setCurrentIndex(condition['merge'])
            if Type=='PLAP':
                self.angle.setValue(condition['angle'])
            elif Type=='PLLP':
                self.len2.setValue(condition['len2'])
            elif Type in ['PLPP', 'PPP']:
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
        for signal in [
                self.p1Exist.clicked, self.p1Result.clicked, self.p1Customize.clicked,
                self.p2Exist.clicked, self.p2Result.clicked, self.p2Customize.clicked,
                self.p3Exist.clicked, self.p3Result.clicked, self.p3Customize.clicked,
                self.p1.currentIndexChanged, self.r1.currentIndexChanged, self.x1.valueChanged, self.y1.valueChanged,
                self.p2.currentIndexChanged, self.r2.currentIndexChanged, self.x2.valueChanged, self.y2.valueChanged,
                self.p3.currentIndexChanged, self.r3.currentIndexChanged, self.x3.valueChanged, self.y3.valueChanged,
                self.len1.valueChanged, self.len1.valueChanged, self.angle.valueChanged]:
            signal.connect(self.isOk)
        self.isOk()
    
    @pyqtSlot(int)
    def on_type_currentIndexChanged(self, pos):
        self.anglePanel.setEnabled(pos==0)
        self.valuePanel.setEnabled(pos in [0, 1, 2])
        self.len2Panel.setEnabled(pos==1)
        self.p3Panel.setEnabled(pos in [2, 3])
        self.other.setEnabled(pos in [0, 1, 2])
        if pos==0:
            pic = ":/icons/preview/PLAP.png"
        elif pos==1:
            pic = ":/icons/preview/PLLP.png"
        elif pos==2:
            pic = ":/icons/preview/PLPP.png"
        elif pos==3:
            pic = ":/icons/preview/PPP.png"
        self.triangleImage.setPixmap(QPixmap(pic).scaledToWidth(560))
        for i in range(self.merge.count()):
            self.merge.removeItem(0)
        if pos==2:
            self.merge.insertItems(0, ["Points only", "Slider"])
        else:
            self.merge.insertItems(0, ["Points only", "Linking L0", "Linking R0", "Fixed Chain", "Linking L0 & R0"])
        self.merge.setCurrentIndex(0)
        self.isOk()
    
    @pyqtSlot(int)
    def on_merge_currentIndexChanged(self, pos):
        if pos!=-1:
            if self.type.currentIndex() in [0, 1, 3]:
                if pos==0:
                    pic = ":/icons/preview/TSMergePointsOnly.png"
                elif pos==1:
                    pic = ":/icons/preview/TSMergeL0.png"
                elif pos==2:
                    pic = ":/icons/preview/TSMergeR0.png"
                elif pos==3:
                    pic = ":/icons/preview/TSMergeChain.png"
                elif pos==4:
                    pic = ":/icons/preview/TSMergeL0R0.png"
            elif self.type.currentIndex()==2:
                if pos==0:
                    pic = ":/icons/preview/TSMergeSliderPointsOnly.png"
                elif pos==1:
                    pic = ":/icons/preview/TSMergeSlider.png"
            self.mergeImage.setPixmap(QPixmap(pic).scaledToWidth(560))
    
    @pyqtSlot()
    @pyqtSlot(int)
    @pyqtSlot(float)
    def isOk(self):
        condition = {
            'Type':self.type.currentText(),
            'p1':(self.x1.value(), self.y1.value()) if self.p1Customize.isChecked() else
                self.p1.currentText() if self.p1Exist.isChecked() else self.r1.currentIndex(),
            'p2':(self.x2.value(), self.y2.value()) if self.p2Customize.isChecked() else
                self.p2.currentText() if self.p2Exist.isChecked() else self.r2.currentIndex(),
            'merge':self.merge.currentIndex()}
        n = condition['p1']!=condition['p2']
        if self.type.currentIndex()==0:
            triangle = {
                'len1':self.len1.value(),
                'angle':self.angle.value(),
                'other':self.other.isChecked()}
            n &= triangle['len1']>=0
        elif self.type.currentIndex()==1:
            triangle = {
                'len1':self.len1.value(),
                'len2':self.len2.value(),
                'other':self.other.isChecked()}
            n &= triangle['len1']>=0 and triangle['len2']>=0
        elif self.type.currentIndex()==2:
            triangle = {
                'len1':self.len1.value(),
                'p3':(self.x3.value(), self.y3.value()) if self.p3Customize.isChecked() else
                self.p3.currentText() if self.p3Exist.isChecked() else self.r3.currentIndex(),
                'other':self.other.isChecked()}
            n &= triangle['len1']>=0 and triangle['p3']!=condition['p1'] and triangle['p3']!=condition['p2']
        elif self.type.currentIndex()==3:
            triangle = {
                'p3':(self.x3.value(), self.y3.value()) if self.p3Customize.isChecked() else
                self.p3.currentText() if self.p3Exist.isChecked() else self.r3.currentIndex()}
            n &= triangle['p3']!=condition['p1'] and triangle['p3']!=condition['p2']
        condition.update(triangle)
        self.condition = Direction(**condition)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
