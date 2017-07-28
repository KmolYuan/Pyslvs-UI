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
from copy import copy, deepcopy

def writeTable(table, rowPosition, name, Args):
    name_set = QTableWidgetItem("{}{}".format(name, rowPosition))
    name_set.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    for i, e in enumerate(Args):
        if type(e) in [str, float, int]:
            content = 'Point{}'.format(e) if type(e)==int else e
            try:
                table.setItem(rowPosition, i+1, QTableWidgetItem(str(round(float(content), 4))))
            except:
                try:
                    table.setItem(rowPosition, i+1, QTableWidgetItem(colorIcons()[content], content))
                except KeyError:
                    table.setItem(rowPosition, i+1, QTableWidgetItem(content))
        elif type(e)==bool:
            checkbox = QTableWidgetItem(str())
            checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Checked if e else Qt.Unchecked)
            table.setItem(rowPosition, i+1, checkbox)

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

class editTableCommand(QUndoCommand):
    def __init__(self, table, name, edit, Args):
        QUndoCommand.__init__(self)
        self.table = table #Pointer - QTableWidget
        self.name = name
        self.edit = edit
        self.Args = Args
        if not edit is False:
            self.oldArgs = list()
            for column in range(1, table.columnCount()):
                item = table.item(edit, column)
                self.oldArgs.append(item.text() if item.text()!='' else item.checkState()!=Qt.Unchecked)
    
    def redo(self):
        isEdit = not self.edit is False
        rowPosition = self.edit if isEdit else self.table.rowCount()
        if not isEdit:
            self.table.insertRow(rowPosition)
        writeTable(self.table, rowPosition, self.name, self.Args)
    def undo(self):
        isEdit = not self.edit is False
        if not isEdit:
            self.table.removeRow(self.table.rowCount()-1)
        else:
            writeTable(self.table, self.edit, self.name, self.oldArgs)

class deleteTableCommand(QUndoCommand):
    def __init__(self, table, name, index, isRename=True):
        QUndoCommand.__init__(self)
        self.table = table
        self.name = name
        self.index = index
        self.isRename = isRename
        self.oldArgs = list()
        for column in range(1, table.columnCount()):
            item = table.item(index, column)
            self.oldArgs += [item.text() if item.text()!=str() else item.checkState()!=Qt.Unchecked]
    
    def redo(self):
        self.table.removeRow(self.index)
        if self.isRename:
            for j in range(self.index, self.table.rowCount()):
                self.table.setItem(j, 0, QTableWidgetItem(self.name+str(j)))
    def undo(self):
        self.table.insertRow(self.index)
        writeTable(self.table, self.index, self.name, self.oldArgs)
        if self.isRename:
            for j in range(self.index, self.table.rowCount()):
                self.table.setItem(j, 0, QTableWidgetItem(self.name+str(j)))

class changePointNumCommand(QUndoCommand):
    def __init__(self, table, pos, row, column, name='Point'):
        QUndoCommand.__init__(self)
        self.table = table
        self.pos = pos
        self.row = row
        self.column = column
        self.name = name
        self.oldPos = int(table.item(row, column).text().replace(name, str()))
    
    def redo(self):
        cell = QTableWidgetItem(self.name+str(self.pos) if not self.name=='n' else str(self.pos))
        self.table.setItem(self.row, self.column, cell)
    def undo(self):
        cell = QTableWidgetItem(self.name+str(self.oldPos))
        self.table.setItem(self.row, self.column, cell)

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
