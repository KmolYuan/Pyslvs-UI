# -*- coding: utf-8 -*-
from .modules import *
from copy import copy

#Add Point(Dedicated)
class addPointCommand(QUndoCommand):
    def __init__(self, table, name, edit, *Args, **Style):
        QUndoCommand.__init__(self)
        self.table = table #pointer - QTable
        self.name = name
        self.edit = edit
        self.styleTable = Style['styleTable'] #pointer - QTable
        self.styleColor = Style['color']
        self.styleRingsize = Style['ringsize']
        self.styleRingcolor = Style['ringcolor']
        self.setText("Add Point{}".format(rowPosition))
    
    def redo(self):
        ''''''
    
    def undo(self):
        ''''''
    
    def table(self): return self.table, self.name

class editTableCommand(QUndoCommand):
    def __init__(self, table, name, edit, *Args):
        QUndoCommand.__init__(self)
        self.table = table #pointer - QTable
        self.name = name
        self.edit = edit
        self.setText("Add Point{}".format(rowPosition))
    
    def redo(self):
        ''''''
    
    def undo(self):
        ''''''
    
    def table(self): return self.table, self.name

class deleteTableCommand(QUndoCommand):
    def __init__(self, table, name, index):
        QUndoCommand.__init__(self)
        self.table = table
        self.name = name
        self.index = index
        self.table
        self.setText("Delete {}{}".format(name, index))
    
    def redo(self):
        self.table.removeRow(index)
        for j in range(self.index, self.table.rowCount()): self.table.setItem(j, 0, QTableWidgetItem(self.name+str(j)))
    
    def undo(self):
        ''''''
    
    def table(self): return self.table, self.name
