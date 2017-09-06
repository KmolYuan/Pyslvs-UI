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
from .io.elements import VPoint, VLink
from typing import TypeVar, Tuple
VPointType = TypeVar('VPointType', int, str)

class BaseTableWidget(QTableWidget):
    name = ''
    deleteRequest = pyqtSignal()
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
    
    def rowTexts(self, row):
        texts = []
        for column in range(self.columnCount()):
            item = self.item(row, column)
            if item is not None:
                texts.append(item.text())
            else:
                texts.append('')
        return tuple(texts)
    
    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Delete:
            self.deleteRequest.emit()

class PointTableWidget(BaseTableWidget):
    name = 'Point'
    def __init__(self, parent=None):
        super(PointTableWidget, self).__init__(1, ['Links', 'Type', 'Color', 'X', 'Y', 'Current'], parent)
        self.editArgs(0, 'ground', 'R', 'Red', '0.0', '0.0')
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 40)
        self.setColumnWidth(3, 90)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 60)
        self.setColumnWidth(6, 60)
        self.draged = False
    
    def data(self) -> Tuple[VPoint]:
        data = []
        for row in range(self.rowCount()):
            Links = self.item(row, 1).text()
            if self.item(row, 2).text()=='R':
                Type = VPoint.R
            elif self.item(row, 2).text()=='P':
                Type = VPoint.P
            elif self.item(row, 2).text()=='RP':
                Type = VPoint.RP
            color = self.item(row, 3).text()
            x = float(self.item(row, 4).text())
            y = float(self.item(row, 5).text())
            v = VPoint(Links, Type, color, x, y)
            c = self.item(row, 6).text().replace('(', '').replace(')', '').split(", ")
            v.move(float(c[0]), float(c[1]))
            data.append(v)
        return tuple(data)
    
    def editArgs(self,
        row: int,
        Links: str,
        Type: VPointType,
        Color: str,
        X, Y
    ):
        Type = 'R' if (Type==0 or Type=='R') else 'P' if (Type==1 or Type=='P') else 'RP'
        for i, e in enumerate(['Point{}'.format(row), Links, Type, Color, X, Y, "({}, {})".format(X, Y)]):
            item = QTableWidgetItem(str(e))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i==3:
                item.setIcon(colorIcons(e))
            self.setItem(row, i, item)
    
    def rename(self, row):
        for j in range(row, self.rowCount()):
            self.setItem(j, 0, QTableWidgetItem(self.name+str(j)))
    
    def updatePosition(self, coordinates):
        for i, (x, y) in enumerate(coordinates):
            text = "({}, {})".format(x, y)
            item = QTableWidgetItem(text)
            item.setToolTip(text)
            self.setItem(i, 6, item)
    
    @pyqtSlot(tuple)
    def setSelections(self, selections: Tuple[int]):
        self.setFocus()
        if QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.setRangesSelected(selections, continueSelect=True)
        else:
            self.setRangesSelected(selections, continueSelect=False)
    
    def setRangesSelected(self, selections, continueSelect):
        selectedRows = self.selectedRows()
        if not continueSelect:
            self.clearSelection()
        self.setCurrentCell(selections[-1], 0)
        for row in selections:
            isSelected = not row in selectedRows
            self.setRangeSelected(
                QTableWidgetSelectionRange(row, 0, row, self.columnCount()-1),
                isSelected)
            self.scrollToItem(self.item(row, 0))
    
    def selectedRows(self):
        a = []
        for r in self.selectedRanges():
            a += [i for i in range(r.topRow(), r.bottomRow()+1)]
        return tuple(sorted(set(a)))
    
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
            if selectedRowCount>1:
                drag = QDrag(self)
                mimeData = QMimeData()
                mimeData.setText(';'.join([str(e) for e in selectedRows]))
                drag.setMimeData(mimeData)
                drag.setPixmap(QPixmap(":/icons/tooltips/needbearings.png").scaledToWidth(50))
                drag.exec_()

class LinkTableWidget(BaseTableWidget):
    name = 'Line'
    dragIn = pyqtSignal(list)
    def __init__(self, parent=None):
        super(LinkTableWidget, self).__init__(1, ['Color', "Points"], parent)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)
        self.editArgs(0, 'ground', 'White', 'Point0')
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 230)
    
    def data(self) -> Tuple[VLink]:
        data = []
        for row in range(self.rowCount()):
            name = self.item(row, 0).text()
            color = self.item(row, 1).text()
            Points = self.item(row, 2).text()
            data.append(VLink(name, color, Points))
        return tuple(data)
    
    def editArgs(self,
        row: int,
        name: str,
        color: str,
        points: str
    ):
        for i, e in enumerate([name, color, points]):
            item = QTableWidgetItem(e)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i==1:
                item.setIcon(colorIcons(e))
            self.setItem(row, i, item)
    
    def dragEnterEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasText():
            if len(mimeData.text().split(';'))>1:
                event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        event.accept()
    
    def dropEvent(self, event):
        self.dragIn.emit([int(e) for e in event.mimeData().text().split(';')])
        event.acceptProposedAction()
