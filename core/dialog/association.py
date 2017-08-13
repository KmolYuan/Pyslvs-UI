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

from ..QtModules import *
from .Ui_association import Ui_Dialog as association_Form

class Association_show(QDialog, association_Form):
    def __init__(self, Point, Line, Chain, Shaft, Slider, Rod, parent=None):
        super(Association_show, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setupUi(self)
        self.splitter.setSizes([400, 500])
        self.Point = Point
        self.Line = Line
        self.Chain = Chain
        self.Shaft = Shaft
        self.Slider = Slider
        self.Rod = Rod
        for i in range(1, len(Point)):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem('Point'+str(i)))
    
    @pyqtSlot(int, int, int, int)
    def on_tableWidget_currentCellChanged(self, pos, _cc, _pr, _pc):
        net = list()
        for i, e in enumerate(self.Line):
            check = [e.start, e.end]
            if pos in check:
                net.append('Line{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.lineLable.setText('\n'.join(net) if net!=[] else 'None')
        net.clear()
        for i, e in enumerate(self.Chain):
            check = [e.p1, e.p2, e.p3]
            if pos in check:
                net.append('Chain{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.chainLable.setText('\n'.join(net) if net!=[] else 'None')
        net.clear()
        for i, e in enumerate(self.Shaft):
            check = [e.cen, e.ref]
            if pos in check:
                net.append('Shaft{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.shaftLable.setText('\n'.join(net) if net!=[] else 'None')
        net.clear()
        for i, e in enumerate(self.Slider):
            check = [e.cen, e.start, e.end]
            if pos in check:
                net.append('Slider{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.sliderLable.setText('\n'.join(net) if net!=[] else 'None')
        net.clear()
        for i, e in enumerate(self.Rod):
            check = [e.cen, e.start, e.end]
            if pos in check:
                net.append('Rod{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.rodLable.setText('\n'.join(net) if net!=[] else 'None')
