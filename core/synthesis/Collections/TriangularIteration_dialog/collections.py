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
from .Ui_collections import Ui_Dialog

mechanismParams_4Bar = {
    'Driver':{'A':None}, #'A':(x, y, r)
    'Follower':{'B':None}, #'B':(x, y, r)
    'Target':{'E':None}, #'E':((x1, y1), (x2, y2), (x3, y3), ...)
    'Link_Expression':"ground[A,B];[A,C];[C,D,E];[B,D]",
    'Expression':"PLAP[A,L0,a0,B](C);PLLP[C,L1,L2,B](D);PLLP[C,L3,L4,D](E)",
    'constraint':[('A', 'B', 'C', 'D')]
}
mechanismParams_8Bar = {
    'Driver':{'A':None},
    'Follower':{'B':None},
    'Target':{'H':None},
    'Link_Expression':"ground[A,B];[A,C];[C,D];[B,D,E];[C,F];[B,F];[E,G];[F,G,H]",
    'Expression':"PLAP[A,L0,a0,B](C);PLLP[B,L2,L1,C](D);PLLP[B,L4,L3,D](E);PLLP[C,L5,L6,B](F);PLLP[F,L8,L7,E](G);PLLP[F,L9,L10,G](H)",
    'constraint':[('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'F')]
}

class CollectionsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(CollectionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.collections = parent.collections
        for name in self.collections:
            self.collections_list.addItem(name)
        self.hasCollection()
        self.canOpen()
    
    def canOpen(self):
        self.buttonBox.button(QDialogButtonBox.Open).setEnabled(self.collections_list.currentRow()>-1)
    
    @pyqtSlot(int)
    def on_collections_list_currentRowChanged(self, row):
        self.canOpen()
    
    def hasCollection(self):
        hasCollection = bool(self.collections)
        self.delete_button.setEnabled(hasCollection)
        self.rename_button.setEnabled(hasCollection)
    
    @pyqtSlot()
    def on_delete_button_clicked(self):
        row = self.collections_list.currentRow()
        if row>-1:
            reply = QMessageBox.question(self, "Delete", "Do you want to delete this structure?",
                (QMessageBox.Yes | QMessageBox.No), QMessageBox.Yes)
            if reply==QMessageBox.Yes:
                item = self.collections_list.takeItem(row)
                del self.collections[item.text()]
                self.hasCollection()
    
    @pyqtSlot()
    def on_rename_button_clicked(self):
        row = self.collections_list.currentRow()
        if row>-1:
            name, ok = QInputDialog.getText(self, "Profile name", "Please enter the profile name:")
            if ok:
                if not name:
                    QMessageBox.warning(self, "Profile name", "Can not use blank to rename.")
                    return
                item = self.collections_list.item(row)
                self.collections[name] = self.collections.pop(item.text())
                item.setText(name)
    
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        self.mechanismParams = self.collections[self.collections_list.currentItem().text()]
    
    @pyqtSlot()
    def on_common_load_clicked(self):
        row = self.common_linkage.currentRow()
        if row==0:
            self.mechanismParams = mechanismParams_4Bar
        elif row==1:
            self.mechanismParams = mechanismParams_8Bar
