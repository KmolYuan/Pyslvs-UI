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
from ...info.info import html

class Path_Solving_options_show(QDialog, Ui_Dialog):
    def __init__(self, algorithm, settings, parent=None):
        super(Path_Solving_options_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.tabWidget.setTabText(1, algorithm)
        self.algorithm = algorithm
        self.init_PLTable()
        self.init_APTable()
        for table in [self.APTable, self.PLTable]:
            table.setColumnWidth(0, 200)
            table.setColumnWidth(1, 90)
        self.setArgs(settings)
        self.isOk()
    
    def init_PLTable(self):
        def writeTable(Length, Degrees):
            i = 0
            for Types, maxV, minV in zip([Length, Degrees], [1000., 360.], [0.1, 0.]):
                for name, vname, tooltip in Types:
                    self.PLTable.insertRow(i)
                    name_cell = QTableWidgetItem(name)
                    name_cell.setToolTip(tooltip)
                    self.PLTable.setItem(i, 0, name_cell)
                    spinbox = QDoubleSpinBox()
                    spinbox.setMaximum(maxV)
                    spinbox.setMinimum(minV)
                    spinbox.setToolTip(vname)
                    self.PLTable.setCellWidget(i, 1, spinbox)
                    i += 1
        writeTable(
            Length=[
                ("Input linkage maximum", 'IMax', html("This value holds with the maximum random number of input linkage.")),
                ("Input linkage minimum", 'IMin', html("This value holds with the minimum random number of input linkage.")),
                ("Connected linkage maximum", 'LMax', html("This value holds with the maximum random number of connected linkage.")),
                ("Connected linkage minimum", 'LMin', html("This value holds with the minimum random number of connected linkage.")),
                ("Follower linkage maximum", 'FMax', html("This value holds with the maximum random number of follower linkage.")),
                ("Follower linkage minimum", 'FMin', html("This value holds with the minimum random number of follower linkage."))
            ],
            Degrees=[
                ("Angle maximum", 'AMax', html("This value holds with the maximum angle of input linkage.")),
                ("Angle minimum", 'AMin', html("This value holds with the minimum angle of input linkage."))
            ])
        for i in range(self.PLTable.rowCount()):
            self.PLTable.cellWidget(i, 1).valueChanged.connect(self.isOk)
    
    def init_APTable(self):
        def writeTable(Integers=list(), Floats=list()):
            i = 0
            for Types, box, maxV in zip([Integers, Floats], [QSpinBox, QDoubleSpinBox], [9, 10.]):
                for name, vname, tooltip in Types:
                    self.APTable.insertRow(i)
                    name_cell = QTableWidgetItem(name)
                    name_cell.setToolTip(tooltip)
                    self.APTable.setItem(i, 0, name_cell)
                    spinbox = box()
                    spinbox.setMaximum(maxV)
                    spinbox.setToolTip(vname)
                    self.APTable.setCellWidget(i, 1, spinbox)
                    i += 1
        if self.algorithm=="Genetic Algorithm":
            writeTable(
                Floats=[
                    ("Crossover Rate", 'pCross', html("The chance of crossover.")),
                    ("Mutation Rate", 'pMute', html("The chance of mutation.")),
                    ("Winning Rate", 'pWin', html("The chance of winning.")),
                    ("Delta value", 'bDelta', html("The power value when matching chromosome."))
                ])
        elif self.algorithm=="Firefly Algorithm":
            writeTable(
                Floats=[
                    ("Alpha value", 'alpha', html("Alpha value is the step size of the firefly.")),
                    ("Minimum Beta value", 'betaMin', html("The minimal attraction, must not less than this.")),
                    ("Gamma value", 'gamma', html("Beta will multiplied by exponential power value with this weight factor.")),
                    ("Beta0 value", 'beta0', html("The attraction of two firefly in 0 distance."))
                ])
        elif self.algorithm=="Differential Evolution":
            writeTable(
                Integers=[
                    ("Evolutionary strategy (0-9)", 'strategy', html("There are 10 way to evolution."))
                ],
                Floats=[
                    ("Weight factor", 'F', html("Weight factor is usually between 0.5 and 1 (in rare cases > 1).")),
                    ("Recombination factor", 'CR', html("The chance of crossover possible."))
                ])
    
    def setArgs(self, PLnAP):
        self.maxGen.setValue(PLnAP['maxGen'])
        self.report.setValue(PLnAP['report'])
        for i, tag in enumerate(['IMax', 'IMin', 'LMax', 'LMin', 'FMax', 'FMin', 'AMax', 'AMin']):
            self.PLTable.cellWidget(i, 1).setValue(PLnAP[tag])
        if self.algorithm=="Genetic Algorithm":
            self.popSize.setValue(PLnAP['algorithmPrams']['nPop'])
            for i, tag in enumerate(['pCross', 'pMute', 'pWin', 'bDelta']):
                self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
        elif self.algorithm=="Firefly Algorithm":
            self.popSize.setValue(PLnAP['algorithmPrams']['n'])
            for i, tag in enumerate(['alpha', 'betaMin', 'gamma', 'beta0']):
                self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
        elif self.algorithm=="Differential Evolution":
            self.popSize.setValue(PLnAP['algorithmPrams']['NP'])
            for i, tag in enumerate(['strategy', 'F', 'CR']):
                self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
    
    @pyqtSlot(int)
    @pyqtSlot(float)
    def isOk(self, r=None):
        n = True
        pre = 0
        for i in range(self.PLTable.rowCount()):
            if i%2==0:
                pre = self.PLTable.cellWidget(i, 1).value()
            elif i%2==1:
                n &= pre>=self.PLTable.cellWidget(i, 1).value()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
    
    @pyqtSlot()
    def on_setDefault_clicked(self):
        self.setArgs({
            'maxGen':1500, 'report':1,
            'IMin':5., 'LMin':5., 'FMin':5., 'AMin':0., 'IMax':300., 'LMax':300., 'FMax':300., 'AMax':360.,
            'algorithmPrams':
                {'nPop':500, 'pCross':0.95, 'pMute':0.05, 'pWin':0.95, 'bDelta':5.} if self.algorithm=="Genetic Algorithm" else
                {'n':80, 'alpha':0.01, 'betaMin':0.2, 'gamma':1., 'beta0':1.} if self.algorithm=="Firefly Algorithm" else
                {'NP':400, 'strategy':1, 'F':0.6, 'CR':0.9}
        })
    
    @pyqtSlot(int)
    def on_maxGen_valueChanged(self, p0):
        self.report.setEnabled(not p0==0)
        self.report_label.setEnabled(not p0==0)
