# -*- coding: utf-8 -*-
from .modules import *
from ..calculation.color import colorlist, colorName
from copy import copy

def writeTable(table, rowPosition, name, Args):
    name_set = QTableWidgetItem("{}{}".format(name, rowPosition))
    name_set.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    for i in range(len(Args)):
        if type(Args[i])==str: table.setItem(rowPosition, i+1, QTableWidgetItem(Args[i]))
        elif type(Args[i])==bool:
            checkbox = QTableWidgetItem('')
            checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Checked if Args[i] else Qt.Unchecked)
            table.setItem(rowPosition, i+1, checkbox)

def writeStyle(table, rowPosition, color, ringsize, ringcolor, color_combobox):
    name_set = QTableWidgetItem('Point{}'.format(rowPosition))
    name_set.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 0, name_set)
    re_Color = colorName()
    for i in range(len(re_Color)): color_combobox.insertItem(i, re_Color[i])
    color_combobox.setCurrentIndex(color_combobox.findText(color))
    table.setCellWidget(rowPosition, 1, color_combobox)
    table.setItem(rowPosition, 1, QTableWidgetItem('Green'))
    ring_size = QTableWidgetItem(ringsize)
    ring_size.setFlags(Qt.ItemIsEnabled)
    table.setItem(rowPosition, 2, ring_size)
    color_combobox.setCurrentIndex(color_combobox.findText(ringcolor))
    table.setCellWidget(rowPosition, 3, color_combobox)

class editTableCommand(QUndoCommand):
    def __init__(self, table, name, edit, Args):
        QUndoCommand.__init__(self)
        self.table = table #Pointer - QTableWidget
        self.name = name
        self.edit = edit
        self.Args = Args
        if self.edit:
            self.oldArgs = list()
            for column in range(1, table.columnCount()):
                item = table.item(edit, column)
                self.oldArgs.append(item.text() if item.text()!='' else item.checkState()!=Qt.Unchecked)
    
    def redo(self):
        rowPosition = self.edit if self.edit else self.table.rowCount()
        if self.edit is False: self.table.insertRow(rowPosition)
        name_set = QTableWidgetItem("{}{}".format(self.name, rowPosition))
        name_set.setFlags(Qt.ItemIsEnabled)
        self.table.setItem(rowPosition, 0, name_set)
        for i in range(len(self.Args)):
            if type(self.Args[i])==str: self.table.setItem(rowPosition, i+1, QTableWidgetItem(self.Args[i]))
            elif type(self.Args[i])==bool:
                checkbox = QTableWidgetItem('')
                checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                checkbox.setCheckState(Qt.Checked if self.Args[i] else Qt.Unchecked)
                self.table.setItem(rowPosition, i+1, checkbox)
    def undo(self):
        if self.edit is False: self.table.removeRow(self.table.rowCount()-1)
        else:
            rowPosition = self.edit if self.edit else self.table.rowCount()
            writeTable(self.table, rowPosition, self.name, self.oldArgs)

class addStyleCommand(QUndoCommand):
    def __init__(self, styleTable, color, ringsize, ringcolor):
        QUndoCommand.__init__(self)
        self.table = styleTable
        self.color = color
        self.ringsize = ringsize
        self.ringcolor = ringcolor
    
    def redo(self):
        color_combobox = QComboBox(self.table)
        rowPosition = self.table.rowCount()
        self.table.insertRow(rowPosition)
        writeStyle(self.table, rowPosition, self.color, self.ringsize, self.ringcolor, color_combobox)
    def undo(self): self.table.removeRow(self.table.rowCount()-1)

class deleteTableCommand(QUndoCommand):
    def __init__(self, table, name, index):
        QUndoCommand.__init__(self)
        self.table = table
        self.name = name
        self.index = index
        self.oldArgs = list()
        for column in range(1, table.columnCount()):
            item = table.item(index, column)
            self.oldArgs += [item.text() if item.text()!='' else item.checkState()!=Qt.Unchecked]
    
    def redo(self):
        self.table.removeRow(self.index)
        for j in range(self.index, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem(self.name+str(j)))
    def undo(self):
        rowPosition = self.index
        self.table.insertRow(rowPosition)
        writeTable(self.table, rowPosition, self.name, self.oldArgs)
        for j in range(self.index, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem(self.name+str(j)))

class deleteStyleCommand(QUndoCommand):
    def __init__(self, table, row):
        QUndoCommand.__init__(self)
        self.table = table
        self.row = row
        self.oldColor = table.item(row, 1).text()
        self.oldSize = table.item(row, 2).text()
        self.oldRingColor = table.cellWidget(row, 3).currentText()
    
    def redo(self):
        self.table.removeRow(self.row)
        for j in range(self.row, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem('Point'+str(j)))
    def undo(self):
        color_combobox = QComboBox(self.table)
        rowPosition = self.row
        self.table.insertRow(rowPosition)
        writeStyle(self.table, rowPosition, self.oldColor, self.oldSize, self.oldRingColor, color_combobox)
        for j in range(self.row, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem('Point'+str(j)))

class changePointNumCommand(QUndoCommand):
    def __init__(self, table, pos, row, column):
        QUndoCommand.__init__(self)
        self.table = table
        self.pos = pos
        self.row = row
        self.column = column
        self.oldPos = int(table.item(row, column).text().replace('Point', ''))
    
    def redo(self):
        cell = QTableWidgetItem("Point{}".format(self.pos))
        self.table.setItem(self.row, self.column, cell)
    def undo(self):
        cell = QTableWidgetItem("Point{}".format(self.oldPos))
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
