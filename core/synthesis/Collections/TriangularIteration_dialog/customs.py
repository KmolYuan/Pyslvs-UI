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
from .Ui_customs import Ui_Dialog

class CustomsDialog(QDialog, Ui_Dialog):
    '''
    name: str = 'P1', 'P2', ...
    num: int = 1, 2, ...
    '''
    
    def __init__(self, parent=None):
        super(CustomsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.cus = parent.PreviewWindow.cus
        self.same = parent.PreviewWindow.same
        self.pos = parent.PreviewWindow.pos
        self.status = parent.PreviewWindow.status
        self.joint_combobox = parent.joint_name
        for row in range(parent.grounded_list.count()):
            self.link_choose.addItem(parent.grounded_list.item(row).text())
        for name, link in self.cus.items():
            self.custom_list.addItem("{} -> {}".format(name, link))
        for i in self.pos:
            self.quote_choose.addItem('P{}'.format(i))
        for s, qs in self.same.items():
            self.multiple_list.addItem("{} -> {}".format('P{}'.format(s), 'P{}'.format(qs)))
    
    @pyqtSlot()
    def on_add_button_clicked(self):
        row = self.link_choose.currentIndex()
        if row>-1:
            try:
                new_num = max(self.cus)
            except ValueError:
                new_num = max(self.pos)
            new_num += 1
            new_name = 'P{}'.format(new_num)
            self.cus[new_name] = row
            self.pos[new_num] = (0., 0.)
            self.status[new_num] = False
            self.custom_list.addItem("{} -> {}".format(new_name, self.link_choose.itemText(row)))
            self.joint_combobox.addItem(new_name)
    
    @pyqtSlot()
    def on_delete_button_clicked(self):
        row = self.custom_list.currentRow()
        if row>-1:
            name = self.custom_list.item(row).text().split(" -> ")[0]
            num = int(name.replace('P', ''))
            self.cus.pop(name)
            self.pos.pop(num)
            self.status.pop(num)
            self.custom_list.takeItem(row)
            self.joint_combobox.removeItem(num)
    
    @pyqtSlot(str)
    def on_quote_choose_currentIndexChanged(self, s):
        self.quote_link_choose.clear()
        if s:
            for row in range(self.link_choose.count()):
                link_text = self.link_choose.itemText(row)
                if s in link_text.replace('(', '').replace(')', '').split(", "):
                    self.quote_link_choose.addItem(link_text)
    
    @pyqtSlot(str)
    def on_quote_link_choose_currentIndexChanged(self, s):
        self.joint_choose.clear()
        if s:
            for joint in s.replace('(', '').replace(')', '').split(", "):
                if joint!=self.quote_choose.currentText():
                    self.joint_choose.addItem(joint)
    
    @pyqtSlot()
    def on_add_mj_button_clicked(self):
        s = self.joint_choose.currentText()
        if s:
            joint = int(s.replace('P', ''))
            qs = self.quote_choose.currentText()
            quote = int(qs.replace('P', ''))
            self.same[joint] = quote
            self.multiple_list.addItem("{} -> {}".format(s, qs))
    
    @pyqtSlot()
    def on_delete_mj_button_clicked(self):
        row = self.multiple_list.currentRow()
        if row>-1:
            joint = int(self.multiple_list.item(row).text().split(" -> ")[0].replace('P', ''))
            self.same.pop(joint)
            self.multiple_list.takeItem(row)
