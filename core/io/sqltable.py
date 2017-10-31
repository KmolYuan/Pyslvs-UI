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
from .Ui_sqltable import Ui_Form
from sys import getsizeof
import zlib
compress = lambda obj: zlib.compress(bytes(repr(obj), encoding="utf8"), 5)
decompress = lambda obj: eval(zlib.decompress(obj).decode())
import datetime
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    TextField,
    ForeignKeyField,
    DateTimeField
)

db = SqliteDatabase(None)

class Designs:
    __slots__ = ('path', 'result')
    
    def __init__(self):
        self.path = []
        self.result = []

#Show who commited the workbook.
class User(Model):
    username = CharField(max_length=255, unique=True)
    class Meta:
        database = db

#Commit data: Mechanism and Workbook information.
class CommitModel(Model):
    #Previous and branch commit
    previous = ForeignKeyField('self', related_name='next', null=True)
    pre_branch = ForeignKeyField('self', related_name='next_branch', null=True)
    #Commit time
    date = DateTimeField(default=datetime.datetime.now)
    #Workbook information
    author = ForeignKeyField(User)
    description = TextField()
    #Use Lark parser
    mechanism = TextField()
    #Path data
    pathdata = CharField()
    #Algorithm data
    algorithmdata = CharField()
    class Meta:
        database = db

#The table that stored workbook data, including IO functions.
class FileWidget(QWidget, Ui_Form):
    def __init__(self, pointDataFunc, parent):
        super(FileWidget, self).__init__(parent)
        self.setupUi(self)
        #UI part
        self.CommitTable.setColumnWidth(0, 30)
        self.CommitTable.setColumnWidth(1, 70)
        self.CommitTable.setColumnWidth(2, 130)
        self.CommitTable.setColumnWidth(3, 70)
        self.CommitTable.setColumnWidth(4, 70)
        self.CommitTable.setColumnWidth(5, 70)
        #The function used to get the data.
        self.pointDataFunc = pointDataFunc
        #Undo Stack
        self.FileState = parent.FileState
        #Reset
        self.resetAllList()
    
    def resetAllList(self):
        self.pathData = []
        self.Designs = Designs()
        self.Script = ""
        self.fileName = QFileInfo("[New Workbook]")
        self.description = ""
        self.author = "Anonymous"
        self.lastTime = datetime.datetime.now()
        self.changed = False
        self.Stack = 0
        self.FileState.clear()
    
    def updateAuthorDescription(self, author, description):
        self.author = author
        self.description = description
    
    def save(self, fileName):
        self.fileName = QFileInfo(fileName)
        for result in self.Designs.result:
            print(getsizeof(result))
        for path in self.pathData:
            print(getsizeof(path))
        '''
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel], safe=True)
        with db.atomic():
            pointData = self.pointDataFunc()
            commit = CommitModel(
                previous=None,
                pre_branch=None,
                author=None,
                description=None,
                mechanism="M[{}]".format(", ".join(str(vpoint) for vpoint in pointData)),
                pathdata=None,
            )
            try:
                commit.save()
            except:
                db.rollback()
        db.close()
        '''
    
    def read(self, fileName):
        self.fileName = QFileInfo(fileName)
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel], safe=True)
        '''Read the table rows.'''
        db.close()
        return
