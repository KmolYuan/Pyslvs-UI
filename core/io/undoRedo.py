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
from copy import copy, deepcopy

noNoneString = lambda l: list(filter(lambda a: a!='', l))

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
        self.table.insertRow(self.table.rowCount())
    
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
        self.table.insertRow(self.row)
        if self.isRename:
            self.table.rename(self.row)

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
        for row in rows1:
            newPoints = self.LinkTable.item(row, 2).text().split(',')+['Point{}'.format(self.row)]
            newPoints = noNoneString(newPoints)
            self.LinkTable.editArgs(row,
                self.LinkTable.item(row, 0).text(),
                self.LinkTable.item(row, 1).text(),
                ','.join(newPoints))
        for row in rows2:
            newPoints = self.LinkTable.item(row, 2).text().split(',')
            newPoints.remove('Point{}'.format(self.row))
            newPoints = noNoneString(newPoints)
            self.LinkTable.editArgs(row,
                self.LinkTable.item(row, 0).text(),
                self.LinkTable.item(row, 1).text(),
                ','.join(newPoints))

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
        self.NewPointRows = newPoints - oldPoints
        self.OldPointRows = oldPoints - newPoints
    
    def redo(self):
        self.LinkTable.editArgs(self.row, *self.Args)
        self.rename(self.Args, self.OldArgs)
        self.writeRows(self.NewPointRows, self.OldPointRows)
    
    def undo(self):
        self.writeRows(self.OldPointRows, self.NewPointRows)
        self.rename(self.OldArgs, self.Args)
        self.LinkTable.editArgs(self.row, *self.OldArgs)
    
    def rename(self, Args1, Args2):
        for row in [int(index.replace('Point', '')) for index in noNoneString(Args2[2].split(','))]:
            self.PointTable.editArgs(row,
                ','.join([w.replace(Args2[0], Args1[0]) for w in self.PointTable.item(row, 1).text().split(',')]),
                self.PointTable.item(row, 2).text(),
                self.PointTable.item(row, 3).text(),
                self.PointTable.item(row, 4).text(),
                self.PointTable.item(row, 5).text())
    
    def writeRows(self, rows1, rows2):
        name = self.LinkTable.item(self.row, 0).text()
        for row in rows1:
            newLinks = self.PointTable.item(row, 1).text().split(',')+[name]
            newLinks = noNoneString(newLinks)
            self.PointTable.editArgs(row,
                ','.join(newLinks),
                self.PointTable.item(row, 2).text(),
                self.PointTable.item(row, 3).text(),
                self.PointTable.item(row, 4).text(),
                self.PointTable.item(row, 5).text())
        for row in rows2:
            newLinks = self.PointTable.item(row, 1).text().split(',')
            newLinks.remove(name)
            newLinks = noNoneString(newLinks)
            self.PointTable.editArgs(row,
                ','.join(newLinks),
                self.PointTable.item(row, 2).text(),
                self.PointTable.item(row, 3).text(),
                self.PointTable.item(row, 4).text(),
                self.PointTable.item(row, 5).text())

class setPathCommand(QUndoCommand):
    def __init__(self, data, path):
        QUndoCommand.__init__(self)
        self.data = data
        self.path = deepcopy(path)
        self.oldPath = deepcopy(data)
    
    def redo(self):
        self.data.clear()
        self.data += self.path
    
    def undo(self):
        self.data.clear()
        self.data += self.oldPath

class clearPathCommand(QUndoCommand):
    def __init__(self, data):
        QUndoCommand.__init__(self)
        self.data = data
        self.oldPath = deepcopy(data)
    
    def redo(self):
        self.data.clear()
    
    def undo(self):
        self.data += self.oldPath

class demoValueCommand(QUndoCommand):
    def __init__(self, table, index, value, column):
        QUndoCommand.__init__(self)
        self.table = table
        self.index = index
        self.value = value
        self.column = column
        self.oldValue = float(table.item(index, self.column).text())
    
    def redo(self):
        self.table.setItem(self.index, self.column, QTableWidgetItem(str(self.value)))
    
    def undo(self):
        self.table.setItem(self.index, self.column, QTableWidgetItem(str(self.oldValue)))

def writeTS(table, row, Direction):
    table.setItem(row, 0, QTableWidgetItem(Direction.Type))
    for i in [2, 3]:
        e = [Direction.p1, Direction.p2][i-2]
        Item = QTableWidgetItem('Result{}'.format(e+1) if type(e)==int else "({:.02f}, {:.02f})".format(e[0], e[1]) if type(e)==tuple else e)
        if type(e)==tuple:
            Item.setToolTip("x = {}\ny = {}".format(e[0], e[1]))
        table.setItem(row, i, Item)
    condition = [
        "{}: {}".format(k, (v if k!='merge' else ["Points only", "Slider"][v] if Direction.Type=='PLPP' else
        ["Points only", "Linking L0", "Linking R0", "Fixed Chain", "Linking L0 & R0"][v])) for k, v in Direction.items().items()]
    conditionItem = QTableWidgetItem(', '.join(condition))
    conditionItem.setToolTip('\n'.join(condition))
    table.setItem(row, 4, conditionItem)

class TSinitCommand(QUndoCommand):
    def __init__(self, TSDirections, Directions):
        QUndoCommand.__init__(self)
        self.TSDirections = TSDirections
        self.Directions = copy(Directions)
        self.oldDirections = copy(TSDirections)
    
    def redo(self):
        self.TSDirections.clear()
        self.TSDirections += self.Directions
    
    def undo(self):
        self.TSDirections.clear()
        self.TSDirections += self.oldDirections

class TSeditCommand(QUndoCommand):
    def __init__(self, TSDirections, table, Direction, edit):
        QUndoCommand.__init__(self)
        self.TSDirections = TSDirections
        self.table = table
        self.Direction = copy(Direction)
        self.edit = edit
        if not self.edit is False:
            self.oldDirection = copy(TSDirections[edit])
    
    def redo(self):
        if self.edit is False:
            self.TSDirections.append(self.Direction)
            try:
                row = self.table.rowCount()
                self.table.insertRow(row)
            except:
                pass
        else:
            self.TSDirections[self.edit] = self.Direction
            row = self.edit
        try:
            writeTS(self.table, row, self.Direction)
        except:
            pass
    
    def undo(self):
        if self.edit is False:
            self.TSDirections.pop()
            try:
                self.table.removeRow(self.table.rowCount()-1)
            except:
                pass
        else:
            self.TSDirections[self.edit] = self.oldDirection
            try:
                writeTS(self.table, self.edit, self.Direction)
            except:
                pass

class TSdeleteCommand(QUndoCommand):
    def __init__(self, TSDirections, table):
        QUndoCommand.__init__(self)
        self.TSDirections = TSDirections
        self.oldDirection = copy(TSDirections[-1])
        self.table = table
    
    def redo(self):
        self.TSDirections.pop()
        try:
            self.table.removeRow(self.table.rowCount()-1)
        except:
            pass
    
    def undo(self):
        row = self.table.rowCount()
        self.TSDirections.append(self.oldDirection)
        self.table.insertRow(row)
        try:
            writeTS(self.table, row, self.oldDirection)
        except:
            pass
