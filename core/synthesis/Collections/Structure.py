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
from core.io import Qt_images
from networkx import (
    Graph,
    is_isomorphic
)
from core.graphics import (
    graph,
    engine_picker,
    EngineList,
    EngineError
)
from .Ui_Structure import Ui_Form

class TestError(Exception):
    pass

class CollectionsStructure(QWidget, Ui_Form):
    layout_sender = pyqtSignal(Graph, dict)
    
    def __init__(self, parent=None):
        super(CollectionsStructure, self).__init__(parent)
        self.setupUi(self)
        self.outputTo = parent.outputTo
        self.saveReplyBox = parent.saveReplyBox
        self.inputFrom = parent.inputFrom
        self.addPoint_by_graph = parent.addPoint_by_graph
        self.unsaveFunc = parent.workbookNoSave
        self.collections = []
        self.collections_layouts = []
        self.collections_grounded = []
        self.graph_engine.addItems(EngineList)
        self.graph_engine.setCurrentIndex(2)
        self.graph_engine.currentIndexChanged.connect(self.on_reload_atlas_clicked)
    
    def clearSelection(self):
        self.grounded_list.clear()
        self.selection_window.clear()
        self.Expression_edges.clear()
        self.NL.setText('0')
        self.NJ.setText('0')
        self.DOF.setText('0')
    
    def clear(self):
        self.grounded_merge.setEnabled(False)
        self.triangle_button.setEnabled(False)
        self.collections.clear()
        self.collection_list.clear()
        self.clearSelection()
    
    @pyqtSlot()
    def on_clear_button_clicked(self):
        if len(self.collections):
            reply = QMessageBox.question(self, "Delete", "Sure to remove all your collections?",
                (QMessageBox.Apply | QMessageBox.Cancel), QMessageBox.Apply)
            if reply==QMessageBox.Apply:
                self.clear()
                self.unsaveFunc()
    
    def engineErrorMsg(self, e):
        QMessageBox.warning(self, str(e), "Please install and make sure Graphviz is working")
    
    #Reload atlas with the engine.
    @pyqtSlot()
    @pyqtSlot(str)
    def on_reload_atlas_clicked(self, p0=None):
        if self.collections:
            self.collections_layouts.clear()
            self.collection_list.clear()
            self.selection_window.clear()
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
                    engine = engine_picker(G, engineSTR)
                    item.setIcon(graph(G, self.collection_list.iconSize().width(), engine))
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
            if not edges:
                raise TestError("is empty graph.")
            for n in G.nodes:
                if len(list(G.neighbors(n)))<2:
                    raise TestError("is not close chain")
            for H in self.collections:
                if is_isomorphic(G, H):
                    raise TestError("is isomorphic")
        except TestError as e:
            QMessageBox.warning(self, "Add Collection Error", "Error: {}".format(e))
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
            QMessageBox.warning(self, str(e), "Error: {}".format(e))
            return
        else:
            self.addCollection(edges)
    
    #Append atlas by text files
    @pyqtSlot()
    def on_add_by_files_button_clicked(self):
        fileNames = self.inputFrom("Edges data", ["Text File (*.txt)"], multiple=True)
        if fileNames:
            read_data = []
            for fileName in fileNames:
                with open(fileName, 'r') as f:
                    read_data += f.read().split('\n')
            collections = []
            for edges in read_data:
                try:
                    collections.append(Graph(eval(edges)))
                except:
                    QMessageBox.warning(self, "Wrong format", "Please check the edges text format.")
                    return
            if collections:
                self.collections += collections
                self.on_reload_atlas_clicked()
    
    @pyqtSlot()
    def on_save_atlas_clicked(self):
        count = self.collection_list.count()
        if count:
            lateral, ok = QInputDialog.getInt(self, "Atlas", "The number of lateral:", 5, 1, 10)
            if ok:
                fileName = self.outputTo("Atlas image", Qt_images)
                if fileName:
                    icon_size = self.collection_list.iconSize()
                    width = icon_size.width()
                    image_main = QImage(
                        QSize(
                            lateral * width if count>lateral else count * width,
                            ((count // lateral) + bool(count % lateral)) * width
                        ),
                        self.collection_list.item(0).icon().pixmap(icon_size).toImage().format()
                    )
                    image_main.fill(QColor(Qt.white).rgb())
                    painter = QPainter(image_main)
                    for row in range(count):
                        image = self.collection_list.item(row).icon().pixmap(icon_size).toImage()
                        painter.drawImage(QPointF(row % lateral * width, row // lateral * width), image)
                    painter.end()
                    pixmap = QPixmap()
                    pixmap.convertFromImage(image_main)
                    pixmap.save(fileName, format=QFileInfo(fileName).suffix())
                    self.saveReplyBox("Atlas", fileName)
    
    @pyqtSlot()
    def on_save_edges_clicked(self):
        count = self.collection_list.count()
        if count:
            fileName = self.outputTo("Atlas edges expression", ["Text file (*.txt)"])
            if fileName:
                with open(fileName, 'w') as f:
                    f.write('\n'.join(str(G.edges) for G in self.collections))
                self.saveReplyBox("edges expression", fileName)
    
    #Show the data of collection.
    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_collection_list_currentItemChanged(self, item, p0):
        has_item = bool(item)
        self.delete_button.setEnabled(has_item)
        self.grounded_button.setEnabled(has_item)
        self.triangle_button.setEnabled(has_item)
        if item:
            self.selection_window.clear()
            item_ = QListWidgetItem(item.text())
            row = self.collection_list.row(item)
            G = self.collections[row]
            #Save the layout position to keep the graphs will be in same appearance.
            self.ground_engine = self.collections_layouts[row]
            item_.setIcon(graph(G, self.selection_window.iconSize().width(), self.ground_engine))
            self.selection_window.addItem(item_)
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
            reply = QMessageBox.question(self, "Delete", "Sure to remove #{} from your collections?".format(row),
                (QMessageBox.Apply | QMessageBox.Cancel), QMessageBox.Apply)
            if reply==QMessageBox.Apply:
                self.clearSelection()
                self.collection_list.takeItem(row)
                del self.collections[row]
                self.unsaveFunc()
    
    #Triangular iteration
    @pyqtSlot()
    def on_triangle_button_clicked(self):
        G = self.collections[self.collection_list.currentRow()]
        self.layout_sender.emit(G, self.ground_engine)
    
    #Grounded combinations
    @pyqtSlot()
    def on_grounded_button_clicked(self):
        current_item = self.collection_list.currentItem()
        self.collections_grounded.clear()
        self.grounded_list.clear()
        G = self.collections[self.collection_list.row(current_item)]
        item = QListWidgetItem("Released")
        try:
            icon = graph(G, self.grounded_list.iconSize().width(), self.ground_engine)
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
            icon = graph(
                G, self.grounded_list.iconSize().width(),
                self.ground_engine,
                except_node=node
            )
            item.setIcon(icon)
            self.collections_grounded.append(G_)
            self.grounded_list.addItem(item)
        self.grounded_merge.setEnabled(bool(self.grounded_list.count()))
    
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
