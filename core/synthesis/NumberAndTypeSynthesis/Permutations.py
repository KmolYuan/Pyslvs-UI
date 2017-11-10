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
        elif self.NL == self.NJ and self.NJ == 0:
            raise ValueError("incorrect mechanism.")
        elif (2*self.NL-3) <= self.NJ and self.NJ <= (self.NL*(self.NL-1)/2):
            return self.NL - 1
        else:
            raise ValueError("incorrect mechanism.")
    
    @property
    def NLm(self):
        result = []
        correction = lambda l: sum((i+2)*l[i] for i in range(len(l))) == 2*self.NJ
        Mmax = self.Mmax
        for symbols in product(range(self.NL+1), repeat=Mmax-2):
            NLMmax = self.NL - sum(symbols)
            if NLMmax < 0:
                continue
            answer = symbols+(NLMmax,)
            if correction(answer):
                result.append(answer)
        return tuple(result)

class Permutations_show(QWidget, Ui_Form):
    def __init__(self, jointDataFunc, linkDataFunc, dofFunc, parent=None):
        super(Permutations_show, self).__init__(parent)
        self.setupUi(self)
        self.jointDataFunc = jointDataFunc
        self.linkDataFunc = linkDataFunc
        self.dofFunc = dofFunc
    
    #Reload button: Auto-combine the mechanism from the workbook.
    @pyqtSlot()
    def on_ReloadMechanism_clicked(self):
        jointData = self.jointDataFunc()
        linkData = self.linkDataFunc()
        dof = self.dofFunc()
        self.Expression_joint.setText("M[{}]".format(", ".join(str(vpoint) for vpoint in jointData)))
        self.Expression_link.setText("M[{}]".format(", ".join(str(vlink) for vlink in linkData)))
        NL = len(tuple(None for vlink in linkData if len(vlink.points)>1))
        NJ = len(tuple(None for vpoint in jointData if len(vpoint.links)>1))
        self.NL_input.setValue(NL)
        self.NJ_input.setValue(NJ)
        self.DOF_input.setValue(dof)
        self.on_Combine_number_clicked()
        self.on_Combine_type_clicked()
    
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
        '''TODO: Topologic'''
