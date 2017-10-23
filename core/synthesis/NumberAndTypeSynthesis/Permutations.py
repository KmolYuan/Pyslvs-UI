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
from .Ui_Permutations import Ui_Form
from itertools import product

class NumberSynthesis:
    def __init__(self, NL, NJ):
        self.NL = NL
        self.NJ = NJ
    
    @property
    def Mmax(self):
        if self.NL <= self.NJ and self.NJ <= (2*self.NL-3):
            return self.NJ - self.NL + 2
        elif (2*self.NL-3) <= self.NJ and self.NJ <= (self.NL*(self.NL-1)/2):
            return self.NL - 1
        else:
            raise ValueError("incorrect mechanism.")
    
    @property
    def NLm(self):
        result = []
        correction = lambda l: sum((i+2)*l[i] for i in range(len(l))) == 2*self.NJ
        try:
            Mmax = self.Mmax
        except ValueError as e:
            return str(e)
        else:
            for symbols in product(range(self.NL+1), repeat=Mmax-2):
                NLMmax = self.NL - sum(symbols)
                answer = symbols+(NLMmax,)
                if correction(answer) and NLMmax>=0:
                    result.append(answer)
            return tuple(result)

class Permutations_show(QWidget, Ui_Form):
    def __init__(self, jointDataFunc, linkDataFunc, dofFunc, parent=None):
        super(Permutations_show, self).__init__(parent)
        self.setupUi(self)
        self.jointDataFunc = jointDataFunc
        self.linkDataFunc = linkDataFunc
        self.dofFunc = dofFunc
        self.Representation_tree.expanded.connect(self.resizeHeader)
        self.Representation_tree.collapsed.connect(self.resizeHeader)
    
    @pyqtSlot()
    def on_ReloadMechanism_clicked(self):
        jointData = self.jointDataFunc()
        linkData = self.linkDataFunc()
        dof = self.dofFunc()
        self.Representation_joint.setText("M[{}]".format(", ".join(str(vpoint) for vpoint in jointData)))
        self.Representation_link.setText("M[{}]".format(", ".join(str(vlink) for vlink in linkData)))
        self.Representation_tree.clear()
        #Show mechanism system.
        root = QTreeWidgetItem(["Mechanism root"])
        root.setIcon(0, QIcon(QPixmap(":/icons/mechanism.png")))
        self.Representation_tree.addTopLevelItem(root)
        NL = len(tuple(None for vlink in linkData if len(vlink.points)>1))
        NJ = len(tuple(None for vpoint in jointData if len(vpoint.links)>1))
        NS = NumberSynthesis(NL, NJ)
        NS_result = NS.NLm
        root.addChildren([
            QTreeWidgetItem(["Degree of freedom", str(dof)]),
            QTreeWidgetItem(["Number of links", str(NL)]),
            QTreeWidgetItem(["Number of joints", str(NJ)]),
            QTreeWidgetItem(["Distant relatives", (
                NS_result if type(NS_result)==str else
                ", ".join("; ".join("NL{} = {}".format(i+2, result[i]) for i in range(len(result))) for result in NS_result)
            )]),
        ])
        '''
        TODO: Topologic
        
        for vlink in linkData:
            node = QTreeWidgetItem([vlink.name])
            node.setIcon(0, QIcon(QPixmap(":/icons/link.png")))
            root.addChild(node)
            node.addChild(QTreeWidgetItem(["Number of joints", str(sum(len(jointData[i].links)-1 for i in vlink.points))]))
            for i in vlink.points:
                vpoint = jointData[i]
                p = QTreeWidgetItem(["Point{}".format(i)])
                p.setIcon(0, QIcon(QPixmap(":/icons/bearing.png")))
                p.addChild(QTreeWidgetItem(["Joint type", vpoint.typeSTR]))
                for link in vpoint.links:
                    if link!=vlink.name:
                        p.addChild(QTreeWidgetItem(["Connect to Link", link]))
                node.addChild(p)
                self.Representation_tree.expandItem(p)
            self.Representation_tree.expandItem(node)
        '''
        self.Representation_tree.expandItem(root)
    
    @pyqtSlot(QModelIndex)
    def resizeHeader(self, index=None):
        for i in range(self.Representation_tree.columnCount()):
            self.Representation_tree.resizeColumnToContents(i)
