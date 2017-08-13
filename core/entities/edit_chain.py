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

from ..QtModules import *
from .Ui_edit_chain import Ui_Dialog as edit_Dialog

class edit_chain_show(QDialog, edit_Dialog):
    def __init__(self, mask, Point, Chains, pos=False, parent=None):
        super(edit_chain_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        icon = QIcon(QPixmap(":/icons/point.png"))
        iconSelf = QIcon(QPixmap(":/icons/line.png"))
        self.Point = Point
        self.Chains = Chains
        for i in range(len(Point)):
            name = 'Point{}'.format(i)
            self.Point1.insertItem(i, icon, name)
            self.Point2.insertItem(i, icon, name)
            self.Point3.insertItem(i, icon, name)
        if pos is False:
            self.Chain.addItem(iconSelf, 'Chain{}'.format(len(Chains)))
            self.Chain.setEnabled(False)
        else:
            for i in range(len(Chains)):
                self.Chain.insertItem(i, iconSelf, 'Chain{}'.format(i))
            self.Chain.setCurrentIndex(pos)
        self.p1_p2.setValidator(mask)
        self.p2_p3.setValidator(mask)
        self.p1_p3.setValidator(mask)
        self.isOk()
    
    @pyqtSlot(int)
    def on_Chain_currentIndexChanged(self, index):
        if len(self.Chains)>index:
            self.Point1.setCurrentIndex(self.Chains[index].p1)
            self.Point2.setCurrentIndex(self.Chains[index].p2)
            self.Point3.setCurrentIndex(self.Chains[index].p3)
            self.p1_p2.setText(str(self.Chains[index].p1p2))
            self.p1_p2.setPlaceholderText(str(self.Chains[index].p1p2))
            self.p2_p3.setText(str(self.Chains[index].p2p3))
            self.p2_p3.setPlaceholderText(str(self.Chains[index].p2p3))
            self.p1_p3.setText(str(self.Chains[index].p1p3))
            self.p1_p3.setPlaceholderText(str(self.Chains[index].p1p3))
    
    @pyqtSlot(int)
    def on_Point1_currentIndexChanged(self, index):
        self.demoLen()
        self.isOk()
    @pyqtSlot(int)
    def on_Point2_currentIndexChanged(self, index):
        self.demoLen()
        self.isOk()
    @pyqtSlot(int)
    def on_Point3_currentIndexChanged(self, index):
        self.demoLen()
        self.isOk()
    @pyqtSlot(str)
    def on_p1_p2_textEdited(self, p0):
        self.isOk()
    @pyqtSlot(str)
    def on_p2_p3_textEdited(self, p0):
        self.isOk()
    @pyqtSlot(str)
    def on_p1_p3_textEdited(self, p0):
        self.isOk()
    
    def demoLen(self):
        p1 = self.Point[self.Point1.currentIndex()]
        p2 = self.Point[self.Point2.currentIndex()]
        p3 = self.Point[self.Point3.currentIndex()]
        p1p2 = str(round(((p1.cx-p2.cx)**2+(p1.cy-p2.cy)**2)**(1/2), 2))
        self.p1_p2.setText(p1p2)
        self.p1_p2.setPlaceholderText(p1p2)
        p2p3 = str(round(((p2.cx-p3.cx)**2+(p2.cy-p3.cy)**2)**(1/2), 2))
        self.p2_p3.setText(p2p3)
        self.p2_p3.setPlaceholderText(p2p3)
        p1p3 = str(round(((p1.cx-p3.cx)**2+(p1.cy-p3.cy)**2)**(1/2), 2))
        self.p1_p3.setText(p1p3)
        self.p1_p3.setPlaceholderText(p1p3)
    
    def isOk(self):
        self.p1 = self.Point1.currentIndex()
        self.p2 = self.Point2.currentIndex()
        self.p3 = self.Point3.currentIndex()
        vals = [text.text() if (not 'n' in text.text()) or (text.text()!='') else text.placeholderText()
            for text in [self.p1_p2, self.p2_p3, self.p1_p3]]
        self.p1_p2Val, self.p2_p3Val, self.p1_p3Val = vals
        n = not((self.p1==self.p2)|(self.p2==self.p3)|(self.p1==self.p3)) and (float(self.p1_p2Val)!=0 or float(self.p2_p3Val)!=0 or float(self.p1_p3Val)!=0)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
