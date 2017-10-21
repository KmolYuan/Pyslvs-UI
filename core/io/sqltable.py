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
import datetime
from peewee import (
    SqliteDatabase,
    Model,
    TextField,
    DateTimeField,
    ForeignKeyField
)

class Designs:
    __slots__ = ('path', 'result', 'TSDirections')
    
    def __init__(self):
        self.path = []
        self.result = []
        self.TSDirections = []
    
    def setPath(self, path):
        self.path = path
    
    def addResult(self, result):
        self.result = result
    
    def add(self, x, y):
        self.path.append((x, y))
    
    def remove(self, pos):
        del self.path[pos]
    
    def removeResult(self, pos):
        del self.result[pos]
    
    def moveUP(self, row):
        if row>0 and len(self.path)>1:
            self.path.insert(row-1, (self.path[row]['x'], self.path[row]['y']))
            del self.path[row+1]
    
    def moveDown(self, row):
        if row<len(self.path)-1 and len(self.path)>1:
            self.path.insert(row+2, (self.path[row]['x'], self.path[row]['y']))
            del self.path[row]

def db_class(class_name, db):
    class wrapper_class(class_name):
        class Meta:
            database = db
    return wrapper_class

#Commit information
class CommitBase(Model):
    #Hash ID
    id = TextField(unique=True)
    #Commit date
    date = DateTimeField()
    #Use Lark parser
    mechanism = TextField()

#Workbook information
class WorkbookBase(Model):
    author = TextField()
    description = TextField()
    pathdata = TextField()
    commit = ForeignKeyField(CommitBase, related_name='workbook')

#Algorithm results. This section does not support version management.
class AlgorithmBase(Model):
    pass

#The table that stored workbook data, including IO functions.
class FileTable(QTableWidget):
    def __init__(self, parent):
        super(FileTable, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #Undo Stack
        self.FileState = parent.FileState
        #Reset
        self.resetAllList()
    
    def resetAllList(self):
        self.pathData = []
        self.Designs = Designs()
        self.Script = ""
        self.fileName = QFileInfo('[New Workbook]')
        self.description = ""
        self.author = 'Anonymous'
        self.lastTime = datetime.datetime.now()
        self.changed = False
        self.Stack = 0
        self.FileState.clear()
    
    def updateAuthorDescription(self, author, description):
        self.author = author
        self.description = description
    
    def save(self, fileName):
        db = SqliteDatabase(fileName)
        db.connect()
        Workbook = db_class(WorkbookBase, db)
        db.create_tables([Workbook], safe=True)
        with db.atomic():
            try:
                db.save()
            except:
                db.rollback()
        db.close()
    
    def read(self, fileName):
        db = SqliteDatabase(fileName)
        db.connect()
        Workbook = db_class(WorkbookBase, db)
        db.create_tables([Workbook], safe=True)
        db.close()
        return
