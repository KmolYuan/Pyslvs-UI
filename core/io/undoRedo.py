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
from copy import deepcopy

noNoneString = lambda l: [e for e in l if e]

'''
The add and delete command has only add and delete.
The add command need to edit Points or Links list after it added to table.
The delete command need to clear Points or Links list before it deleted from table.
'''

class addTableCommand(QUndoCommand):
    def __init__(self, table):
        QUndoCommand.__init__(self)
        self.table = table
    
    def redo(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for column in range(row):
            self.table.setItem(row, column, QTableWidgetItem(''))
    
    def undo(self):
        self.table.removeRow(self.table.rowCount()-1)

class deleteTableCommand(QUndoCommand):
    def __init__(self, table, row, isRename):
        QUndoCommand.__init__(self)
        self.table = table
        self.row = row
        self.isRename = isRename
    
    def redo(self):
        self.table.removeRow(self.row)
        if self.isRename:
            self.table.rename(self.row)
    
    def undo(self):
        if self.isRename:
            self.table.rename(self.row)
        self.table.insertRow(self.row)
        for column in range(self.table.columnCount()):
            self.table.setItem(self.row, column, QTableWidgetItem(''))

#Fix sequence number when deleting a point.
class fixSequenceNumberCommand(QUndoCommand):
    def __init__(self, table, row, q):
        QUndoCommand.__init__(self)
        self.table = table
        self.row = row
        self.q = q
    
    def redo(self):
        self.sorting(True)
    
    def undo(self):
        self.sorting(False)
    
    #Sorting point number by q.
    def sorting(self, bs):
        item = self.table.item(self.row, 2)
        if item.text():
            points = [int(p.replace('Point', '')) for p in item.text().split(',')]
            if bs:
                points = [p-1 if p>self.q else p for p in points]
            else:
                points = [p+1 if p>=self.q else p for p in points]
            points = ['Point{}'.format(p) for p in points]
            item.setText(','.join(points))

'''
The edit command need to know who is included by the VPoint or VLink.
'''

class editPointTableCommand(QUndoCommand):
    def __init__(self, PointTable, row, LinkTable, Args):
        QUndoCommand.__init__(self)
        self.PointTable = PointTable
        self.row = row
        self.LinkTable = LinkTable
        '''
        Links: str,
        Type: int,
        Color: str,
        X, Y
        '''
        self.Args = tuple(Args)
        self.OldArgs = self.PointTable.rowTexts(row)[1:-1]
        #Links: Tuple[str] -> Set[str]
        newLinks = set(self.Args[0].split(','))
        oldLinks = set(self.OldArgs[0].split(','))
        self.NewLinkRows = []
        self.OldLinkRows = []
        for row in range(self.LinkTable.rowCount()):
            linkName = self.LinkTable.item(row, 0).text()
            if linkName in newLinks - oldLinks:
                self.NewLinkRows.append(row)
            if linkName in oldLinks - newLinks:
                self.OldLinkRows.append(row)
        self.NewLinkRows = tuple(self.NewLinkRows)
        self.OldLinkRows = tuple(self.OldLinkRows)
    
    def redo(self):
        self.PointTable.editArgs(self.row, *self.Args)
        self.writeRows(self.NewLinkRows, self.OldLinkRows)
    
    def undo(self):
        self.writeRows(self.OldLinkRows, self.NewLinkRows)
        self.PointTable.editArgs(self.row, *self.OldArgs)
    
    def writeRows(self, rows1, rows2):
        #Append the point that relate with these links.
        for row in rows1:
            newPoints = self.LinkTable.item(row, 2).text().split(',')+['Point{}'.format(self.row)]
            item = QTableWidgetItem(','.join(noNoneString(newPoints)))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.LinkTable.setItem(row, 2, item)
        #Remove the point that irrelevant with these links.
        for row in rows2:
            newPoints = self.LinkTable.item(row, 2).text().split(',')
            newPoints.remove('Point{}'.format(self.row))
            item = QTableWidgetItem(','.join(noNoneString(newPoints)))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.LinkTable.setItem(row, 2, item)

class editLinkTableCommand(QUndoCommand):
    def __init__(self, LinkTable, row, PointTable, Args):
        QUndoCommand.__init__(self)
        self.LinkTable = LinkTable
        self.row = row
        self.PointTable = PointTable
        '''
        name: str,
        color: str,
        points: str
        '''
        self.Args = tuple(Args)
        self.OldArgs = self.LinkTable.rowTexts(row)
        #Points: Tuple[int]
        newPoints = self.Args[2].split(',')
        oldPoints = self.OldArgs[2].split(',')
        newPoints = set(int(index.replace('Point', '')) for index in noNoneString(newPoints))
        oldPoints = set(int(index.replace('Point', '')) for index in noNoneString(oldPoints))
        self.NewPointRows = tuple(newPoints - oldPoints)
        self.OldPointRows = tuple(oldPoints - newPoints)
    
    def redo(self):
        self.LinkTable.editArgs(self.row, *self.Args)
        self.rename(self.Args, self.OldArgs)
        self.writeRows(self.Args[0], self.NewPointRows, self.OldPointRows)
    
    def undo(self):
        self.writeRows(self.OldArgs[0], self.OldPointRows, self.NewPointRows)
        self.rename(self.OldArgs, self.Args)
        self.LinkTable.editArgs(self.row, *self.OldArgs)
    
    def rename(self, Args1, Args2):
        for row in [int(index.replace('Point', '')) for index in noNoneString(Args2[2].split(','))]:
            newLinks = self.PointTable.item(row, 1).text().split(',')
            item = QTableWidgetItem(','.join(noNoneString([w.replace(Args2[0], Args1[0]) for w in newLinks])))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.PointTable.setItem(row, 1, item)
    
    def writeRows(self, name, rows1, rows2):
        #Append the link that relate with these points.
        for row in rows1:
            newLinks = self.PointTable.item(row, 1).text().split(',')+[name]
            item = QTableWidgetItem(','.join(noNoneString(newLinks)))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.PointTable.setItem(row, 1, item)
        #Remove the link that irrelevant with these points.
        for row in rows2:
            newLinks = self.PointTable.item(row, 1).text().split(',')
            if name:
                newLinks.remove(name)
            item = QTableWidgetItem(','.join(noNoneString(newLinks)))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.PointTable.setItem(row, 1, item)

class addPathCommand(QUndoCommand):
    def __init__(self, widget, name, data, path):
        QUndoCommand.__init__(self)
        self.widget = widget
        self.name = name
        self.data = data
        self.path = deepcopy(path)
    
    def redo(self):
        self.data[self.name] = self.path
        self.widget.addItem("{}: {}".format(self.name, ", ".join("[{}]".format(i) for i, d in enumerate(self.path) if d)))
    
    def undo(self):
        self.widget.takeItem(self.widget.count()-1)
        del self.data[self.name]

class deletePathCommand(QUndoCommand):
    def __init__(self, row, widget, data):
        QUndoCommand.__init__(self)
        self.row = row
        self.widget = widget
        self.data = data
    
    def redo(self):
        self.oldItem = self.widget.takeItem(self.row)
        name = self.oldItem.text().split(':')[0]
        self.oldPath = self.data[name]
        del self.data[name]
    
    def undo(self):
        self.data[self.oldItem.text().split(':')[0]] = self.oldPath
        self.widget.addItem(self.oldItem)

class addStorageCommand(QUndoCommand):
    def __init__(self, name, widget, mechanism):
        QUndoCommand.__init__(self)
        self.name = name
        self.widget = widget
        self.mechanism = mechanism
    
    def redo(self):
        item = QListWidgetItem(self.name)
        item.expr = self.mechanism
        item.setIcon(QIcon(QPixmap(":/icons/mechanism.png")))
        self.widget.addItem(item)
    
    def undo(self):
        self.widget.takeItem(self.widget.count()-1)

class addStorageNameCommand(QUndoCommand):
    def __init__(self, name, widget):
        QUndoCommand.__init__(self)
        self.name = name
        self.widget = widget
    
    def redo(self):
        self.widget.setText(self.name)
    
    def undo(self):
        self.widget.clear()

class deleteStorageCommand(QUndoCommand):
    def __init__(self, row, widget):
        QUndoCommand.__init__(self)
        self.row = row
        self.widget = widget
        self.name = widget.item(row).text()
        self.mechanism = widget.item(row).expr
    
    def redo(self):
        self.widget.takeItem(self.row)
    
    def undo(self):
        item = QListWidgetItem(self.name)
        item.expr = self.mechanism
        item.setIcon(QIcon(QPixmap(":/icons/mechanism.png")))
        self.widget.insertItem(self.row, item)

class clearStorageNameCommand(QUndoCommand):
    def __init__(self, widget):
        QUndoCommand.__init__(self)
        self.name = widget.text()
        if not self.name:
            self.name = widget.placeholderText()
        self.widget = widget
    
    def redo(self):
        self.widget.clear()
    
    def undo(self):
        self.widget.setText(self.name)
