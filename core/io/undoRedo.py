# -*- coding: utf-8 -*-
from .modules import *
from ..calculation.color import colorlist, colorName

class editTableCommand(QUndoCommand):
    def __init__(self, table, name, edit, *Args):
        QUndoCommand.__init__(self)
        self.table = table #pointer - QTable
        self.name = name
        self.edit = edit
        self.Args = Args
        if self.edit:
            self.oldArgs = list()
            for column in range(1, table.columnCount()):
                item = self.table.item(self.edit, column)
                self.oldArgs += [item.text() if item.text()!='' else item.checkState()!=Qt.Unchecked]
    
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
            name_set = QTableWidgetItem("{}{}".format(self.name, rowPosition))
            name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(rowPosition, 0, name_set)
            for i in range(len(self.oldArgs)):
                if type(self.oldArgs[i])==str: self.table.setItem(rowPosition, i+1, QTableWidgetItem(self.oldArgs[i]))
                elif type(self.oldArgs[i])==bool:
                    checkbox = QTableWidgetItem('')
                    checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    checkbox.setCheckState(Qt.Checked if self.oldArgs[i] else Qt.Unchecked)
                    self.table.setItem(rowPosition, i+1, checkbox)

class styleAddCommand(QUndoCommand):
    def __init__(self, **Style):
        QUndoCommand.__init__(self)
        self.Style = Style
    
    def redo(self):
        rowPosition = self.Style['styleTable'].rowCount()
        self.Style['styleTable'].insertRow(rowPosition)
        name_set = QTableWidgetItem("Point{}".format(rowPosition))
        name_set.setFlags(Qt.ItemIsEnabled)
        self.Style['styleTable'].setItem(rowPosition, 0, name_set)
        color_combobox = QComboBox(self.Style['styleTable'])
        re_Color = colorName()
        for i in range(len(re_Color)): color_combobox.insertItem(i, re_Color[i])
        color_combobox.setCurrentIndex(color_combobox.findText(self.Style['color']))
        self.Style['styleTable'].setCellWidget(rowPosition, 1, color_combobox)
        self.Style['styleTable'].setItem(rowPosition, 1, QTableWidgetItem("Green"))
        ring_size = QTableWidgetItem(self.Style['ringsize'])
        ring_size.setFlags(Qt.ItemIsEnabled)
        self.Style['styleTable'].setItem(rowPosition, 2, ring_size)
        color_combobox.setCurrentIndex(color_combobox.findText(self.Style['ringcolor']))
        self.Style['styleTable'].setCellWidget(rowPosition, 3, color_combobox)
    
    def undo(self):
        self.Style['styleTable'].removeRow(self.Style['styleTable'].rowCount()-1)

class deleteTableCommand(QUndoCommand):
    def __init__(self, table, name, index):
        QUndoCommand.__init__(self)
        self.table = table
        self.name = name
        self.index = index
        self.oldArgs = list()
        for column in range(1, table.columnCount()):
            item = self.table.item(self.index, column)
            self.oldArgs += [item.text() if item.text()!='' else item.checkState()!=Qt.Unchecked]
    
    def redo(self):
        self.table.removeRow(self.index)
        for j in range(self.index, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem(self.name+str(j)))
    
    def undo(self):
        rowPosition = self.index
        self.table.insertRow(rowPosition)
        name_set = QTableWidgetItem("{}{}".format(self.name, rowPosition))
        name_set.setFlags(Qt.ItemIsEnabled)
        self.table.setItem(rowPosition, 0, name_set)
        for i in range(len(self.oldArgs)):
            if type(self.oldArgs[i])==str: self.table.setItem(rowPosition, i+1, QTableWidgetItem(self.oldArgs[i]))
            elif type(self.oldArgs[i])==bool:
                checkbox = QTableWidgetItem('')
                checkbox.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                checkbox.setCheckState(Qt.Checked if self.oldArgs[i] else Qt.Unchecked)
                self.table.setItem(rowPosition, i+1, checkbox)
