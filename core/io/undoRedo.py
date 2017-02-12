# -*- coding: utf-8 -*-
from .modules import *
from copy import copy

#Add Point(Dedicated)
class addPointUndo(QUndoCommand):
    def __init__(self, table, styleTable, tableList, styleTableList, row):
        QUndoCommand.__init__(self)
        self.table = table #pointer - QTable
        self.styleTable = styleTable #pointer - QTable
        self.tableList = tableList #pointer - list
        self.styleTableList = styleTableList #pointer - list
        self.tableContent = table
        self.row = copy(row)
    
    def undo(self):
        ''''''
    
    def redo(self):
        ''''''
