0# -*- coding: utf-8 -*-
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
from .number import NumberSynthesis
from .topologic import topo, as_expression
from .graph import graph_node, graph_link, EngineError
from .Ui_Permutations import Ui_Form

class Permutations_show(QWidget, Ui_Form):
    def __init__(self, parent):
        super(Permutations_show, self).__init__(parent)
        self.setupUi(self)
        self.splitter.setStretchFactor(0, 2)
        self.splitter.setStretchFactor(1, 15)
        self.answer = []
        self.NL_input.valueChanged.connect(self.setDOF)
        self.NJ_input.valueChanged.connect(self.setDOF)
        self.graph_engine.addItems([
            "dot",
            "neato",
            "fdp",
            "twopi",
            "circo",
            "shell",
            "circular",
            "spring",
            "spectral",
            "random"
        ])
        self.graph_engine.setCurrentIndex(1)
        self.graph_degenerate.clicked.connect(self.on_Combine_type_clicked)
        self.graph_link_as_node.clicked.connect(self.on_reload_atlas_clicked)
        self.graph_engine.currentIndexChanged.connect(self.on_reload_atlas_clicked)
        self.Topologic_result.customContextMenuRequested.connect(self.Topologic_result_context_menu)
        self.popMenu_topo = QMenu(self)
        self.copy_edges = QAction("Copy edges", self)
        self.copy_expr = QAction("Copy expression", self)
        self.copy_image = QAction("Copy image", self)
        self.popMenu_topo.addActions([self.copy_edges, self.copy_expr, self.copy_image])
        self.jointDataFunc = parent.Entities_Point.data
        self.linkDataFunc = parent.Entities_Link.data
    
    #Reload button: Auto-combine the mechanism from the workbook.
    @pyqtSlot()
    def on_ReloadMechanism_clicked(self):
        jointData = self.jointDataFunc()
        linkData = self.linkDataFunc()
        self.Expression_joint.setText(", ".join(vpoint.joint for vpoint in jointData))
        NL = sum(1 for vlink in linkData if len(vlink.points)>1)
        NJ = sum(len(vpoint.links)-1 for vpoint in jointData if len(vpoint.links)>1)
        self.NL_input.setValue(NL)
        self.NJ_input.setValue(NJ)
        self.on_Combine_number_clicked()
    
    @pyqtSlot(int)
    def setDOF(self):
        self.DOF_input.setValue(3*(self.NL_input.value()-1) - 2*self.NJ_input.value())
    
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
        if self.answer:
            engine = self.graph_engine.currentText()
            self.Topologic_result.clear()
            progdlg = QProgressDialog("Drawing atlas...", "Cancel", 0, len(self.answer), self)
            progdlg.setWindowTitle("Type synthesis")
            progdlg.resize(400, progdlg.height())
            progdlg.setModal(True)
            progdlg.show()
            for i, G in enumerate(self.answer):
                QCoreApplication.processEvents()
                if progdlg.wasCanceled():
                    return
                item = QListWidgetItem("No. {}".format(i+1))
                if self.graph_link_as_node.isChecked():
                    icon = graph_node
                else:
                    icon = graph_link
                try:
                    item.setIcon(icon(G, self.Topologic_result.iconSize().width(), engine))
                except EngineError as e:
                    progdlg.setValue(progdlg.maximum())
                    dlg = QMessageBox(QMessageBox.Warning, str(e), "Please install and make sure Graphviz is working", (QMessageBox.Ok), self)
                    dlg.show()
                    dlg.exec_()
                    break
                else:
                    item.setToolTip(str(G.edges))
                    self.Topologic_result.addItem(item)
                    progdlg.setValue(i+1)
    
    @pyqtSlot(QPoint)
    def Topologic_result_context_menu(self, point):
        index = self.Topologic_result.currentIndex().row()
        self.copy_edges.setEnabled(index>-1)
        self.copy_expr.setEnabled(index>-1)
        self.copy_image.setEnabled(index>-1)
        action = self.popMenu_topo.exec_(self.Topologic_result.mapToGlobal(point))
        clipboard = QApplication.clipboard()
        if action==self.copy_edges:
            clipboard.setText(str(self.answer[index].edges))
        elif action==self.copy_expr:
            clipboard.setText(str(as_expression(self.answer[index])))
        elif action==self.copy_image:
            clipboard.setPixmap(self.Topologic_result.currentItem().icon().pixmap(self.Topologic_result.iconSize()))
