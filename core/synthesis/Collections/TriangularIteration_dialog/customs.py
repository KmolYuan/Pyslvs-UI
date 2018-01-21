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
        self.pos = parent.PreviewWindow.pos
        self.status = parent.PreviewWindow.status
        self.joint_combobox = parent.joint_name
        for row in range(parent.grounded_list.count()):
            self.link_choose.addItem(parent.grounded_list.item(row).text())
        for name, link in parent.PreviewWindow.cus.items():
            self.custom_list.addItem("{} -> {}".format(name, link))
    
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
