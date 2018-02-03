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

from core.QtModules import *
from core.graphics import PreviewCanvas, edges_view, replace_by_dict
from core.io import get_from_parenthesis
from networkx import Graph
from .Ui_collections import Ui_Dialog

mechanismParams_4Bar = {
    'Driver':{'A':None}, #'A':(x, y, r)
    'Follower':{'B':None}, #'B':(x, y, r)
    'Target':{'E':None}, #'E':((x1, y1), (x2, y2), (x3, y3), ...)
    'Link_Expression':"ground[A,B];[A,C];[C,D,E];[B,D]",
    'Expression':"PLAP[A,L0,a0,B](C);PLLP[C,L1,L2,B](D);PLLP[C,L3,L4,D](E)",
    'constraint':[('A', 'B', 'C', 'D')],
    'Graph':((0, 1), (1, 2), (2, 3), (3, 0)),
    'name_dict':{
        'A': 'P0',
        'B': 'P1',
        'C': 'P2',
        'D': 'P3',
        'E': 'P4'
    },
    'pos':{
        0: (-70, -70),
        1: (70, -70),
        2: (-70, 12.5),
        3: (70, 12.5),
        4: (0, 63.5)
    },
    'cus':{'P4':2},
    'same':{}
}

mechanismParams_8Bar = {
    'Driver':{'A':None},
    'Follower':{'B':None},
    'Target':{'H':None},
    'Link_Expression':"ground[A,B];[A,C];[C,D];[C,F];[B,D,E];[B,F];[E,G];[F,G,H]",
    'Expression':"PLAP[A,L0,a0,B](C);PLLP[B,L2,L1,C](D);PLLP[B,L4,L3,D](E);PLLP[C,L5,L6,B](F);PLLP[F,L8,L7,E](G);PLLP[F,L9,L10,G](H)",
    'constraint':[('A', 'B', 'C', 'D'), ('A', 'B', 'C', 'F')],
    'Graph':((0, 1), (0, 4), (0, 5), (1, 2), (1, 3), (2, 4), (3, 5), (3, 7), (4, 6), (6, 7)),
    'name_dict':{
        'C':'P3',
        'F':'P7',
        'J':'P4',
        'K':'P6',
        'B':'P1',
        'D':'P5',
        'H':'P10',
        'G':'P9',
        'E':'P8',
        'A':'P0',
        'I':'P2'
    },
    'pos':{
        0:(30.5, 10.5),
        1:(-14.5, 10.5),
        2:(-18.5, 0.),
        3:(81.5, 60.5),
        4:(92.5, 75.5),
        5:(-31.5, 86.5),
        6:(41.5, -38.5),
        7:(19.5, -32.5),
        8:(-85.5, 9.5),
        9:(-37.5, -48.5),
        10:(32.5, -107.5)
    },
    'cus':{'P10': 7},
    'same':{2:1, 4:3, 6:7}
}

class CollectionsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super(CollectionsDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.collections = parent.collections
        self.name_loaded = ""
        #Canvas
        def get_solutions_func():
            try:
                return replace_by_dict(self.collections[self.name_loaded])
            except KeyError:
                if self.name_loaded=="Four bar linkage mechanism":
                    return replace_by_dict(mechanismParams_4Bar)
                elif self.name_loaded=="Eight bar linkage mechanism":
                    return replace_by_dict(mechanismParams_8Bar)
                else:
                    return tuple()
        self.PreviewCanvas = PreviewCanvas(get_solutions_func, self)
        self.preview_layout.addWidget(self.PreviewCanvas)
        self.show_solutions.clicked.connect(self.PreviewCanvas.setShowSolutions)
        for name in self.collections:
            self.collections_list.addItem(name)
        #Splitter
        self.main_splitter.setSizes([200, 200])
        #Signals
        self.common_list.currentTextChanged.connect(self.choose_common)
        self.common_list.itemClicked.connect(self.choose_common)
        self.common_load.clicked.connect(self.load_common)
        self.common_list.itemDoubleClicked.connect(self.load_common)
        self.collections_list.currentTextChanged.connect(self.choose_collections)
        self.collections_list.itemClicked.connect(self.choose_collections)
        self.buttonBox.accepted.connect(self.load_collections)
        self.collections_list.itemDoubleClicked.connect(self.load_collections)
        self.collections_list.currentRowChanged.connect(self.canOpen)
        self.hasCollection()
        self.canOpen()
    
    def canOpen(self):
        self.buttonBox.button(QDialogButtonBox.Open).setEnabled(self.collections_list.currentRow()>-1)
    
    def hasCollection(self):
        hasCollection = bool(self.collections)
        for button in [self.rename_button, self.copy_button, self.delete_button]:
            button.setEnabled(hasCollection)
    
    @pyqtSlot()
    def on_rename_button_clicked(self):
        row = self.collections_list.currentRow()
        if row>-1:
            name, ok = QInputDialog.getText(self, "Profile name", "Please enter the profile name:")
            if ok:
                if not name:
                    QMessageBox.warning(self, "Profile name", "Can not use blank string to rename.")
                    return
                item = self.collections_list.item(row)
                self.collections[name] = self.collections.pop(item.text())
                item.setText(name)
    
    @pyqtSlot()
    def on_copy_button_clicked(self):
        row = self.collections_list.currentRow()
        if row>-1:
            name, ok = QInputDialog.getText(self, "Profile name", "Please enter a new profile name:")
            if ok:
                if not name:
                    QMessageBox.warning(self, "Profile name", "Can not use blank string to rename.")
                    return
                name_old = self.collections_list.item(row).text()
                self.collections[name] = self.collections[name_old].copy()
                self.collections_list.addItem(name)
    
    @pyqtSlot()
    def on_delete_button_clicked(self):
        row = self.collections_list.currentRow()
        if row>-1:
            reply = QMessageBox.question(self, "Delete", "Do you want to delete this structure?",
                (QMessageBox.Yes | QMessageBox.No), QMessageBox.Yes)
            if reply==QMessageBox.Yes:
                item = self.collections_list.takeItem(row)
                del self.collections[item.text()]
                self.PreviewCanvas.clear()
                self.hasCollection()
    
    @pyqtSlot(str)
    @pyqtSlot(QListWidgetItem)
    def choose_common(self, p0=None):
        text = self.common_list.currentItem().text()
        if text:
            self.name_loaded = text
            if text=="Four bar linkage mechanism":
                self.mechanismParams = mechanismParams_4Bar
            elif text=="Eight bar linkage mechanism":
                self.mechanismParams = mechanismParams_8Bar
            self.reload_canvas()
    
    @pyqtSlot(str)
    @pyqtSlot(QListWidgetItem)
    def choose_collections(self, p0=None):
        text = self.collections_list.currentItem().text()
        if text:
            self.name_loaded = text
            self.mechanismParams = self.collections[self.name_loaded]
            self.reload_canvas()
    
    #Simple loading. As same as dimensional synthesis tab widget.
    def reload_canvas(self):
        params = self.mechanismParams
        mapping = params['name_dict']
        #Name dict.
        if self.switch_name.isChecked():
            self.PreviewCanvas.setNameDict(mapping)
        #Add customize joints.
        G = Graph(params['Graph'])
        self.PreviewCanvas.setGraph(G, params['pos'])
        self.PreviewCanvas.cus = params['cus']
        self.PreviewCanvas.same = params['same']
        #Grounded setting.
        Driver = [mapping[e] for e in params['Driver']]
        Follower = [mapping[e] for e in params['Follower']]
        for row, link in enumerate(G.nodes):
            points = set(
                'P{}'.format(n)
                for n, edge in edges_view(G) if link in edge
            )
            if set(Driver + Follower) <= points:
                self.PreviewCanvas.setGrounded(row)
                break
        #Expression
        for expr in params['Expression'].split(';'):
            target = get_from_parenthesis(expr, '(', ')')
            self.PreviewCanvas.setStatus(params['name_dict'][target], True)
    
    @pyqtSlot()
    @pyqtSlot(QListWidgetItem)
    def load_common(self, p0=None):
        self.choose_common(self.common_list.currentItem().text())
        self.accept()
    
    @pyqtSlot()
    @pyqtSlot(QListWidgetItem)
    def load_collections(self, p0=None):
        self.choose_collections(self.collections_list.currentItem().text())
        self.accept()
    
    @pyqtSlot(bool)
    def on_switch_name_clicked(self, checked):
        if checked:
            self.PreviewCanvas.setNameDict({})
        else:
            self.PreviewCanvas.setNameDict(self.mechanismParams['name_dict'])
