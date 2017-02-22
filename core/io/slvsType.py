# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .slvsForm import *
from .Ui_slvsType import Ui_Dialog

class slvsTypeSettings(QDialog, Ui_Dialog):
    def __init__(self, Environment_variables, Point, Line, Chain, parent=None):
        super(slvsTypeSettings, self).__init__(parent)
        self.setupUi(self)
        self.Environment_variables = QDir(Environment_variables)
        self.Point = Point
        self.Line = Line
        self.Chain = Chain
        self.folderPath.setText(Environment_variables)
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save)
    
    @pyqtSlot()
    def on_setPath_clicked(self):
        folderName = QFileDialog.getExistingDirectory(self, 'Save to folder...', self.Environment_variables.path(), QFileDialog.ShowDirsOnly)
        if folderName:
            self.Environment_variables = QDir(folderName)
            self.folderPath.setText(folderName)
    
    @pyqtSlot(int)
    def on_LinkRule_currentIndexChanged(self, index):
        self.LinkHeaderText.setEnabled(index==2 or index==3)
        self.LinkHeader.setEnabled(index==2 or index==3)
        if index==0: name = "Line0"
        elif index==1: name = "Line0_75.02"
        elif index==2: name = self.LinkHeader.text()+"0"
        elif index==3: name = self.LinkHeader.text()+"0_75.02"
        elif index==4: name = "0"
        self.LinkPreview.setText(name)
    @pyqtSlot(int)
    def on_ChainRule_currentIndexChanged(self, index):
        self.ChainHeaderText.setEnabled(index==2 or index==3)
        self.ChainHeader.setEnabled(index==2 or index==3)
        if index==0: name = "Chain0"
        elif index==1: name = "Chain0_20_10.05_12.4"
        elif index==2: name = self.ChainHeader.text()+"0"
        elif index==3: name = self.ChainHeader.text()+"0_20_10.05_12.4"
        elif index==4: name = "0"
        self.ChainPreview.setText(name if self.LinkPreview.text()!=name else name+"_c")
    
    @pyqtSlot(str)
    def on_LinkHeader_textEdited(self, p0):
        if self.LinkRule.currentIndex()==2: self.LinkPreview.setText(p0+"0" if p0!="" else "Line0")
        elif self.LinkRule.currentIndex()==3: self.LinkPreview.setText(p0+"0_75.02" if p0!="" else "Line0_75.02")
    @pyqtSlot(str)
    def on_ChainHeader_textEdited(self, p0):
        if self.ChainRule.currentIndex()==2: name = p0+"0" if self.ChainHeader.text()!="" else "Chain0"
        elif self.ChainRule.currentIndex()==3: name = p0+"0_20_10.05_12.4" if p0!="" else "Chain0_20_10.05_12.4"
        self.ChainPreview.setText(name if self.LinkPreview.text()!=name else name+"_c")
    @pyqtSlot(str)
    def on_AssemblyHeader_textEdited(self, p0):
        name = p0+"0" if p0!="" else "Assembly"
        self.AssemblyPreview.setText(name if self.LinkPreview.text()!=name and self.ChainPreview.text()!=name else name+"_a")
    
    def save(self):
        scale = self.ScaleMolecular.value()/self.ScaleDenominator.value()
        setting = {
            'width': self.LinkWidthVal.value()*scale,
            'thickness': self.ThicknessVal.value()*scale,
            'drilling': self.DrillingVal.value()*scale,
            'joint': self.JointVal.value()*scale if self.hasJoint.checkState() else 0,
        }
        for i in range(len(self.Line)):
            linkFileName = self.LinkPreview.text()[:-1]+str(i)+'.slvs'
            filePath = QFileInfo(self.Environment_variables, linkFileName).absoluteFilePath()
            with open(fileName, 'w', encoding="iso-8859-15", newline="") as f: f.write(slvsLink(self.Line[i]['len'], type=self.LinkType.currentIndex(), **setting))
            print("Saved: {}".format(filePath))
        for i in range(len(self.Chain)):
            chainFileName = self.ChainPreview.text()[:-1]+str(i)+'.slvs'
            filePath = QFileInfo(self.Environment_variables, linkFileName).absoluteFilePath()
            with open(fileName, 'w', encoding="iso-8859-15", newline="") as f: f.write(slvsChain(self.Chain[i]['p1'], self.Chain[i]['p2'], self.Chain[i]['p3'], type=self.ChainType.currentIndex(), **setting))
            print("Saved: {}".format(filePath))
        if self.hasAssembly.checkState():
            assemblyFileName = self.AssemblyPreview.text()+'.slvs'
            filePath = QFileInfo(self.Environment_variables, assemblyFileName).absoluteFilePath()
            with open(fileName, 'w', encoding="iso-8859-15", newline="") as f: f.write(slvsAssembly(self.Point, self.Line, self.Chain))
            print("Saved: {}".format(filePath))
