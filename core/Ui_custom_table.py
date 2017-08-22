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

from .QtModules import *
from .graphics.color import colorIcons

class BaseTableWidget(QTableWidget):
    name = ''
    def __init__(self, RowCount, HorizontalHeaderItems, parent=None):
        super(BaseTableWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setRowCount(RowCount)
        self.setColumnCount(len(HorizontalHeaderItems)+1)
        for i, e in enumerate(['Name']+HorizontalHeaderItems):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(e))
    
    def setRowItems(self, row, Args):
        name_set = QTableWidgetItem("{}{}".format(self.name, row))
        name_set.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.setItem(row, 0, name_set)
        for i, e in enumerate(Args):
            if type(e) in [str, float, int]:
                content = '{}{}'.format(self.name, e) if type(e)==int else e
                try:
                    self.setItem(row, i+1, QTableWidgetItem(str(round(float(content), 4))))
                except:
                    try:
                        self.setItem(row, i+1, QTableWidgetItem(colorIcons()[content], content))
                    except KeyError:
                        self.setItem(row, i+1, QTableWidgetItem(content))
            elif type(e)==bool:
                checkbox = QTableWidgetItem()
                checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                checkbox.setCheckState(Qt.Checked if e else Qt.Unchecked)
                self.setItem(row, i+1, checkbox)
    
    def rename(self, index):
        for j in range(index, self.rowCount()):
            self.setItem(j, 0, QTableWidgetItem(self.name+str(j)))

class PointTableWidget(BaseTableWidget):
    name = 'Point'
    def __init__(self, parent=None):
        super(PointTableWidget, self).__init__(1, ['X', 'Y', 'Fixed', 'Color', 'Current'], parent)
        self.setVerticalHeaderItem(0, QTableWidgetItem('Origin'))
        for i, e in enumerate(['Point0', '0.0', '0.0', '', 'Red', "(0.0, 0.0)"]):
            item = QTableWidgetItem(e)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i==3:
                item.setCheckState(Qt.Checked)
            if i==4:
                item.setIcon(colorIcons()['Red'])
            self.setItem(0, i, item)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 45)
        self.setColumnWidth(4, 90)
        self.setColumnWidth(5, 60)
        self.draged = False
    
    @pyqtSlot(list)
    def setSelections(self, selections):
        for selection in selections:
            self.setRangeSelected(selection, True)
    
    def selectedRows(self):
        a = list()
        for r in self.selectedRanges():
            a += [i for i in range(r.topRow(), r.bottomRow()+1)]
        return sorted(set(a))
    
    def mousePressEvent(self, event):
        super(PointTableWidget, self).mousePressEvent(event)
        if event.button()==Qt.LeftButton:
            self.draged = True
    
    def mouseReleaseEvent(self, event):
        super(PointTableWidget, self).mouseReleaseEvent(event)
        self.draged = False
    
    def mouseMoveEvent(self, event):
        if self.draged:
            selectedRows = self.selectedRows()
            selectedRowCount = len(selectedRows)
            if selectedRowCount==2 or selectedRowCount==3:
                drag = QDrag(self)
                mimeData = QMimeData()
                mimeData.setText(';'.join([str(e) for e in selectedRows]))
                drag.setMimeData(mimeData)
                drag.setPixmap(QPixmap(":/icons/tooltips/need{}bearings.png".format(selectedRowCount)).scaledToWidth(50))
                drag.exec_()

class DropTableWidget(BaseTableWidget):
    dragIn = None
    def __init__(self, RowCount, HorizontalHeaderItems, bearings, parent=None):
        super(DropTableWidget, self).__init__(RowCount, HorizontalHeaderItems, parent)
        self.setAcceptDrops(True)
        self.bearings = bearings
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasText():
            if len(mimeData.text().split(';'))==self.bearings:
                event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        event.accept()
    
    def dropEvent(self, event):
        self.dragIn.emit(*[int(e) for e in event.mimeData().text().split(';')])
        event.acceptProposedAction()

class LinkTableWidget(DropTableWidget):
    name = 'Line'
    dragIn = pyqtSignal(int, int)
    def __init__(self, parent=None):
        super(LinkTableWidget, self).__init__(0, ["Start side", "End side", "Length"], 2, parent)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 60)

class ChainTableWidget(DropTableWidget):
    name = 'Chain'
    dragIn = pyqtSignal(int, int, int)
    def __init__(self, parent=None):
        super(ChainTableWidget, self).__init__(0, ['Point[1]', 'Point[2]', 'Point[3]', '[1]-[2]', '[2]-[3]', '[1]-[3]'], 3, parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 60)
        self.setColumnWidth(2, 60)
        self.setColumnWidth(3, 60)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 60)
        self.setColumnWidth(6, 60)

class ShaftTableWidget(BaseTableWidget):
    name = 'Shaft'
    def __init__(self, parent=None):
        super(ShaftTableWidget, self).__init__(0, ['Center', 'Reference', "Start angle(deg)", "End angle(deg)", "Demo angle(deg)"], parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 85)
        self.setColumnWidth(2, 85)
        self.setColumnWidth(3, 110)
        self.setColumnWidth(4, 110)
        self.setColumnWidth(5, 110)

class SliderTableWidget(BaseTableWidget):
    name = 'Slider'
    def __init__(self, parent=None):
        super(SliderTableWidget, self).__init__(0, ['Center', "Start side", "End side"], parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 70)

class RodTableWidget(BaseTableWidget):
    name = 'Rod'
    def __init__(self, parent=None):
        super(RodTableWidget, self).__init__(0, ['Center', "Start side", "End side", 'Position'], parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 70)
        self.setColumnWidth(3, 70)
        self.setColumnWidth(4, 70)

class ParameterTableWidget(BaseTableWidget):
    name = 'n'
    def __init__(self, parent=None):
        super(ParameterTableWidget, self).__init__(0, ['Parameter', 'Comment'], parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 70)
        self.setColumnWidth(2, 80)
