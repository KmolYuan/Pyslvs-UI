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
    CharField,
    TextField,
    BooleanField,
    IntegerField,
    FloatField,
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
    #pathdata = "0.0,0.0;1.0,1.0;..."
    pathdata = TextField()
    class Meta:
        database = db

#Algorithm results. This section does NOT support version management.
class AlgorithmModel(Model):
    #Hardware information
    network = BooleanField()
    cpu = TextField()
    os = TextField()
    memory = TextField()
    '''
    Results
    
    Links = "8.5607,5.7183,..."(L0,L1,...)
    '''
    Algorithm = TextField()
    type = TextField() #8Bar / 4Bar
    time = FloatField()
    interrupted = BooleanField()
    Ax = FloatField()
    Ay = FloatField()
    Dx = FloatField()
    Dy = FloatField()
    Links = TextField()
    #TimeAndFitness = "generation,fitness,time;..."
    TimeAndFitness = TextField()
    '''
    generateData
    
    targetPath = "0.0,0.0;1.0,1.0;..."
    upper/lower = "50.0,50.0,..."
    '''
    targetPath = TextField()
    upper = TextField()
    lower = TextField()
    nParm = IntegerField()
    maxGen = IntegerField()
    report = IntegerField()
    #algorithmPrams = "CR:0.9,NP:400,..."
    algorithmPrams = TextField()
    class Meta:
        database = db

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
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, AlgorithmModel], safe=True)
        with db.atomic():
            try:
                '''Save the table rows.'''
            except:
                db.rollback()
        db.close()
    
    def read(self, fileName):
        self.fileName = QFileInfo(fileName)
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, AlgorithmModel], safe=True)
        '''Read the table rows.'''
        db.close()
        return
