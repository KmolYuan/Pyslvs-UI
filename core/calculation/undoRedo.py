# -*- coding: utf-8 -*-
from .modules import *
from copy import copy

class addTableUndo(QUndoCommand):
    def __init__(self, table, contentTable, list, contentList, row):
        QUndoCommand.__init__(self)
        self.table = table
        self.contentTable = copy(contentTable) #List
        self.list = list
        self.contentList = copy(contentList) #dict
        self.row = row
    
    def undo(self):
        self.list.pop(self.row)
        self.table.removeRow(self.row)
    
    def redo(self):
        self.list.append(self.contentList)
        for i in range(len(self.contentTable)):
            name_set = QTableWidgetItem(self.contentTable[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(rowPosition, i, name_set)

class deleteTableUndo(QUndoCommand):
    def __init__(self, table, contentTable, list, contentList, row):
        QUndoCommand.__init__(self)
        self.table = table
        self.contentTable = copy(contentTable) #List
        self.list = list
        self.contentList = copy(contentList) #dict
        self.row = row
    
    def undo(self):
        self.list.append(self.contentList)
        for i in range(len(self.contentTable)):
            name_set = QTableWidgetItem(self.contentTable[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(rowPosition, i, name_set)
    
    def redo(self):
        self.list.pop(self.row)
        self.table.removeRow(self.row)

class moveTableUndo(QUndoCommand):
    def __init__(self):
        QUndoCommand.__init__(self, table, list, preRow, nexRow)
        self.table = table
        self.list = list
        self.preRow = copy(preRow)
        self.nexRow = copy(nexRow)
    
    def undo(self):
        ''''''
    
    def redo(self):
        ''''''
