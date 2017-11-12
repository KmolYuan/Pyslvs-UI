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
from .Ui_peeweeIO import Ui_Form
from .example import example_list
import zlib
compress = lambda obj: zlib.compress(bytes(repr(obj), encoding="utf8"), 5)
decompress = lambda obj: eval(zlib.decompress(obj).decode())
import os
import datetime
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    BlobField,
    ForeignKeyField,
    DateTimeField
)

#Create a empty Sqlite database object.
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

#The branch in this workbook.
class BranchModel(Model):
    name = CharField(unique=True)
    class Meta:
        database = db

#Commit data: Mechanism and Workbook information.
class CommitModel(Model):
    #Previous and branch commit
    previous = ForeignKeyField('self', related_name='next', null=True)
    branch = ForeignKeyField(BranchModel, null=True)
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

class LoadCommitButton(QPushButton):
    loaded = pyqtSignal(int)
    
    def __init__(self, id, parent=None):
        super(LoadCommitButton, self).__init__(QIcon(QPixmap(":icons/dataupdate.png")), " #{}".format(id), parent)
        self.setToolTip("Reset to commit #{}.".format(id))
        self.id = id
    
    def mouseReleaseEvent(self, event):
        super(LoadCommitButton, self).mouseReleaseEvent(event)
        self.loaded.emit(self.id)
    
    def isLoaded(self, id: int):
        self.setEnabled(id!=self.id)

