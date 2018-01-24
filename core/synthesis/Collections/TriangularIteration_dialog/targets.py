# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang
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

#Generator to get the text from list widget.
def list_texts(widget, returnRow=False):
    for row in range(widget.count()):
        if returnRow:
            yield row, widget.item(row).text()
        else:
            yield widget.item(row).text()

#Generator to get the text from combobox widget.
def combo_texts(widget):
    for row in range(widget.count()):
        yield widget.itemText(row)

class TargetsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(TargetsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        currentItem = parent.grounded_list.currentItem()
        if currentItem:
            for text in combo_texts(parent.joint_name):
                if not parent.PreviewWindow.name_in_same(text) and (text not in (
                    currentItem.text()
                    .replace('(', '')
                    .replace(')', '')
                    .split(", ")
                )):
                    self.other_list.addItem(text)
        target_list = [text for text in list_texts(parent.Target_list)]
        for row, text in list_texts(self.other_list, True):
            if text in target_list:
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
