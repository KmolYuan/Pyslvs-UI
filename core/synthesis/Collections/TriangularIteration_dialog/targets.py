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

from core.QtModules import *
from .Ui_targets import Ui_Dialog

class TargetsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(TargetsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        currentItem = parent.grounded_list.currentItem()
        if currentItem:
            for row in range(parent.joint_name.count()):
                text = parent.joint_name.itemText(row)
                if text not in (
                    currentItem.text()
                    .replace('(', '')
                    .replace(')', '')
                    .split(", ")
                ):
                    self.other_list.addItem(text)
        target_list = [parent.Target_list.item(row).text() for row in range(parent.Target_list.count())]
        for row in range(self.other_list.count()):
            if self.other_list.item(row).text() in target_list:
                self.targets_list.addItem(self.other_list.takeItem(row))
    
    @pyqtSlot()
    def on_targets_add_clicked(self):
        row = self.other_list.currentRow()
        if row>-1:
            self.targets_list.addItem(self.other_list.takeItem(row))
    
    @pyqtSlot()
    def on_other_add_clicked(self):
        row = self.targets_list.currentRow()
        if row>-1:
            self.other_list.addItem(self.targets_list.takeItem(row))
