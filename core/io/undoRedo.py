# -*- coding: utf-8 -*-
from ..QtModules import *
from ..calculation.color import colorlist, colorName
from copy import copy

def writeTable(table, rowPosition, name, Args):
    name_set = QTableWidgetItem("{}{}".format(name, rowPosition))
    name_set.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    for i in range(len(Args)):
        if type(Args[i]) in [str, float, int]:
            content = 'Point{}'.format(Args[i]) if type(Args[i])==int else Args[i]
            try: table.setItem(rowPosition, i+1, QTableWidgetItem(str(float(content))))
            except: table.setItem(rowPosition, i+1, QTableWidgetItem(content))
        elif type(Args[i])==bool:
            checkbox = QTableWidgetItem(str())
            checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Checked if Args[i] else Qt.Unchecked)
            table.setItem(rowPosition, i+1, checkbox)

def writeStyle(table, rowPosition, color, ringsize, ringcolor, color_combobox1, color_combobox2):
    name_set = QTableWidgetItem('Point{}'.format(rowPosition))
    name_set.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    re_Color = colorName()
    for i in range(len(re_Color)):
        color_combobox1.insertItem(i, re_Color[i])
        color_combobox2.insertItem(i, re_Color[i])
    color_combobox1.setCurrentIndex(color_combobox1.findText(color))
    color_combobox2.setCurrentIndex(color_combobox2.findText(ringcolor))
    table.setCellWidget(rowPosition, 1, color_combobox1)
    table.setItem(rowPosition, 2, QTableWidgetItem(str(ringsize)))
    table.setCellWidget(rowPosition, 3, color_combobox2)

def writeTS(table, row, Direction):
    table.setItem(row, 0, QTableWidgetItem(Direction.Type))
    for i in [2, 3]:
        e = [Direction.p1, Direction.p2][i-2]
        Item = QTableWidgetItem('Result{}'.format(e) if type(e)==int else "({:.02f}, {:.02f})".format(e[0], e[1]) if type(e)==tuple else e)
        if type(e)==tuple: Item.setToolTip("x = {}\ny = {}".format(e[0], e[1]))
        table.setItem(row, i, Item)
    condition = [
        "{}: {}".format(k, (v if k!='merge' else ["Points only", "Slider"][v] if Direction.Type=='PLPP' else
        ["Points only", "Linking L0", "Linking R0", "Stay Chain", "Linking L0 & R0"][v])) for k, v in Direction.items().items()]
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
        if not isEdit: self.table.insertRow(rowPosition)
        writeTable(self.table, rowPosition, self.name, self.Args)
    def undo(self):
        isEdit = not self.edit is False
        if not isEdit: self.table.removeRow(self.table.rowCount()-1)
        else: writeTable(self.table, self.edit, self.name, self.oldArgs)

class addStyleCommand(QUndoCommand):
    def __init__(self, styleTable, color, ringsize, ringcolor):
        QUndoCommand.__init__(self)
        self.table = styleTable
        self.color = color
        self.ringsize = ringsize
        self.ringcolor = ringcolor
    
    def redo(self):
        color_combobox1 = QComboBox(self.table)
        color_combobox2 = QComboBox(self.table)
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        writeStyle(self.table, rowPosition, self.color, self.ringsize, self.ringcolor, color_combobox1, color_combobox2)
    def undo(self): self.table.removeRow(self.table.rowCount()-1)

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
            for j in range(self.index, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem(self.name+str(j)))
    def undo(self):
        self.table.insertRow(self.index)
        writeTable(self.table, self.index, self.name, self.oldArgs)
        if self.isRename:
            for j in range(self.index, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem(self.name+str(j)))

class deleteStyleCommand(QUndoCommand):
    def __init__(self, table, row):
        QUndoCommand.__init__(self)
        self.table = table
        self.row = row
        self.oldColor = table.cellWidget(row, 1).currentText()
        self.oldSize = table.item(row, 2).text()
        self.oldRingColor = table.cellWidget(row, 3).currentText()
    
    def redo(self):
        self.table.removeRow(self.row)
        for j in range(self.row, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem('Point'+str(j)))
    def undo(self):
        color_combobox1 = QComboBox(self.table)
        color_combobox2 = QComboBox(self.table)
        rowPosition = self.row
        self.table.insertRow(rowPosition)
        writeStyle(self.table, rowPosition, self.oldColor, self.oldSize, self.oldRingColor, color_combobox1, color_combobox2)
        for j in range(self.row, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem('Point'+str(j)))

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
    def __init__(self, data, runTable, shaftTable, path, runList, shaftList):
        QUndoCommand.__init__(self)
        self.data = data
        self.runTable = runTable
        self.shaftTable = shaftTable
        self.path = copy(path)
        self.runList = copy(runList)
        self.shaftList = copy(shaftList)
        self.oldPath = copy(data)
        self.oldRunList = copy(runTable)
        self.oldShaftList = copy(shaftTable)
    
    def redo(self):
        self.data.clear()
        self.runTable.clear()
        self.shaftTable.clear()
        self.data += self.path
        self.runTable += self.runList
        self.shaftTable += self.shaftList
    def undo(self):
        self.data.clear()
        self.runTable.clear()
        self.shaftTable.clear()
        self.data += self.oldPath
        self.runTable += self.oldRunList
        self.shaftTable += self.oldShaftList

