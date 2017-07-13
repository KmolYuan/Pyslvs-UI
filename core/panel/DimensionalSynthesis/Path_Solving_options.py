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
from .Ui_Path_Solving_options import Ui_Dialog

class Path_Solving_options_show(QDialog, Ui_Dialog):
    def __init__(self, linkage_type, algorithm, settings, parent=None):
        super(Path_Solving_options_show, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.setTabText(1, algorithm)
        self.linkage_type = linkage_type
        self.algorithm = algorithm
        self.init_PLTable()
        self.init_APTable()
        self.setArgs(settings)
        self.isOk()
    
    def init_PLTable(self):
        def writeTable(Coordinates, Length, Degrees):
            for i, (name, value) in enumerate(Coordinates):
                self.PLTable.insertRow(i)
                self.PLTable.setItem(i, 0, QTableWidgetItem(name))
                spinbox = QDoubleSpinBox()
                spinbox.setMaximum(10000.)
                spinbox.setMinimum(-10000.)
                spinbox.setValue(value)
                self.PLTable.setCellWidget(i, 1, spinbox)
            for i, (name, value) in enumerate(Length):
                self.PLTable.insertRow(i+len(Coordinates))
                self.PLTable.setItem(i+len(Coordinates), 0, QTableWidgetItem(name))
                spinbox = QDoubleSpinBox()
                spinbox.setMaximum(1000.)
                spinbox.setValue(value)
                self.PLTable.setCellWidget(i+len(Coordinates), 1, spinbox)
            for i, (name, value) in enumerate(Degrees):
                self.PLTable.insertRow(i+len(Coordinates)+len(Length))
                self.PLTable.setItem(i+len(Coordinates)+len(Length), 0, QTableWidgetItem(name))
                spinbox = QDoubleSpinBox()
                spinbox.setMaximum(360.)
                spinbox.setValue(value)
                self.PLTable.setCellWidget(i+len(Coordinates)+len(Length), 1, spinbox)
        if self.linkage_type=="4 Bar": writeTable(
            [('AxMax', 50.), ('AxMin', -50.), ('AyMax', 50.), ('AyMin', -50.), ('DxMax', 50.), ('DxMin', -50.), ('DyMax', 50.), ('DyMin', -50.)],
            [('IMax', 50.), ('IMin', 5.), ('LMax', 50.), ('LMin', 5.), ('FMax', 50.), ('FMin', 5.)],
            [('AMax', 360.), ('AMin', 0.)])
        for i in range(self.PLTable.rowCount()): self.PLTable.cellWidget(i, 1).valueChanged.connect(self.isOk)
    
    def init_APTable(self):
        def writeTable(Integers, Floats):
            for i, (name, value) in enumerate(Integers):
                self.APTable.insertRow(i)
                self.APTable.setItem(i, 0, QTableWidgetItem(name))
                spinbox = QSpinBox()
                spinbox.setMaximum(1000)
                spinbox.setValue(value)
                self.APTable.setCellWidget(i, 1, spinbox)
            for i, (name, value) in enumerate(Floats):
                self.APTable.insertRow(i+len(Integers))
                self.APTable.setItem(i+len(Integers), 0, QTableWidgetItem(name))
                spinbox = QDoubleSpinBox()
                spinbox.setMaximum(10.)
                spinbox.setValue(value)
                self.APTable.setCellWidget(i+len(Integers), 1, spinbox)
        if self.algorithm=="Genetic Algorithm": writeTable(
            [("Population Size", 250)],
            [("Crossover Rate", 0.95), ("Mutation Rate", 0.05), ("Winning Rate", 0.95), ("Delta value", 5.)])
        elif self.algorithm=="Firefly Algorithm": writeTable(
            [("Population Size", 40)],
            [("Alpha value", 0.01), ("Minimum Beta value", 0.2), ("Gamma value", 1.), ("Beta0 value", 1.)])
        elif self.algorithm=="Differential Evolution": writeTable(
            [("Evolutionary strategy (0-9)", 1), ("Population Size", 190)],
            [("Weight factor", 0.6), ("Recombination factor", 0.9)])
    
    def setArgs(self, PLnAP):
        self.maxGen.setValue(PLnAP['maxGen'])
        self.report.setValue(PLnAP['report'])
        for i, tag in enumerate(['AxMax', 'AxMin', 'AyMax', 'AyMin', 'DxMax', 'DxMin', 'DyMax', 'DyMin',
            'IMax', 'IMin', 'LMax', 'LMin', 'FMax', 'FMin', 'AMax', 'AMin']): self.PLTable.cellWidget(i, 1).setValue(PLnAP[tag])
        if self.algorithm=="Genetic Algorithm":
            for i, tag in enumerate(['nPop', 'pCross', 'pMute', 'pWin', 'bDelta']): self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
        elif self.algorithm=="Firefly Algorithm":
            for i, tag in enumerate(['n', 'alpha', 'betaMin', 'gamma', 'beta0']): self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
        elif self.algorithm=="Differential Evolution":
            for i, tag in enumerate(['strategy', 'NP', 'F', 'CR']): self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
    
    @pyqtSlot(int)
    @pyqtSlot(float)
    def isOk(self, r=None):
        n = True
        pre = 0
        for i in range(self.PLTable.rowCount()):
            if i%2==0: pre = self.PLTable.cellWidget(i, 1).value()
            elif i%2==1: n &= pre>=self.PLTable.cellWidget(i, 1).value()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
    
    @pyqtSlot()
    def on_setDefault_clicked(self): self.setArgs({'maxGen':1500, 'report':1,
        'AxMin':-50., 'AyMin':-50., 'DxMin':-50., 'DyMin':-50., 'IMin':5., 'LMin':5., 'FMin':5., 'AMin':0.,
        'AxMax':50., 'AyMax':50., 'DxMax':50., 'DyMax':50., 'IMax':50., 'LMax':50., 'FMax':50., 'AMax':360.,
        'algorithmPrams':{'nPop':250, 'pCross':0.95, 'pMute':0.05, 'pWin':0.95, 'bDelta':5.} if self.algorithm=="Genetic Algorithm" else
            {'n':40, 'alpha':0.01, 'betaMin':0.2, 'gamma':1., 'beta0':1.} if self.algorithm=="Firefly Algorithm" else
            {'strategy':1, 'NP':190, 'F':0.6, 'CR':0.9}})
