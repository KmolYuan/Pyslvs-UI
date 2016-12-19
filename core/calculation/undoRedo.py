# -*- coding: utf-8 -*-
from .__init__ import *

class addTableUndo(QUndoCommand):
    def __init__(self, table, contentTable, list, contentList):
        QUndoCommand.__init__(self)
        self.table = table
        self.contentTable = copy(contentTable)
        self.list = list
        self.contentList = copy(contentList)
    
    def undo(self):
        ''''''
    
    def redo(self):
        ''''''
