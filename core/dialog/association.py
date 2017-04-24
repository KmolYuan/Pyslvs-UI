# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_association import Ui_Dialog as association_Form

class Association_show(QDialog, association_Form):
    def __init__(self, PointList, LineList, ChainList, ShaftList, SliderList, RodList, parent=None):
        super(Association_show, self).__init__(parent)
        self.setupUi(self)
        self.PointList = PointList
        self.LineList = LineList
        self.ChainList = ChainList
        self.ShaftList = ShaftList
        self.SliderList = SliderList
        self.RodList = RodList
        for i in range(1, len(PointList)):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0, QTableWidgetItem('Point'+str(i)))
    
    @pyqtSlot(int, int, int, int)
    def on_tableWidget_currentCellChanged(self, pos, _cc, _pr, _pc):
        net = list()
        for i, e in enumerate(self.LineList):
            check = [e.start, e.end]
            if pos in check: net.append('Line{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.lineLable.setText('\n'.join(net) if net!=[] else 'None')
        net.clear()
        for i, e in enumerate(self.ChainList):
            check = [e.p1, e.p2, e.p3]
            if pos in check: net.append('Chain{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.chainLable.setText('\n'.join(net) if net!=[] else 'None')
        net.clear()
        for i, e in enumerate(self.ShaftList):
            check = [e.cen, e.ref]
            if pos in check: net.append('Shaft{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.shaftLable.setText('\n'.join(net) if net!=[] else 'None')
        net.clear()
        for i, e in enumerate(self.SliderList):
            check = [e.cen, e.start, e.end]
            if pos in check: net.append('Slider{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.sliderLable.setText('\n'.join(net) if net!=[] else 'None')
        net.clear()
        for i, e in enumerate(self.RodList):
            check = [e.cen, e.start, e.end]
            if pos in check: net.append('Rod{}: '.format(i)+', '.join(['Point{}'.format(k) for k in check if k!=pos]))
        self.rodLable.setText('\n'.join(net) if net!=[] else 'None')
