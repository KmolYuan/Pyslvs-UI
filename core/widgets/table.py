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
from ..graphics.color import colorIcons
from ..io.elements import VPoint, VLink
from typing import TypeVar, Tuple
VPointType = TypeVar('VPointType', int, str)

class BaseTableWidget(QTableWidget):
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
        for i, e in enumerate(('Name',)+HorizontalHeaderItems):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(e))
    
    #Get the whole row of texts.
    def rowTexts(self, row):
        texts = []
        for column in range(self.columnCount()):
            item = self.item(row, column)
            if item is not None:
                texts.append(item.text())
            else:
                texts.append('')
        return tuple(texts)
    
    #Get what row is been selected.
    def selectedRows(self) -> Tuple[int]:
        a = set()
        for r in self.selectedRanges():
            a |= {i for i in range(r.topRow(), r.bottomRow()+1)}
        return tuple(sorted(a))
    
    #Hit the delete key, will emit delete signal from this table.
    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Delete:
            self.deleteRequest.emit()

class PointTableWidget(BaseTableWidget):
    name = 'Point'
    rowSelectionChanged = pyqtSignal(tuple, tuple)
    
    def __init__(self, parent=None):
        super(PointTableWidget, self).__init__(0, ('Links', 'Type', 'Color', 'X', 'Y', 'Current'), parent)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 40)
        self.setColumnWidth(3, 90)
        self.setColumnWidth(4, 60)
        self.setColumnWidth(5, 60)
        self.setColumnWidth(6, 60)
        self.draged = False
    
    #Get the digitization of all table data.
    def data(self, index=-1) -> Tuple[VPoint]:
        def get(row):
            Links = self.item(row, 1).text()
            color = self.item(row, 3).text()
            x = float(self.item(row, 4).text())
            y = float(self.item(row, 5).text())
            '''
            Type = (type:str, angle:float)
            '''
            Type = self.item(row, 2).text().split(':')
            if Type[0]=='R':
                Type = 0
                angle = 0.
            else:
                angle = float(Type[1])
                if Type[0]=='P':
                    Type = 1
                elif Type[0]=='RP':
                    Type = 2
            v = VPoint(Links, Type, angle, color, x, y)
            v.move(*self.currentPosition(row))
            return v
        if index==-1:
            data = []
            for row in range(self.rowCount()):
                data.append(get(row))
            return tuple(data)
        else:
            return get(index)
    
    #Edite a point.
    def editArgs(self,
        row: int,
        Links: str,
        Type: str,
        Color: str,
        X, Y
    ):
        for i, e in enumerate(['Point{}'.format(row), Links, Type, Color, X, Y, "({}, {})".format(X, Y)]):
            item = QTableWidgetItem(str(e))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i==3:
                item.setIcon(colorIcons(e))
            self.setItem(row, i, item)
    
    #When index changed, the points need to rename.
    def rename(self, row):
        for j in range(row, self.rowCount()):
            self.setItem(j, 0, QTableWidgetItem(self.name+str(j)))
    
    #Get the current coordinate from a point.
    def currentPosition(self, row: int) -> Tuple[float, float]:
        return tuple(tuple(float(p) for p in coordinate.split(", "))
            for coordinate in self.item(row, 6).text().replace('(', '').replace(')', '').split("; "))
    
    #Update the current coordinate for a point.
    def updateCurrentPosition(self, coordinates: Tuple[Tuple[Tuple[float, float],],]):
        for i, coordinate in enumerate(coordinates):
            if type(coordinate[0])==float:
                text = "({}, {})".format(*coordinate)
            else:
                text = "; ".join("({}, {})".format(*c) for c in coordinate)
            item = QTableWidgetItem(text)
            item.setToolTip(text)
            self.setItem(i, 6, item)
    
    #Let all points go back to the origin coordinate.
    def getBackOrigin(self):
        self.updateCurrentPosition(tuple(
            (float(self.item(row, 4).text()), float(self.item(row, 5).text()))
            for row in range(self.rowCount())
        ))
    
    #Auto select function, get the signal from canvas.
    @pyqtSlot(tuple)
    def setSelections(self, selections: Tuple[int]):
        self.setFocus()
        if QApplication.keyboardModifiers()==Qt.ShiftModifier:
            self.setRangesSelected(selections, continueSelect=True, UnSelect=False)
        elif QApplication.keyboardModifiers()==Qt.ControlModifier:
            self.setRangesSelected(selections, continueSelect=True)
        else:
            self.setRangesSelected(selections, continueSelect=False, UnSelect=False)
        distance = []
        selectedRows = self.selectedRows()
        if len(selectedRows)>1:
            data = self.data()
            for i, row in enumerate(selectedRows):
                if i==len(selectedRows)-1:
                    break
                distance.append(round(data[row].distance(data[selectedRows[i+1]]), 4))
        self.rowSelectionChanged.emit(selectedRows, tuple(distance))
    
    #Different mode of select function.
    def setRangesSelected(self, selections, continueSelect=True, UnSelect=True):
        selectedRows = self.selectedRows()
        if not continueSelect:
            self.clearSelection()
        self.setCurrentCell(selections[-1], 0)
        for row in selections:
            isSelected = not row in selectedRows
            self.setRangeSelected(
                QTableWidgetSelectionRange(row, 0, row, self.columnCount()-1),
                isSelected if UnSelect else True)
            self.scrollToItem(self.item(row, 0))
    
    #Overwrite "clearSelection" slot, so it will emit "rowSelectionChanged" signal.
    @pyqtSlot()
    def clearSelection(self):
        super(PointTableWidget, self).clearSelection()
        self.rowSelectionChanged.emit((), ())
    
    #Drag-out functions.
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
                drag.setPixmap(QPixmap(":/icons/bearing.png").scaledToWidth(30))
                drag.exec_()

class LinkTableWidget(BaseTableWidget):
    name = 'Line'
    dragIn = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super(LinkTableWidget, self).__init__(1, ('Color', 'Points'), parent)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)
        self.editArgs(0, 'ground', 'White', '')
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 90)
        self.setColumnWidth(2, 230)
    
    #Get the digitization of all table data.
    def data(self) -> Tuple[VLink]:
        data = []
        for row in range(self.rowCount()):
            name = self.item(row, 0).text()
            color = self.item(row, 1).text()
            try:
                points = tuple(int(p.replace('Point', '')) for p in self.item(row, 2).text().split(','))
            except:
                points = ()
            data.append(VLink(name, color, points))
        return tuple(data)
    
    #Edite a link.
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
    
    #Drag-in functions.
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

class SelectionLabel(QLabel):
    def __init__(self, *Args):
        super(SelectionLabel, self).__init__(*Args)
        self.updateSelectPoint()
    
    #This QLabel can show distance in status bar.
    @pyqtSlot()
    @pyqtSlot(tuple, tuple)
    def updateSelectPoint(self, points=(), distance=()):
        text = ""
        if points:
            text += "Selected: {}".format('-'.join('[{}]'.format(p) for p in points))
        if distance:
            text += " | {}".format(", ".join('({})'.format(d) for d in distance))
        if text:
            self.setText(text)
        else:
            self.setText("No selection.")
    
    @pyqtSlot(float, float)
    def updateMousePosition(self, x, y):
        self.setText("Mouse at: ({}, {})".format(x, y))
