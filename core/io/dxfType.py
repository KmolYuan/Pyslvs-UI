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
