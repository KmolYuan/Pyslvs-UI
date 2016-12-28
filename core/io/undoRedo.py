# -*- coding: utf-8 -*-
'''
QUndoCommand Form:
* Add / Delete
    [table, table_content], [file, file_content], row
* Edit
    [table, table_content1, table_content2], [file, file_content1, file_content2], row
* Move up / down
    table, file, [prev, next]
'''
from .modules import *
from copy import copy, deepcopy

class addPointUndo(QUndoCommand):
    def __init__(self, table, style, file, stylefile, row):
        QUndoCommand.__init__(self)
        self.table = table[0]
        self.style = style[0]
        self.file = file[0]
        self.stylefile = stylefile[0]
        self.table_content = deepcopy(table[1]) #List
        self.style_content = deepcopy(style[1]) #List
        self.file_content = deepcopy(file[1]) #Dict
        self.stylefile_content = deepcopy(stylefile[1]) #Dict
        self.row = copy(row)
    
    def undo(self):
        self.table.removeRow(self.row)
        self.style.removeRow(self.row)
        del self.file[self.row]
        del self.stylefile[self.row]
    
    def redo(self):
        for i in range(len(self.table_content)):
            name_set = QTableWidgetItem(self.table_content[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(self.row, i, name_set)
        for i in range(len(self.style_content)):
            name_set = QTableWidgetItem(self.style_content[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(self.row, i, name_set)
        self.file.append(self.file_content)
        self.style.append(self.style_content)

class addTableUndo(QUndoCommand):
    def __init__(self, table, file, row):
        QUndoCommand.__init__(self)
        self.table = table[0]
        self.file = file[0]
        self.table_content = deepcopy(table[1]) #List
        self.file_content = deepcopy(file[1]) #Dict
        self.row = copy(row)
    
    def undo(self):
        del self.file[self.row]
        self.table.removeRow(self.row)
    
    def redo(self):
        for i in range(len(self.table_content)):
            name_set = QTableWidgetItem(self.table_content[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(self.row, i, name_set)
        self.file.append(self.file_content)

class deleteTableUndo(QUndoCommand):
    def __init__(self, table, file, row):
        QUndoCommand.__init__(self)
        self.table = table[0]
        self.file = file[0]
        self.table_content = deepcopy(table[1]) #Dict
        self.file_content = deepcopy(file[1]) #Dict
        self.row = copy(row)
    
    def undo(self):
        for i in range(len(self.table_content)):
            name_set = QTableWidgetItem(self.table_content[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(self.row, i, name_set)
        self.file.append(self.file_content)
    
    def redo(self):
        del self.file[self.row]
        self.table.removeRow(self.row)

class editTableUndo(QUndoCommand):
    def __init__(self, table, file, row):
        QUndoCommand.__init__(self)
        self.table = table[0]
        self.file = file[0]
        self.table_content1 = deepcopy(table[1]) #List
        self.table_content2 = deepcopy(table[2]) #List
        self.file_content1 = deepcopy(file[1]) #Dict
        self.file_content2 = deepcopy(file[2]) #Dict
        self.row = copy(row)
    
    def undo(self):
        self.file[self.row] = self.file_content1
        for i in range(len(self.table_content1)):
            name_set = QTableWidgetItem(self.table_content1[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(self.row, i, name_set)
    
    def redo(self):
        self.file[self.row] = self.file_content2
        for i in range(len(self.table_content2)):
            name_set = QTableWidgetItem(self.table_content2[i])
            if i==0: name_set.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(self.row, i, name_set)

class moveTableUndo(QUndoCommand):
    def __init__(self):
        QUndoCommand.__init__(self, table, file, row)
        self.table = table
        self.file = file
        self.prev = copy(row[0])
        self.next = copy(row[1])
    
    def undo(self):
        ''''''
    
    def redo(self):
        ''''''
