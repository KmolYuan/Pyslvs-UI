# -*- coding: utf-8 -*-
from ...QtModules import *
from .Ui_Path_Solving_options import Ui_Dialog

class Path_Solving_options_show(QDialog, Ui_Dialog):
    def __init__(self, algorithm, settings, parent=None):
        super(Path_Solving_options_show, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.setTabText(1, algorithm)
        self.setArgs(**settings)
        self.isOk()
    
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