#The table that stored workbook data, including IO functions.
class FileWidget(QWidget, Ui_Form):
    load_id = pyqtSignal(int)
    
    def __init__(self, parent):
        super(FileWidget, self).__init__(parent)
        self.setupUi(self)
        #UI part
        self.CommitTable.setColumnWidth(0, 70) #ID
        self.CommitTable.setColumnWidth(1, 70) #Date
        self.CommitTable.setColumnWidth(2, 130) #Description
        self.CommitTable.setColumnWidth(3, 70) #Author
        self.CommitTable.setColumnWidth(4, 70) #Previous
        self.CommitTable.setColumnWidth(5, 70) #Branch
        #The main window functions.
        self.pointDataFunc = parent.Entities_Point.data #Get current Point data.
        self.isSavedFunc = parent.workbookSaved #Call it to get main window be shown as saved.
        self.parseFunc = parent.parseExpression #Main window will load the entered expression.
        self.clearFunc = parent.clear #Reset the main window.
        self.loadPathFunc = parent.loadPaths #Call after loaded paths.
        '''self.loadAlgorithmFunc = parent.DimensionalSynthesis.loadResults''' #Call after loaded algorithm results.
        #Undo Stack
        self.FileState = parent.FileState
        #Reset
        self.reset()
    
    def reset(self):
        self.history_commit = None #peewee Quary type
        self.pathData = {}
        self.Designs = Designs()
        self.Script = ""
        self.fileName = QFileInfo("Untitled")
        self.lastTime = datetime.datetime.now()
        self.changed = False
        self.Stack = 0
        self.FileState.clear()
        for row in range(self.CommitTable.rowCount()):
            self.CommitTable.removeRow(0)
        self.BranchList.clear()
        self.AuthorList.clear()
        self.FileAuthor.clear()
        self.FileDescription.clear()
        self.branch_current.clear()
        self.commit_search_text.clear()
        self.commit_current_id.setValue(0)
    
    def save(self, fileName, isBranch=False):
        if fileName!=self.fileName and os.path.isfile(fileName):
            os.remove(fileName)
            print("The original file has been overwritten.")
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, UserModel, BranchModel], safe=True)
        authors = (user.name for user in UserModel.select())
        branches = (branch.name for branch in BranchModel.select())
        commit_text = self.FileDescription.text()
        branch_name = '' if isBranch else self.branch_current.text()
        while not branch_name:
            branch_name, ok = QInputDialog.getText(self, "Branch", "Please enter a branch name:", QLineEdit.Normal, "master")
            if not ok:
                return
        while not commit_text:
            commit_text, ok = QInputDialog.getText(self, "Commit", "Please add a comment:", QLineEdit.Normal, "Update mechanism.")
            if not ok:
                return
        with db.atomic():
            author_name = self.FileAuthor.text() if self.FileAuthor.text() else "Anonymous"
            if author_name in authors:
                author_model = UserModel.select().where(UserModel.name==author_name).get()
            else:
                author_model = UserModel(name=author_name)
            if branch_name in branches:
                branch_model = BranchModel.select().where(BranchModel.name==branch_name).get()
            else:
                branch_model = BranchModel(name=branch_name)
            pointData = self.pointDataFunc()
            args = {
                'author':author_model,
                'description':commit_text,
                'mechanism':compress("M[{}]".format(", ".join(str(vpoint) for vpoint in pointData))),
                'pathdata':compress(self.pathData),
                'algorithmdata':compress(self.Designs.result),
                'branch':branch_model
            }
            #Last commit
            try:
                args['previous'] = CommitModel.select().where(CommitModel.id==self.commit_current_id.value()).get()
            except CommitModel.DoesNotExist:
                args['previous'] = None
            commit = CommitModel(**args)
            try:
                author_model.save()
                branch_model.save()
                commit.save()
                self.addCommit(commit)
            except Exception as e:
                print(str(e))
                db.rollback()
            else:
                self.history_commit = CommitModel.select().order_by(CommitModel.id)
                self.loadCommit(self.history_commit.get())
                print("Saving {} successful.".format(fileName))
                self.isSavedFunc()
        self.fileName = QFileInfo(fileName)
        db.close()
    
    def read(self, fileName):
        self.reset()
        self.fileName = QFileInfo(fileName)
        for row in range(self.CommitTable.rowCount()):
            self.CommitTable.removeRow(0)
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, UserModel, BranchModel], safe=True)
        #Read and load the table rows to commit table widget.
        self.AuthorList.clear()
        self.history_commit = CommitModel.select().order_by(CommitModel.id)
        for commit in self.history_commit:
            self.addCommit(commit)
        db.close()
        #Load the last commit.
        print("Added {} commits.".format(len(self.history_commit)))
        try:
            self.loadCommit(self.history_commit.get())
        except CommitModel.DoesNotExist:
            QMessageBox.warning(self, "Warning", "This file is a non-committed database.")
            return
        self.isSavedFunc()
    
    def importMechanism(self, fileName):
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, UserModel, BranchModel], safe=True)
        commit_all = CommitModel.select().join(BranchModel)
        branch_all = BranchModel.select().order_by(BranchModel.name)
        db.close()
        branch_name, ok = QInputDialog.getItem(self, "Branch", "Select the latest commit in the branch to load.",
            [branch.name for branch in branch_all], 0, False)
        if ok:
            try:
                commit = commit_all.where(BranchModel.name==branch_name).order_by(CommitModel.date).get()
            except CommitModel.DoesNotExist:
                QMessageBox.warning(self, "Warning", "This file is a non-committed database.")
            else:
                self.importCommit(commit)
    
    def addCommit(self, commit):
        row = self.CommitTable.rowCount()
        self.CommitTable.insertRow(row)
        #Commit ID
        self.commit_current_id.setValue(commit.id)
        button = LoadCommitButton(commit.id, self)
        button.loaded.connect(self.loadCommitID)
        self.load_id.connect(button.isLoaded)
        self.CommitTable.setCellWidget(row, 0, button)
        #Date
        date = "{t.year:02d}-{t.month:02d}-{t.day:02d} {t.hour:02d}:{t.minute:02d}:{t.second:02d}".format(t=commit.date)
        #Description
        self.CommitTable.setItem(row, 2, QTableWidgetItem(commit.description))
        #Author
        author_name = commit.author.name
        if author_name not in (self.AuthorList.item(row).text() for row in range(self.AuthorList.count())):
            self.AuthorList.addItem(author_name)
        #Previous commit
        if commit.previous:
            previous_id = str(commit.previous.id)
        else:
            previous_id = "None"
        #Branch
        branch_name = commit.branch.name
        if branch_name not in (self.BranchList.item(row).text() for row in range(self.BranchList.count())):
            self.BranchList.addItem(branch_name)
        self.branch_current.setText(branch_name)
        #Add to table widget.
        for i, text in enumerate((date, commit.description, author_name, previous_id, branch_name)):
            item = QTableWidgetItem(text)
            item.setToolTip(text)
            self.CommitTable.setItem(row, i+1, item)
    
    #Check the id is correct.
    def loadCommitID(self, id: int):
        print("Load commit #{}".format(id))
        try:
            commit = self.history_commit.where(CommitModel.id==id).get()
        except CommitModel.DoesNotExist:
            QMessageBox.warning(self, "Warning", "Commit ID is not exist.")
        except AttributeError:
            QMessageBox.warning(self, "Warning", "Nothing submitted.")
        else:
            if self.changed:
                reply = QMessageBox.question(self, "Message", "Are you sure to load?\nAny changes won't be saved.",
                    (QMessageBox.Ok | QMessageBox.Cancel), QMessageBox.Ok)
                if reply==QMessageBox.Ok:
                    self.loadCommit(commit)
            else:
                self.loadCommit(commit)
    
    #Load the commit pointer.
    def loadCommit(self, commit: CommitModel):
        #Reset the main window status.
        self.clearFunc()
        #Load the commit to widgets.
        self.load_id.emit(commit.id)
        self.commit_current_id.setValue(commit.id)
        self.branch_current.setText(commit.branch.name)
        #Load the expression.
        self.parseFunc(decompress(commit.mechanism))
        #Load pathdata.
        self.pathData = decompress(commit.pathdata)
        self.loadPathFunc()
        #Load algorithmdata.
        self.Designs.result = decompress(commit.algorithmdata)
        self.loadAlgorithmFunc()
        #Workbook loaded.
        self.isSavedFunc()
        print("The specified phase has been loaded.")
    
    def importCommit(self, commit: CommitModel):
        #Load the expression.
        self.parseFunc(decompress(commit.mechanism))
        print("The specified phase has been merged.")
    
    @pyqtSlot()
    def on_commit_stash_clicked(self):
        self.loadCommitID(self.commit_current_id.value())
    
    def loadExample(self):
        #load example by expression.
        example_name, ok = QInputDialog.getItem(self,
            "Examples", "Select a example to load:", [k for k in example_list], 0, False)
        if ok:
            self.parseFunc(example_list[example_name])
            print("Example {} has been loaded.".format(example_name))
