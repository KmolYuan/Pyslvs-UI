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
from ...io.elements import v_to_graph
from .number import NumberSynthesis
from .topologic import topo
from .graph import (
    graph,
    EngineList,
    EngineError
)
from .Ui_Permutations import Ui_Form

class Permutations_show(QWidget, Ui_Form):
    def __init__(self, parent):
        super(Permutations_show, self).__init__(parent)
        self.setupUi(self)
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
        self.DOF.setValue(0)
    
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
        self.on_Combine_number_clicked()
    
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
        NS = NumberSynthesis(self.NL_input.value(), self.NJ_input.value())
        self.Expression_number.clear()
        try:
            NS_result = NS.NLm
        except ValueError as e:
            self.Expression_number.addItem(str(e))
        else:
            for result in NS_result:
                self.Expression_number.addItem(", ".join("NL{} = {}".format(i+2, result[i]) for i in range(len(result))))
        self.Expression_number.setCurrentRow(0)
    
    @pyqtSlot()
    def on_Combine_type_clicked(self):
        r = self.Expression_number.currentItem()
        if r and r.text()!="incorrect mechanism.":
            progdlg = QProgressDialog("Analysis of the topology...", "Cancel", 0, 100, self)
            progdlg.setWindowTitle("Type synthesis")
            progdlg.resize(400, progdlg.height())
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
            answer = topo(
                [int(t.split(" = ")[1]) for t in r.text().split(", ")],
                not self.graph_degenerate.isChecked(),
                setjobFunc,
                stopFunc
            )
            progdlg.setValue(progdlg.maximum())
            if answer:
                self.answer = answer
                self.on_reload_atlas_clicked()
    
    @pyqtSlot()
    @pyqtSlot(str)
    def on_reload_atlas_clicked(self, p0=None):
        self.Topologic_result.clear()
        if self.answer:
            progdlg = QProgressDialog("Drawing atlas...", "Cancel", 0, len(self.answer), self)
            progdlg.setWindowTitle("Type synthesis")
            progdlg.resize(400, progdlg.height())
            progdlg.setModal(True)
            progdlg.show()
            engine = self.graph_engine.currentText().split(" - ")[1]
            for i, G in enumerate(self.answer):
                QCoreApplication.processEvents()
                if progdlg.wasCanceled():
                    return
                item = QListWidgetItem("No. {}".format(i+1))
                try:
                    item.setIcon(graph(G, self.Topologic_result.iconSize().width(), engine, self.graph_link_as_node.isChecked()))
                except EngineError as e:
                    progdlg.setValue(progdlg.maximum())
                    QMessageBox.warning(self, str(e), "Please install and make sure Graphviz is working", QMessageBox.Ok, QMessageBox.Ok)
                    break
                else:
                    item.setToolTip(str(G.edges))
                    self.Topologic_result.addItem(item)
                    progdlg.setValue(i+1)
    
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
                painter.drawImage(0, 0, image1)
                p = QPixmap()
                p.convertFromImage(image2)
                clipboard.setPixmap(p)
    
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
