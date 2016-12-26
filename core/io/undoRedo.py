# -*- coding: utf-8 -*-
from .modules import *
from copy import deepcopy

class addTableUndo(QUndoCommand):
    def __init__(self, table, contentTable, list, contentList, row):
        QUndoCommand.__init__(self)
        self.table = table
        self.contentTable = deepcopy(contentTable) #List
        self.list = list
        self.contentList = deepcopy(contentList) #List
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
        self.contentTable = deepcopy(contentTable) #List
        self.list = list
        self.contentList = deepcopy(contentList) #List
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

class editTableUndo(QUndoCommand):
    def __init__(self, table, contentTable1, contentTable2, list, contentList1, contentList2, row):
        QUndoCommand.__init__(self)
        self.table = table
        self.contentTable1 = deepcopy(contentTable1) #List
        self.contentTable2 = deepcopy(contentTable2) #List
        self.list = list
        self.contentList1 = deepcopy(contentList1) #List
        self.contentList2 = deepcopy(contentList2) #List
        self.row = row
    
    def undo(self):
        self.list[self.row] = self.contentList
        self.table.removeRow(self.row)
    
    def redo(self):
        self.list.append(self.contentList)
        for i in range(len(self.contentTable)):
            name_set = QTableWidgetItem(self.contentTable[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(rowPosition, i, name_set)

class moveTableUndo(QUndoCommand):
    def __init__(self):
        QUndoCommand.__init__(self, table, list, row1, row2)
        self.table = table
        self.list = list
        self.row1 = deepcopy(row1)
        self.row2 = deepcopy(row2)
    
    def undo(self):
        ''''''
    
    def redo(self):
        ''''''
