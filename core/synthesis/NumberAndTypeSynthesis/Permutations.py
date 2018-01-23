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
from networkx import Graph
from core.io import Qt_images, v_to_graph
from core.libs import NumberSynthesis, topo
from core.graphics import (
    graph,
    EngineList,
    EngineError
)
from .Ui_Permutations import Ui_Form

class NumberAndTypeSynthesis(QWidget, Ui_Form):
    def __init__(self, parent):
        super(NumberAndTypeSynthesis, self).__init__(parent)
        self.setupUi(self)
        self.outputTo = parent.outputTo
        self.saveReplyBox = parent.saveReplyBox
        self.inputFrom = parent.inputFrom
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 15)
        self.answer = []
        self.NL_input.valueChanged.connect(self.adjust_NJ_NL_dof)
        self.NJ_input.valueChanged.connect(self.adjust_NJ_NL_dof)
        self.graph_engine.addItems(EngineList)
        self.graph_engine.setCurrentIndex(2)
        self.graph_link_as_node.clicked.connect(self.on_reload_atlas_clicked)
        self.graph_engine.currentIndexChanged.connect(self.on_reload_atlas_clicked)
        self.Topologic_result.customContextMenuRequested.connect(self.Topologic_result_context_menu)
        self.popMenu_topo = QMenu(self)
        self.add_collection = QAction(QIcon(QPixmap(":/icons/collections.png")), "Add to collection", self)
        self.copy_edges = QAction("Copy edges", self)
        self.copy_image = QAction("Copy image", self)
        self.popMenu_topo.addActions([self.add_collection, self.copy_edges, self.copy_image])
        self.jointDataFunc = parent.Entities_Point.data
        self.linkDataFunc = parent.Entities_Link.data
    
    def clear(self):
        self.answer.clear()
        self.Expression_edges.clear()
        self.Expression_number.clear()
        self.Topologic_result.clear()
        self.NL_input.setValue(0)
        self.NJ_input.setValue(0)
        self.DOF.setValue(1)
    
    #Reload button: Auto-combine the mechanism from the workbook.
    @pyqtSlot()
    def on_ReloadMechanism_clicked(self):
        jointData = self.jointDataFunc()
        linkData = self.linkDataFunc()
        if jointData and linkData:
            self.Expression_edges.setText(str(list(v_to_graph(jointData, linkData).edges)))
        else:
            self.Expression_edges.setText("")
        keep_dof_checked = self.keep_dof.isChecked()
        self.keep_dof.setChecked(False)
        self.NL_input.setValue(
            sum(len(vlink.points)>1 for vlink in linkData)+
            sum(len(vpoint.links)-1 for vpoint in jointData if vpoint.type==2 and len(vpoint.links)>1)
        )
        self.NJ_input.setValue(sum((len(vpoint.links)-1 + int(vpoint.type==2)) for vpoint in jointData if len(vpoint.links)>1))
        self.keep_dof.setChecked(keep_dof_checked)
    
    def adjust_NJ_NL_dof(self):
        if self.keep_dof.isChecked():
            if self.sender()==self.NJ_input:
                N2 = self.NJ_input.value()
                NL_func = lambda: float(((self.DOF.value() + 2*N2) / 3) + 1)
            else:
                N2 = self.NL_input.value()
                NL_func = lambda: float((3*(N2-1) - self.DOF.value()) / 2)
            N1 = NL_func()
            while not N1.is_integer():
                N2 += 1
                N1 = NL_func()
                if N2==0:
                    break
            if self.sender()==self.NJ_input:
                self.NJ_input.setValue(N2)
                self.NL_input.setValue(N1)
            else:
                self.NJ_input.setValue(N1)
                self.NL_input.setValue(N2)
        else:
            self.DOF.setValue(3*(self.NL_input.value()-1) - 2*self.NJ_input.value())
    
    #Show number of links with different number of joints.
    @pyqtSlot()
    def on_Combine_number_clicked(self):
        self.Expression_number.clear()
        NS_result = NumberSynthesis(self.NL_input.value(), self.NJ_input.value())
        if type(NS_result)==str:
            item = QListWidgetItem(NS_result)
            item.links = None
            self.Expression_number.addItem(item)
        else:
            for result in NS_result:
                item = QListWidgetItem(", ".join("NL{} = {}".format(i+2, result[i]) for i in range(len(result))))
                item.links = result
                self.Expression_number.addItem(item)
        self.Expression_number.setCurrentRow(0)
    
    #Combine and show progress dialog.
    def combineType(self, row):
        item = self.Expression_number.item(row)
        progdlg = QProgressDialog("Analysis of the topology...", "Cancel", 0, 100, self)
        progdlg.setWindowTitle("Type synthesis - ({})".format(item.text()))
        progdlg.setMinimumSize(QSize(500, 120))
        progdlg.setMaximumSize(QSize(500, 120))
        progdlg.setWindowFlags(progdlg.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        progdlg.setModal(True)
        progdlg.show()
        #Call in every loop.
        def stopFunc():
            QCoreApplication.processEvents()
            progdlg.setValue(progdlg.value()+1)
            return progdlg.wasCanceled()
        def setjobFunc(job, maximum):
            progdlg.setLabelText(job)
            progdlg.setValue(0)
            progdlg.setMaximum(maximum+1)
        answer, time = topo(item.links, not self.graph_degenerate.isChecked(), setjobFunc, stopFunc)
        progdlg.setValue(progdlg.maximum())
        print("Type synthesis {} {:.04f} [s].".format("find in" if answer else "break at", time))
        if answer:
            return [Graph(G.edges) for G in answer]
    
    @pyqtSlot()
    def on_Combine_type_clicked(self):
        row = self.Expression_number.currentRow()
        if not row>-1:
            self.on_Combine_number_clicked()
            row = self.Expression_number.currentRow()
        if self.Expression_number.currentItem().links is None:
            return
        answer = self.combineType(row)
        if answer:
            self.answer = answer
            self.on_reload_atlas_clicked()
    
    @pyqtSlot()
    def on_Combine_type_all_clicked(self):
        if not self.Expression_number.currentRow()>-1:
            self.on_Combine_number_clicked()
        if self.Expression_number.currentItem().links is None:
            return
        answers = []
        break_point = False
        for row in range(self.Expression_number.count()):
            answer = self.combineType(row)
            if answer:
                answers += answer
            else:
                break_point = True
                break
        if answers:
            if break_point:
                reply = QMessageBox.question(self, "Type synthesis - abort", "Do you want to keep the results?",
                    (QMessageBox.Apply | QMessageBox.Cancel), QMessageBox.Apply)
            else:
                reply = QMessageBox.Apply
            if reply==QMessageBox.Apply:
                self.answer = answers
                self.on_reload_atlas_clicked()
    
    @pyqtSlot()
    @pyqtSlot(str)
    def on_reload_atlas_clicked(self, p0=None):
        self.engine = self.graph_engine.currentText().split(" - ")[1]
        self.Topologic_result.clear()
        if self.answer:
            progdlg = QProgressDialog("Drawing atlas...", "Cancel", 0, len(self.answer), self)
            progdlg.setWindowTitle("Type synthesis")
            progdlg.resize(400, progdlg.height())
            progdlg.setModal(True)
            progdlg.show()
            for i, G in enumerate(self.answer):
                QCoreApplication.processEvents()
                if progdlg.wasCanceled():
                    return
                if self.drawAtlas(i, G):
                    progdlg.setValue(i+1)
                else:
                    break
            progdlg.setValue(progdlg.maximum())
    
    def drawAtlas(self, i, G) -> bool:
        item = QListWidgetItem("No. {}".format(i+1))
        try:
            item.setIcon(graph(G, self.Topologic_result.iconSize().width(), self.engine, self.graph_link_as_node.isChecked()))
        except EngineError as e:
            QMessageBox.warning(self, str(e), "Please install and make sure Graphviz is working.")
            return False
        else:
            item.setToolTip(str(G.edges))
            self.Topologic_result.addItem(item)
            return True
    
    @pyqtSlot(QPoint)
    def Topologic_result_context_menu(self, point):
        index = self.Topologic_result.currentIndex().row()
        self.add_collection.setEnabled(index>-1)
        self.copy_edges.setEnabled(index>-1)
        self.copy_image.setEnabled(index>-1)
        action = self.popMenu_topo.exec_(self.Topologic_result.mapToGlobal(point))
        if action:
            clipboard = QApplication.clipboard()
            if action==self.add_collection:
                self.addCollection(self.answer[index].edges)
            elif action==self.copy_edges:
                clipboard.setText(str(self.answer[index].edges))
            elif action==self.copy_image:
                #Turn the transparent background to white.
                image1 = self.Topologic_result.currentItem().icon().pixmap(self.Topologic_result.iconSize()).toImage()
                image2 = QImage(image1.size(), image1.format())
                image2.fill(QColor(Qt.white).rgb())
                painter = QPainter(image2)
                painter.drawImage(QPointF(0, 0), image1)
                painter.end()
                pixmap = QPixmap()
                pixmap.convertFromImage(image2)
                clipboard.setPixmap(pixmap)
    
    @pyqtSlot()
    def on_Expression_copy_clicked(self):
        string = self.Expression_edges.text()
        if string:
            clipboard = QApplication.clipboard()
            clipboard.setText(string)
            self.Expression_edges.selectAll()
    
    @pyqtSlot()
    def on_Expression_add_collection_clicked(self):
        string = self.Expression_edges.text()
        if string:
            self.addCollection(eval(string))
    
    @pyqtSlot()
    def on_save_atlas_clicked(self):
        fileName = ""
        lateral = 0
        if self.save_edges_auto.isChecked():
            lateral, ok = QInputDialog.getInt(self, "Atlas", "The number of lateral:", 5, 1, 10)
            if ok:
                fileName = self.outputTo("Atlas image", Qt_images)
                if fileName:
                    reply = QMessageBox.question(self, "Type synthesis", "Do you want to Re-synthesis?",
                        (QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.Cancel), QMessageBox.YesToAll)
                    if reply==QMessageBox.Yes:
                        self.on_Combine_type_clicked()
                    elif reply==QMessageBox.YesToAll:
                        self.on_Combine_type_all_clicked()
        count = self.Topologic_result.count()
        if count:
            if not lateral:
                lateral, ok = QInputDialog.getInt(self, "Atlas", "The number of lateral:", 5, 1, 10)
            if ok:
                if not fileName:
                    fileName = self.outputTo("Atlas image", Qt_images)
                if fileName:
                    icon_size = self.Topologic_result.iconSize()
                    width = icon_size.width()
                    image_main = QImage(
                        QSize(
                            lateral * width if count>lateral else count * width,
                            ((count // lateral) + bool(count % lateral)) * width
                        ),
                        self.Topologic_result.item(0).icon().pixmap(icon_size).toImage().format()
                    )
                    image_main.fill(QColor(Qt.white).rgb())
                    painter = QPainter(image_main)
                    for row in range(count):
                        image = self.Topologic_result.item(row).icon().pixmap(icon_size).toImage()
                        painter.drawImage(QPointF(row % lateral * width, row // lateral * width), image)
                    painter.end()
                    pixmap = QPixmap()
                    pixmap.convertFromImage(image_main)
                    pixmap.save(fileName, format=QFileInfo(fileName).suffix())
                    self.saveReplyBox("Atlas", fileName)
    
    @pyqtSlot()
    def on_save_edges_clicked(self):
        fileName = ""
        if self.save_edges_auto.isChecked():
            fileName = self.outputTo("Atlas edges expression", ["Text file (*.txt)"])
            if fileName:
                reply = QMessageBox.question(self, "Type synthesis", "Do you want to Re-synthesis?",
                    (QMessageBox.Yes | QMessageBox.YesToAll | QMessageBox.Cancel), QMessageBox.YesToAll)
                if reply==QMessageBox.Yes:
                    self.on_Combine_type_clicked()
                elif reply==QMessageBox.YesToAll:
                    self.on_Combine_type_all_clicked()
        count = self.Topologic_result.count()
        if count:
            if not fileName:
                fileName = self.outputTo("Atlas edges expression", ["Text file (*.txt)"])
            if fileName:
                with open(fileName, 'w') as f:
                    f.write('\n'.join(str(G.edges) for G in self.answer))
                self.saveReplyBox("edges expression", fileName)
    
    @pyqtSlot()
    def on_Edges_to_altas_clicked(self):
        fileNames = self.inputFrom("Edges data", ["Text File (*.txt)"], multiple=True)
        if fileNames:
            read_data = []
            for fileName in fileNames:
                with open(fileName, 'r') as f:
                    read_data += f.read().split('\n')
            answer = []
            for edges in read_data:
                try:
                    answer.append(Graph(eval(edges)))
                except:
                    QMessageBox.warning(self, "Wrong format", "Please check the edges text format.")
                    return
            if answer:
                self.answer = answer
                self.on_reload_atlas_clicked()
                check_status = self.save_edges_auto.isChecked()
                self.save_edges_auto.setChecked(False)
                self.on_save_atlas_clicked()
                self.save_edges_auto.setChecked(check_status)
