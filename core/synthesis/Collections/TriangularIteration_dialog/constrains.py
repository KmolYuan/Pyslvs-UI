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
from networkx import cycle_basis
from itertools import combinations
from .Ui_constrains import Ui_Dialog

get_list = lambda item: item.text().split(", ")

class ConstrainsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(ConstrainsDialog, self).__init__(parent)
        self.setupUi(self)
        for chain in cycle_basis(parent.PreviewWindow.G):
            if len(chain)==4:
                chain_node = []
                for link in combinations(chain, 2):
                    for n, edge in enumerate(parent.PreviewWindow.G.edges):
                        if sorted(link)==sorted(edge):
                            chain_node.append('P{}'.format(n))
                self.Loops_list.addItem(", ".join(sorted(chain_node)))
        constraint_list = [
            sorted(get_list(parent.constraint_list.item(row)))
            for row in range(parent.constraint_list.count())
        ]
        for row in range(self.Loops_list.count()):
            item_list = sorted(get_list(self.Loops_list.item(row)))
            if item_list in constraint_list:
                self.Loops_list.takeItem(row)
                self.main_list.addItem(parent.constraint_list.item(constraint_list.index(item_list)).text())
    
    @pyqtSlot(int)
    def on_Loops_list_currentRowChanged(self, row):
        if row>-1:
            self.sorting_list.clear()
            for point in get_list(self.Loops_list.item(row)):
                self.sorting_list.addItem(point)
    
    @pyqtSlot()
    def on_main_add_clicked(self):
        if self.sorting_list.count():
            self.main_list.addItem(", ".join(
                self.sorting_list.item(row).text()
                for row in range(self.sorting_list.count())
            ))
            self.sorting_list.clear()
            self.Loops_list.takeItem(self.Loops_list.currentRow())
    
    @pyqtSlot()
    def on_sorting_add_clicked(self):
        row = self.main_list.currentRow()
        if row>-1:
            self.Loops_list.addItem(self.main_list.takeItem(row))
