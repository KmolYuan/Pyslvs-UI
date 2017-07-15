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
tr = QCoreApplication.translate
from .Ui_fileInfo import Ui_Info_Dialog

class editFileInfo_show(QDialog, Ui_Info_Dialog):
    def __init__(self, name, author, description, lastTime, results, parent=None):
        super(editFileInfo_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("About {}".format(name))
        self.fileName.setText("File Name: {}".format(name))
        self.authorName_input.setText(author)
        self.dateName.setText(lastTime)
        self.descriptionText.setPlainText(description)
        if results: self.Results.setText('\n'.join(["{} ({} gen)".format(result['Algorithm'], result['GenerateData']['maxGen']) for result in results]))

class fileInfo_show(editFileInfo_show):
    def __init__(self, name, author, description, lastTime, results, errorInfo, parent=None):
        super(fileInfo_show, self).__init__(name, author, description, lastTime, results, parent)
        self.setWindowTitle("About {} (Edit mode)".format(name))
        self.authorName_input.setReadOnly(True)
        self.descriptionText.setReadOnly(True)
        if errorInfo:
            self.ErrorTables.setText('\n'.join(["Some part are missing:"]+['+{}'.format(e) for e in errorInfo]))
            self.ErrorTables.setStyleSheet("color: rgb(255, 0, 0);")
