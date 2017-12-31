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

from ...QtModules import *
from networkx import (
    Graph,
    is_isomorphic
)
from .topologic import testT, TestError
from .graph import (
    graph,
    engine_picker,
    EngineList,
    EngineError
)
from .Ui_Collections import Ui_Form

class Collections_show(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Collections_show, self).__init__(parent)
        self.setupUi(self)
        self.addPoint_by_graph = parent.addPoint_by_graph
        self.collections = []
        self.collections_layouts = []
        self.collections_grounded = []
        self.graph_engine.addItems(EngineList)
        self.graph_engine.setCurrentIndex(2)
        self.graph_link_as_node.clicked.connect(self.on_reload_atlas_clicked)
        self.graph_engine.currentIndexChanged.connect(self.on_reload_atlas_clicked)
        self.unsaveFunc = parent.workbookNoSave
    
    def clear(self):
        self.grounded_merge.setEnabled(False)
        self.collections.clear()
        self.collection_list.clear()
        self.Preview_window.clear()
        self.Expression_edges.clear()
        self.NL.setText('0')
        self.NJ.setText('0')
        self.DOF.setText('0')
        self.grounded_list.clear()
    
    def engineErrorMsg(self, e):
        QMessageBox.warning(self, str(e), "Please install and make sure Graphviz is working", QMessageBox.Ok, QMessageBox.Ok)
    
    #Reload atlas with the engine.
    @pyqtSlot()
    @pyqtSlot(str)
    def on_reload_atlas_clicked(self, p0=None):
        if self.collections:
            self.collections_layouts.clear()
            self.collection_list.clear()
            self.Preview_window.clear()
            self.Expression_edges.clear()
            self.NL.setText('0')
            self.NJ.setText('0')
            self.DOF.setText('0')
            self.grounded_list.clear()
            progdlg = QProgressDialog("Drawing atlas...", "Cancel", 0, len(self.collections), self)
            progdlg.setWindowTitle("Type synthesis")
            progdlg.resize(400, progdlg.height())
            progdlg.setModal(True)
            progdlg.show()
            engineSTR = self.graph_engine.currentText().split(" - ")[1]
            for i, G in enumerate(self.collections):
                QCoreApplication.processEvents()
                if progdlg.wasCanceled():
                    return
                item = QListWidgetItem("No. {}".format(i+1))
                try:
                    engine = engine_picker(G, engineSTR, self.graph_link_as_node.isChecked())
                    item.setIcon(graph(G, self.collection_list.iconSize().width(), engine, self.graph_link_as_node.isChecked()))
                except EngineError as e:
                    progdlg.setValue(progdlg.maximum())
                    self.engineErrorMsg(e)
                    break
                else:
                    self.collections_layouts.append(engine)
                    item.setToolTip(str(G.edges))
                    self.collection_list.addItem(item)
                    progdlg.setValue(i+1)
    
    #Add collection by in put edges.
    def addCollection(self, edges):
        G = Graph(edges)
        try:
            testT(G, False)
            for n in G.nodes:
                if len(list(G.neighbors(n)))<2:
                    raise TestError("is not close chain")
            for H in self.collections:
                if is_isomorphic(G, H):
                    raise TestError("is isomorphic")
        except TestError as e:
            QMessageBox.warning(self, "Add Collection Error", "Error: {}".format(e), QMessageBox.Ok, QMessageBox.Ok)
            return
        self.collections.append(G)
        self.unsaveFunc()
        self.on_reload_atlas_clicked()
    
    #Add collections.
    def addCollections(self, collections):
        for c in collections:
            self.addCollection(c)
    
    #Add collection by input string.
    @pyqtSlot()
    def on_add_by_edges_button_clicked(self):
        edgesSTR = ""
        while not edgesSTR:
            edgesSTR, ok = QInputDialog.getText(
                self,
                "Add by edges",
                "Please enter a connection expression:\nExample: [(0, 1), (1, 2), (2, 3), (3, 0)]"
            )
            if not ok:
                return
        try:
            edges = eval(edgesSTR)
            if any(len(edge)!=2 for edge in edges):
                raise SyntaxError("Wrong format")
        except Exception as e:
            QMessageBox.warning(self, str(e), "Error: {}".format(e), QMessageBox.Ok, QMessageBox.Ok)
            return
        else:
            self.addCollection(edges)
    
    #Show the data of collection.
    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_collection_list_currentItemChanged(self, item, p0):
        has_item = bool(item)
        self.delete_button.setEnabled(has_item)
        self.grounded_button.setEnabled(has_item)
        if item:
            self.Preview_window.clear()
            item_ = QListWidgetItem(item.text())
            row = self.collection_list.row(item)
            G = self.collections[row]
            self.ground_engine = self.collections_layouts[row]
            item_.setIcon(graph(G, self.Preview_window.iconSize().width(), self.ground_engine, self.graph_link_as_node.isChecked()))
            self.Preview_window.addItem(item_)
            self.Expression_edges.setText(str(list(G.edges)))
            self.NL.setText(str(len(G.nodes)))
            self.NJ.setText(str(len(G.edges)))
            self.DOF.setText(str(3*(int(self.NL.text())-1) - 2*int(self.NJ.text())))
    
    @pyqtSlot()
    def on_Expression_copy_clicked(self):
        string = self.Expression_edges.text()
        if string:
            clipboard = QApplication.clipboard()
            clipboard.setText(string)
            self.Expression_edges.selectAll()
    
    #Delete the selected collection.
    @pyqtSlot()
    def on_delete_button_clicked(self):
        row = self.collection_list.currentRow()
        if row>-1:
            reply = QMessageBox.question(self, "Message", "Sure to remove #{} from your collections?".format(row),
                (QMessageBox.Apply | QMessageBox.Cancel), QMessageBox.Apply)
            if reply:
                self.grounded_list.clear()
                self.Preview_window.clear()
                self.Expression_edges.clear()
                self.NL.setText('0')
                self.NJ.setText('0')
                self.DOF.setText('0')
                self.collection_list.takeItem(row)
                del self.collections[row]
    
    #Grounded combinations
    @pyqtSlot()
    def on_grounded_button_clicked(self):
        item = self.collection_list.currentItem()
        self.grounded_merge.setEnabled(bool(item))
        if item:
            self.collections_grounded.clear()
            self.grounded_list.clear()
            G = self.collections[self.collection_list.row(item)]
            item = QListWidgetItem("Released")
            try:
                icon, pos = graph(G, self.grounded_list.iconSize().width(), self.ground_engine, self.graph_link_as_node.isChecked(), get_pos=True)
            except EngineError as e:
                self.engineErrorMsg(e)
                return
            item.setIcon(icon)
            self.collections_grounded.append(G)
            self.grounded_list.addItem(item)
            for node in G.nodes:
                G_ = Graph(G)
                G_.remove_node(node)
                error = False
                for H in self.collections_grounded:
                    if is_isomorphic(G_, H):
                        error = True
                if error:
                    continue
                item = QListWidgetItem("link_{} constrainted".format(node))
                icon, pos = graph(
                    G, self.grounded_list.iconSize().width(),
                    self.ground_engine,
                    self.graph_link_as_node.isChecked(),
                    None if self.graph_link_as_node.isChecked() else node,
                    get_pos=True
                )
                item.setIcon(icon)
                self.collections_grounded.append(G_)
                self.grounded_list.addItem(item)
    
    @pyqtSlot()
    def on_grounded_merge_clicked(self):
        item = self.grounded_list.currentItem()
        if item:
            G = self.collections_grounded[0]
            text = item.text()
            ground_link = None if text=="Released" else int(text.replace(" constrainted", "").split("_")[1])
            reply = QMessageBox.question(self, "Message", "Merge \"{}\" chain to your canvas?".format(text),
                (QMessageBox.Apply | QMessageBox.Cancel), QMessageBox.Apply)
            if reply==QMessageBox.Apply:
                self.addPoint_by_graph(G, self.ground_engine, ground_link)
