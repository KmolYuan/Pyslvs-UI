# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Mechanical Synthesis System. 
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

from core.QtModules import (
    QDialog,
    Qt,
    pyqtSlot,
)
from core.graphics import edges_view
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

#A generator to find out the four bar loops.
def four_bar_loops(G):
    result = set([])
    vertexes = {v: k for k, v in edges_view(G)}
    for node in G.nodes:
        if node in result:
            continue
        nb1s = G.neighbors(node)
        #node not in nb1s
        for nb1 in nb1s:
            if nb1 in result:
                continue
            nb2s = G.neighbors(nb1)
            #node can not in nb2s
            for nb2 in nb2s:
                if (nb2 == node) or (nb2 in result):
                    continue
                nb3s = G.neighbors(nb2)
                #node can not in nb3s
                for nb3 in nb3s:
                    if (nb3 in (node, nb1)) or (nb3 in result):
                        continue
                    if node in G.neighbors(nb3):
                        result.update([node, nb1, nb2, nb3])
                        yield tuple(
                            vertexes[tuple(sorted(e))]
                            for e in [(node, nb1), (nb1, nb2), (nb2, nb3), (node, nb3)]
                        )

class ConstraintsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(ConstraintsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        cl = tuple(
            set(get_list(item))
            for item in list_items(parent.constraint_list)
        )
        for chain in four_bar_loops(parent.PreviewWindow.G):
            chain = sorted(chain)
            for i, n in enumerate(chain):
                if n in parent.PreviewWindow.same:
                    n = parent.PreviewWindow.same[n]
                chain[i] = 'P{}'.format(n)
            if set(chain) not in cl:
                self.Loops_list.addItem(", ".join(chain))
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
