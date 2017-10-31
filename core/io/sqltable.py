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
import zlib
compress = lambda obj: zlib.compress(bytes(repr(obj), encoding="utf8"), 5)
decompress = lambda obj: eval(zlib.decompress(obj).decode())
import datetime
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    BlobField,
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
class UserModel(Model):
    name = CharField(unique=True)
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
    author = ForeignKeyField(UserModel, null=True)
    description = CharField()
    #Use Lark parser
    mechanism = BlobField()
    #Path data
    pathdata = BlobField()
    #Algorithm data
    algorithmdata = BlobField()
    class Meta:
        database = db

#The table that stored workbook data, including IO functions.
class FileWidget(QWidget, Ui_Form):
    def __init__(self, pointDataFunc, isSavedFunc, parent):
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
        self.isSavedFunc = isSavedFunc
        #Undo Stack
        self.FileState = parent.FileState
        #Reset
        self.resetAllList()
    
    def resetAllList(self):
        self.history_commit = []
        self.pathData = []
        self.Designs = Designs()
        self.Script = ""
        self.fileName = QFileInfo("[New Workbook]")
        self.description = ""
        self.lastTime = datetime.datetime.now()
        self.changed = False
        self.Stack = 0
        self.FileState.clear()
    
    def save(self, fileName, branch=False):
        self.fileName = QFileInfo(fileName)
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, UserModel], safe=True)
        authors = tuple(user.name for user in UserModel.select())
        with db.atomic():
            author = self.FileAuthor.text() if self.FileAuthor.text() else "Anonymous"
            if author in authors:
                author_model = UserModel.select().where(UserModel.name==author).get()
            else:
                author_model = UserModel(name=author)
            pointData = self.pointDataFunc()
            args = {
                'author':author_model,
                'description':self.FileDescription.text(),
                'mechanism':compress("M[{}]".format(", ".join(str(vpoint) for vpoint in pointData))),
                'pathdata':compress(self.pathData),
                'algorithmdata':compress(self.Designs.result)
            }
            if not branch:
                #Last commit
                try:
                    args['previous'] = CommitModel.select().order_by(CommitModel.id).get()
                except CommitModel.DoesNotExist:
                    args['previous'] = None
            else:
                #Branch from
                try:
                    args['pre_branch'] = CommitModel.select().where(CommitModel.id==self.CommitTable.currentRow()+1).get()
                except CommitModel.DoesNotExist:
                    args['pre_branch'] = None
            commit = CommitModel(**args)
            try:
                print("Saving successful.")
                author_model.save()
                commit.save()
                self.isSavedFunc()
            except Exception as e:
                print(str(e))
                db.rollback()
        db.close()
    
    def read(self, fileName):
        self.resetAllList()
        self.fileName = QFileInfo(fileName)
        self.AuthorList.clear()
        for row in range(self.CommitTable.rowCount()):
            self.CommitTable.removeRow(row)
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, UserModel], safe=True)
        #Read the table rows.
        self.history_commit = CommitModel.select().order_by(CommitModel.id)
        for commit in self.history_commit:
            author = commit.author.name
            #AuthorList
            if author not in (self.AuthorList.item(row).text() for row in range(self.AuthorList.count())):
                self.AuthorList.addItem(author)
            #CommitTable
            row = self.CommitTable.rowCount()
            self.CommitTable.insertRow(row)
            self.CommitTable.setItem(row, 0, QTableWidgetItem(str(commit.id)))
            self.CommitTable.setItem(row, 1, QTableWidgetItem(
                "{t.year:02d}-{t.month:02d}-{t.day:02d} {t.hour:02d}:{t.minute:02d}:{t.second:02d}".format(t=commit.date)
            ))
            self.CommitTable.setItem(row, 2, QTableWidgetItem(commit.description))
            self.CommitTable.setItem(row, 3, QTableWidgetItem(commit.author.name))
            if commit.previous:
                self.CommitTable.setItem(row, 4, QTableWidgetItem(commit.previous.id))
            else:
                self.CommitTable.setItem(row, 4, QTableWidgetItem("None"))
            if commit.pre_branch:
                self.CommitTable.setItem(row, 5, QTableWidgetItem(commit.pre_branch.id))
            else:
                self.CommitTable.setItem(row, 5, QTableWidgetItem("None"))
            #Other data
            self.pathData = decompress(commit.pathdata)
            self.Designs.result = decompress(commit.algorithmdata)
        db.close()
        self.isSavedFunc()
    
    def getCommitState(self, id):
        try:
            commit = self.history_commit.where(CommitModel.id==id).get()
            #TODO: Load the commit.
        except CommitModel.DoesNotExist:
            return None
    
    @pyqtSlot(int)
    def on_AuthorList_currentRowChanged(self, row):
        if row>-1:
            self.FileAuthor.setText(self.AuthorList.item(row).text())
