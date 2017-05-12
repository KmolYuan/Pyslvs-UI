# -*- coding: utf-8 -*-
from ..QtModules import *
import os
from .slvsForm.assembly import slvsAssembly
from .slvsForm.link import slvsLink
from .slvsForm.chain import slvsChain
from .Ui_slvsType import Ui_Dialog

class slvsTypeSettings(QDialog, Ui_Dialog):
    def __init__(self, Environment_variables, name, Point, Line, Chain, parent=None):
        super(slvsTypeSettings, self).__init__(parent)
        self.setupUi(self)
        self.Environment_variables = QDir(Environment_variables)
        self.folderName.setPlaceholderText(name)
        self.folderName.setText(name)
        self.Point = Point
        self.Line = Line
        self.Chain = Chain
        self.folderPath.setText(Environment_variables)
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save)
        self.on_LinkRule_currentIndexChanged(0)
        self.on_ChainRule_currentIndexChanged(0)
        self.on_LinkType_currentIndexChanged(0)
        self.on_ChainType_currentIndexChanged(0)
    
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
        self.LinkPreview.setText(self.nameRule('Line', self.LinkRule.currentIndex(), self.LinkHeader.text()).format(0, 75.02))
    @pyqtSlot(int)
    def on_ChainRule_currentIndexChanged(self, index):
        self.ChainHeaderText.setEnabled(index==2 or index==3)
        self.ChainHeader.setEnabled(index==2 or index==3)
        self.ChainPreview.setText(self.nameRule('Chain', self.ChainRule.currentIndex(), self.ChainHeader.text()).format(0, '20_10.05_12.4'))
    
    @pyqtSlot(str)
    def on_LinkHeader_textEdited(self, p0): self.LinkPreview.setText(self.nameRule('Line', self.LinkRule.currentIndex(), p0).format(0, 75.02))
    @pyqtSlot(str)
    def on_ChainHeader_textEdited(self, p0): self.ChainPreview.setText(self.nameRule('Chain', self.ChainRule.currentIndex(), p0).format(0, '20_10.05_12.4'))
    @pyqtSlot(str)
    def on_AssemblyHeader_textEdited(self, p0): self.AssemblyPreview.setText(p0+'0' if p0!='' else 'Assembly')
    
    def nameRule(self, name, type, ctext):
        rule = [
            name if type in [0, 1] or(type in [2, 3] and ctext=='') else ctext if type in [2, 3] else '',
            '_{}' if type in [1, 3] else '']
        return '{}{{}}{}.slvs'.format(*rule)
    
    def save(self):
        if self.hasCreateFolder.checkState():
            folderPath = self.Environment_variables.absolutePath()+'/'+(self.folderName.text() if not self.folderName.text()=='' else self.folderName.placeholderText())
            if not os.path.exists(folderPath): os.makedirs(folderPath)
            self.folderPath = QDir(folderPath)
        else: self.folderPath = QDir(self.Environment_variables)
        scale = self.ScaleMolecular.value()/self.ScaleDenominator.value()
        setting = {
            'thickness': self.ThicknessVal.value()*scale,
            'drilling': self.DrillingVal.value()*scale,
            'joint': self.JointVal.value()*scale if self.hasJoint.checkState() else 0}
        for i in range(len(self.Line)):
            fileName = self.nameRule('Line', self.LinkRule.currentIndex(), self.LinkHeader.text()).format(i, self.Line[i].len)
            self.write(fileName,
                slvsLink(self.Line[i]['len'], width=self.LinkWidthVal.value()*scale, type=self.LinkType.currentIndex(), **setting))
        for i in range(len(self.Chain)):
            fileName = self.nameRule('Chain', self.ChainRule.currentIndex(), self.ChainHeader.text()).format(
                i, '_'.join(['{}']*3).format(self.Chain[i].p1p2, self.Chain[i].p2p3, self.Chain[i].p1p3))
            self.write(fileName,
                slvsChain(self.Chain[i].p1p2, self.Chain[i].p2p3, self.Chain[i].p1p3, width=self.ChainWidthVal.value()*scale, type=self.ChainType.currentIndex(), **setting))
        if self.hasAssembly.checkState(): self.write(self.AssemblyPreview.text()+'.slvs', slvsAssembly(self.Point, self.Line, self.Chain))
    def write(self, fileName, content):
        filePath = QFileInfo(self.folderPath, fileName).absoluteFilePath()
        with open(filePath, 'w', encoding='iso-8859-15', newline="") as f: f.write(content)
        print("Saved: {}".format(filePath))
    
    @pyqtSlot(int)
    def on_LinkType_currentIndexChanged(self, index):
        if index==0: self.LinkImage.setPixmap(QPixmap(":/icons/preview/Link_round.png"))
    @pyqtSlot(int)
    def on_ChainType_currentIndexChanged(self, index):
        if index==0: self.ChainImage.setPixmap(QPixmap(":/icons/preview/Chain_sheet.png"))
        if index==1: self.ChainImage.setPixmap(QPixmap(":/icons/preview/Chain_frame.png"))