class clearPathCommand(QUndoCommand):
    def __init__(self, data, runTable, shaftTable):
        QUndoCommand.__init__(self)
        self.data = data
        self.runTable = runTable
        self.shaftTable = shaftTable
        self.oldPath = copy(data)
        self.oldRunList = copy(runTable)
        self.oldShaftList = copy(shaftTable)
    
    def redo(self):
        self.data.clear()
        self.runTable.clear()
        self.shaftTable.clear()
    def undo(self):
        self.data += self.oldPath
        self.runTable += self.oldRunList
        self.shaftTable += self.oldShaftList

class shaftChangeCommand(QUndoCommand):
    def __init__(self, shaftList, table, prv, next):
        QUndoCommand.__init__(self)
        self.shaftList = shaftList
        self.table = table
        self.prv = prv
        self.next = next
    
    def redo(self):
        try: self.shaftList[self.prv], self.shaftList[self.next] = self.shaftList[self.next], self.shaftList[self.prv]
        except: pass
        tableRow = list()
        for i in range(self.table.columnCount()): tableRow.append(self.table.takeItem(self.prv, i))
        self.table.removeRow(self.prv)
        self.table.insertRow(self.next)
        for j in range(len(tableRow)): self.table.setItem(self.next, j, tableRow[j])
        for k in range(self.next, self.table.rowCount()): self.table.setItem(k, 0, QTableWidgetItem('Shaft'+str(k)))
    def undo(self):
        try: self.shaftList[self.prv], self.shaftList[self.next] = self.shaftList[self.next], self.shaftList[self.prv]
        except: pass
        tableRow = list()
        for i in range(self.table.columnCount()): tableRow.append(self.table.takeItem(self.prv, i))
        self.table.removeRow(self.prv)
        self.table.insertRow(self.next)
        for j in range(len(tableRow)): self.table.setItem(self.next, j, tableRow[j])
        for k in range(self.next, self.table.rowCount()): self.table.setItem(k, 0, QTableWidgetItem('Shaft'+str(k)))

class demoValueCommand(QUndoCommand):
    def __init__(self, table, index, value, column):
        QUndoCommand.__init__(self)
        self.table = table
        self.index = index
        self.value = value
        self.column = column
        self.oldValue = float(table.item(index, self.column).text())
    
    def redo(self): self.table.setItem(self.index, self.column, QTableWidgetItem(str(self.value)))
    def undo(self): self.table.setItem(self.index, self.column, QTableWidgetItem(str(self.oldValue)))

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
        if not self.edit is False: self.oldDirection = copy(TSDirections[edit])
    
    def redo(self):
        if self.edit is False:
            self.TSDirections.append(self.Direction)
            try:
                row = self.table.rowCount()
                self.table.insertRow(row)
            except: pass
        else:
            self.TSDirections[self.edit] = self.Direction
            row = self.edit
        try: writeTS(self.table, row, self.Direction)
        except: pass
    def undo(self):
        if self.edit is False:
            self.TSDirections.pop()
            try: self.table.removeRow(self.table.rowCount()-1)
            except: pass
        else:
            self.TSDirections[self.edit] = self.oldDirection
            try: writeTS(self.table, self.edit, self.Direction)
            except: pass

class TSdeleteCommand(QUndoCommand):
    def __init__(self, TSDirections, table):
        QUndoCommand.__init__(self)
        self.TSDirections = TSDirections
        self.oldDirection = copy(TSDirections[-1])
        self.table = table
    
    def redo(self):
        self.TSDirections.pop()
        try: self.table.removeRow(self.table.rowCount()-1)
        except: pass
    def undo(self):
        row = self.table.rowCount()
        self.TSDirections.append(self.oldDirection)
        self.table.insertRow(row)
        try: writeTS(self.table, row, self.oldDirection)
        except: pass
