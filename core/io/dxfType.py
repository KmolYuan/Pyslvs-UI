# -*- coding: utf-8 -*-
from ..QtModules import *
from .dxfForm.model import dxfModel
from .Ui_dxfType import Ui_Dialog

class dxfTypeSettings(QDialog, Ui_Dialog):
    def __init__(self, Environment_variables, name, Line, Chain, parent=None):
        super(dxfTypeSettings, self).__init__(parent)
        self.setupUi(self)
        self.Line = Line
        self.Chain = Chain
        self.filePath = Environment_variables+'/'+name+'.dxf'
        self.folderPath.setText(self.filePath)
        self.buttonBox.button(QDialogButtonBox.Save).clicked.connect(self.save)
        self.LinkImage.setPixmap(QPixmap(":/icons/preview/Link_round.png"))
        self.ChainImage.setPixmap(QPixmap(":/icons/preview/Chain_sheet.png"))
    
    @pyqtSlot()
    def on_setPath_clicked(self):
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save file...', self.filePath, 'AutoCAD DXF (*.dxf)')
        if fileName:
            self.filePath = fileName
            self.folderPath.setText(self.filePath)
    
    def save(self): 
        dxfModel(self.filePath, self.Line, self.Chain,
            LinkWidth=self.LinkWidthVal.value(),
            ChainWidth=self.ChainWidthVal.value(),
            interval=self.IntervalVal.value(),
            drilling=self.DrillingVal.value())
