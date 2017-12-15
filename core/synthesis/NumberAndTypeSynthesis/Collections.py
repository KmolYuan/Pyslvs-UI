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
from networkx import Graph
from .topologic import testT, TestError
from .graph import (
    graph,
    EngineList,
    EngineError
)
from .Ui_Collections import Ui_Form

class Collections_show(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Collections_show, self).__init__(parent)
        self.setupUi(self)
        self.Collections = []
        self.graph_engine.addItems(EngineList)
        self.graph_engine.setCurrentIndex(1)
        self.graph_link_as_node.clicked.connect(self.on_reload_atlas_clicked)
        self.graph_engine.currentIndexChanged.connect(self.on_reload_atlas_clicked)
        self.unsaveFunc = parent.workbookNoSave
    
    def clear(self):
        self.Collections.clear()
        self.Collection_list.clear()
        self.Preview_window.clear()
        self.Expression_edges.clear()
        self.NL.setText('0')
        self.NJ.setText('0')
        self.DOF.setText('0')
        self.grounded_list.clear()
    
    #Reload atlas with the engine.
    @pyqtSlot()
    @pyqtSlot(str)
    def on_reload_atlas_clicked(self, p0=None):
        if self.Collections:
            self.Collection_list.clear()
            progdlg = QProgressDialog("Drawing atlas...", "Cancel", 0, len(self.Collections), self)
            progdlg.setWindowTitle("Type synthesis")
            progdlg.resize(400, progdlg.height())
            progdlg.setModal(True)
            progdlg.show()
            engine = self.graph_engine.currentText().split(" - ")[1]
            for i, G in enumerate(self.Collections):
                QCoreApplication.processEvents()
                if progdlg.wasCanceled():
                    return
                item = QListWidgetItem("No. {}".format(i+1))
                try:
                    item.setIcon(graph(G, self.Collection_list.iconSize().width(), engine, self.graph_link_as_node.isChecked()))
                except EngineError as e:
                    progdlg.setValue(progdlg.maximum())
                    dlg = QMessageBox(QMessageBox.Warning, str(e), "Please install and make sure Graphviz is working", (QMessageBox.Ok), self)
                    dlg.show()
                    dlg.exec_()
                    break
                else:
                    item.setToolTip(str(G.edges))
                    self.Collection_list.addItem(item)
                    progdlg.setValue(i+1)
    
    #Add collection by in put edges.
    def addCollection(self, edges):
        G = Graph(edges)
        try:
            testT(G, False)
            for n in G.nodes:
                if len(list(G.neighbors(n)))<2:
                    raise TestError("is not close chain")
        except TestError as e:
            dlg = QMessageBox(QMessageBox.Warning, str(e), "Error: {}".format(e), (QMessageBox.Ok), self)
            dlg.show()
            dlg.exec_()
            return
        self.Collections.append(G)
        self.unsaveFunc()
        self.on_reload_atlas_clicked()
    
    #Add collections.
    def addCollections(self, Collections):
        for c in Collections:
            self.addCollection(c)
    
    #Add collection by input string.
    @pyqtSlot()
    def on_add_by_edges_button_clicked(self):
        edgesSTR = ""
        while not edgesSTR:
            edgesSTR, ok = QInputDialog.getText(self, "Add by edges", "Please enter a connection:")
            if not ok:
                return
        try:
            edges = eval(edgesSTR)
            if any(len(edge)!=2 for edge in edges):
                raise SyntaxError("Wrong format")
        except Exception as e:
            dlg = QMessageBox(QMessageBox.Warning, str(e), "Error: {}".format(e), (QMessageBox.Ok), self)
            dlg.show()
            dlg.exec_()
            return
        else:
            self.addCollection(edges)
    
    #Show the data of collection.
    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_Collection_list_currentItemChanged(self, item, p0):
        self.delete_button.setEnabled(bool(item))
        if item:
            self.Preview_window.clear()
            item_ = QListWidgetItem(item.text())
            G = self.Collections[self.Collection_list.row(item)]
            item_.setIcon(graph(G, self.Preview_window.iconSize().width(), self.graph_engine.currentText().split(" - ")[1], self.graph_link_as_node.isChecked()))
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
        row = self.Collection_list.currentRow()
        if row>-1:
            self.Preview_window.clear()
            self.Expression_edges.clear()
            self.NL.setText('0')
            self.NJ.setText('0')
            self.DOF.setText('0')
            self.Collection_list.takeItem(row)
            del self.Collections[row]
    
    @pyqtSlot()
    def on_grounded_button_clicked(self):
        # TODO: grounded combinations
        pass
