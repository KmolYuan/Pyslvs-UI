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
from networkx import cycle_basis
from itertools import combinations
from .Ui_constraints import Ui_Dialog

def get_list(item):
    if not item:
        return []
    for e in item.text().split(", "):
        yield e

def list_items(widget, returnRow=False):
    for row in range(widget.count()):
        if returnRow:
            yield row, widget.item(row)
        else:
            yield widget.item(row)

class ConstraintsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(ConstraintsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        cl = tuple(
            set(get_list(item)) for item in list_items(parent.constraint_list)
        )
        for chain in cycle_basis(parent.PreviewWindow.G):
            if len(chain)==4:
                chain_node = []
                for link in combinations(chain, 2):
                    for n, edge in enumerate(parent.PreviewWindow.G.edges):
                        if sorted(link)==sorted(edge):
                            if n in parent.PreviewWindow.same:
                                n = parent.PreviewWindow.same[n]
                            chain_node.append('P{}'.format(n))
                if set(chain_node) in cl:
                    continue
                self.Loops_list.addItem(", ".join(sorted(chain_node)))
        for item in list_items(parent.constraint_list):
            self.main_list.addItem(item.text())
    
    @pyqtSlot(int)
    def on_Loops_list_currentRowChanged(self, row):
        if row>-1:
            self.sorting_list.clear()
            for point in get_list(self.Loops_list.item(row)):
                self.sorting_list.addItem(point)
    
    @pyqtSlot()
    def on_main_add_clicked(self):
        if self.sorting_list.count():
            self.main_list.addItem(", ".join(item.text() for item in list_items(self.sorting_list)))
            self.sorting_list.clear()
            self.Loops_list.takeItem(self.Loops_list.currentRow())
    
    @pyqtSlot()
    def on_sorting_add_clicked(self):
        row = self.main_list.currentRow()
        if row>-1:
            self.Loops_list.addItem(self.main_list.takeItem(row))
