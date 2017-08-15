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
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("About {} (Edit mode)".format(name))
        self.fileName.setText("File Name: {}".format(name))
        self.authorName_input.setText(author)
        self.dateName.setText(lastTime)
        self.descriptionText.setPlainText(description)
        if results:
            for result in results:
                item = QListWidgetItem("{} ({} gen)".format(result['Algorithm'], result['generateData']['maxGen']))
                interrupt = result['interruptedGeneration']
                if interrupt=='False':
                    item.setIcon(QIcon(QPixmap(":/icons/task-completed.png")))
                elif interrupt=='N/A':
                    item.setIcon(QIcon(QPixmap(":/icons/question-mark.png")))
                else:
                    item.setIcon(QIcon(QPixmap(":/icons/interrupted.png")))
                keys = sorted(list(result.keys()))
                info = (["{}: {}".format(k, result[k]) for k in keys if 'x' in k or 'y' in k or 'L' in k])
                item.setToolTip('\n'.join(["[{}] ({}{} gen)".format(result['Algorithm'],
                    '' if interrupt=='False' else interrupt+'-', result['generateData']['maxGen'])]+
                    (["※ Completeness is not clear." if interrupt=='N/A' else ''])+info))
                self.Results.addItem(item)
        else:
            item = QListWidgetItem(QIcon(QPixmap(":/icons/task-completed.png")), "No results")
            item.setToolTip("There is no any algorithm results in this workbook.")
            self.Results.addItem(item)

class fileInfo_show(editFileInfo_show):
    def __init__(self, name, author, description, lastTime, results, errorInfo, parent=None):
        super(fileInfo_show, self).__init__(name, author, description, lastTime, results, parent)
        self.setWindowTitle("About {}".format(name))
        self.authorName_input.setReadOnly(True)
        self.descriptionText.setReadOnly(True)
        if errorInfo:
            self.ErrorTables.setText('\n'.join(["Some part are missing:"]+['+{}'.format(e) for e in errorInfo]))
            self.ErrorTables.setStyleSheet("color: rgb(255, 0, 0);")
