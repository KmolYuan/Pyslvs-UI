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
from .number import NumberSynthesis
from .topologic import topo
from .graph import graph
from .Ui_Permutations import Ui_Form

class Permutations_show(QWidget, Ui_Form):
    def __init__(self, parent):
        super(Permutations_show, self).__init__(parent)
        self.setupUi(self)
        self.jointDataFunc = parent.Entities_Point.data
        self.linkDataFunc = parent.Entities_Link.data
        self.dofFunc = lambda: parent.DOF
    
    #Reload button: Auto-combine the mechanism from the workbook.
    @pyqtSlot()
    def on_ReloadMechanism_clicked(self):
        jointData = self.jointDataFunc()
        linkData = self.linkDataFunc()
        dof = self.dofFunc()
        self.Expression_joint.setText(", ".join(vpoint.joint for vpoint in jointData))
        NL = sum(1 for vlink in linkData if len(vlink.points)>1)
        NJ = sum(len(vpoint.links)-1 for vpoint in jointData if len(vpoint.links)>1)
        self.NL_input.setValue(NL)
        self.NJ_input.setValue(NJ)
        self.DOF_input.setValue(dof)
        self.on_Combine_number_clicked()
    
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
        self.Topologic_result.clear()
        r = self.Expression_number.currentItem()
        if r and r.text()!="incorrect mechanism.":
            progdlg = QProgressDialog("Analysis of the topology...", "Cancel", 0, 100, self)
            progdlg.setWindowTitle("Type synthesis")
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
                progdlg.setMaximum(maximum)
            answer = topo([int(t.split(" = ")[1]) for t in r.text().split(", ")], setjobFunc, stopFunc)
            if answer:
                setjobFunc("Drawing atlas...", len(answer))
                for i, G in enumerate(answer):
                    QCoreApplication.processEvents()
                    if progdlg.wasCanceled():
                        return
                    item = QListWidgetItem("No. {}".format(i))
                    item.setIcon(graph(G, self.Topologic_result.iconSize().width()))
                    self.Topologic_result.addItem(item)
                    progdlg.setValue(i+1)
