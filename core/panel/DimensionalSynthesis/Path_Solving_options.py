# -*- coding: utf-8 -*-
from ...QtModules import *
from .Ui_Path_Solving_options import Ui_Dialog

class Path_Solving_options_show(QDialog, Ui_Dialog):
    def __init__(self, algorithm, settings, parent=None):
        super(Path_Solving_options_show, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.setTabText(1, algorithm)
        self.setArgs(**settings)
        self.init_APTable(algorithm)
        self.isOk()
    
    def init_APTable(self, algorithm):
        if algorithm=="Differential Evolution":
            for i, (name, value) in enumerate([("Evolutionary strategy", 1), ("Population Size", 190)]):
                self.APTable.insertRow(i)
                self.APTable.setItem(i, 0, QTableWidgetItem(name))
                spinbox = QSpinBox()
                spinbox.setValue(value)
                self.APTable.setCellWidget(i, 1, spinbox)
            for i, (name, value) in enumerate([("Weight factor", 0.6), ("Recombination factor", 0.9)]):
                self.APTable.insertRow(i+2)
                self.APTable.setItem(i+2, 0, QTableWidgetItem(name))
                spinbox = QDoubleSpinBox()
                spinbox.setValue(value)
                self.APTable.setCellWidget(i+2, 1, spinbox)
        elif algorithm=="Firefly Algorithm":
            self.APTable.insertRow(0)
            self.APTable.setItem(0, 0, QTableWidgetItem("Population Size"))
            spinbox = QSpinBox()
            spinbox.setValue(190)
            self.APTable.setCellWidget(0, 1, spinbox)
            for i, (name, value) in enumerate([("Alpha value", 0.01), ("Minimum Beta value", 0.2), ("Gamma value", 1.), ("Beta0 value", 1.)]):
                self.APTable.insertRow(i+1)
                self.APTable.setItem(i+1, 0, QTableWidgetItem(name))
                spinbox = QDoubleSpinBox()
                spinbox.setValue(value)
                self.APTable.setCellWidget(i+1, 1, spinbox)
        elif algorithm=="Genetic Algorithm":
            self.APTable.insertRow(0)
            self.APTable.setItem(0, 0, QTableWidgetItem("Population Size"))
            spinbox = QSpinBox()
            spinbox.setValue(250)
            self.APTable.setCellWidget(0, 1, spinbox)
            for i, (name, value) in enumerate([("Crossover Rate", 0.95), ("Mutation Rate", 0.05), ("Winning Rate", 0.95), ("Delta value", 5.)]):
                self.APTable.insertRow(i+1)
                self.APTable.setItem(i+1, 0, QTableWidgetItem(name))
                spinbox = QDoubleSpinBox()
                spinbox.setValue(value)
                self.APTable.setCellWidget(i+1, 1, spinbox)
    
    def setArgs(self, maxGen=1500, report=1, AxMin=-50., AyMin=-50., DxMin=-50., DyMin=-50., IMin=5., LMin=5., FMin=5., AMin=0.,
            AxMax=50., AyMax=50., DxMax=50., DyMax=50., IMax=50., LMax=50., FMax=50., AMax=360.):
        self.maxGen.setValue(maxGen)
        self.report.setValue(report)
        self.AxMin.setValue(AxMin)
        self.AyMin.setValue(AyMin)
        self.DxMin.setValue(DxMin)
        self.DyMin.setValue(DyMin)
        self.IMin.setValue(IMin)
        self.LMin.setValue(LMin)
        self.FMin.setValue(FMin)
        self.AMin.setValue(AMin)
        self.AxMax.setValue(AxMax)
        self.AyMax.setValue(AyMax)
        self.DxMax.setValue(DxMax)
        self.DyMax.setValue(DyMax)
        self.IMax.setValue(IMax)
        self.LMax.setValue(LMax)
        self.FMax.setValue(FMax)
        self.AMax.setValue(AMax)
    
    def isOk(self):
        n = True
        for a, b in zip(
            [self.AxMin, self.AyMin, self.DxMin, self.DyMin, self.IMin, self.LMin, self.FMin, self.AMin],
            [self.AxMax, self.AyMax, self.DxMax, self.DyMax, self.IMax, self.LMax, self.FMax, self.AMax]
            ): n &= a.value()<=b.value()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
    
    @pyqtSlot(float)
    def on_maxGen_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_report_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_AxMin_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_AyMin_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_DxMin_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_DyMin_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_IMin_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_LMin_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_FMin_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_AMin_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_AxMax_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_AyMax_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_DxMax_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_DyMax_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_IMax_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_LMax_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_FMax_valueChanged(self, p0): self.isGenerate()
    @pyqtSlot(float)
    def on_AMax_valueChanged(self, p0): self.isGenerate()
    
    @pyqtSlot()
    def on_setDefault_clicked(self): self.setArgs()
