# -*- coding: utf-8 -*-
##Pyslvs - Open Source Planar Linkage Mechanism Simulation and Dimensional Synthesis System.
##Copyright (C) 2016-2018 Yuan Chang
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

from core.QtModules import *
from .Ui_peeweeIO import Ui_Form
from .example import example_list
from typing import List, Dict
import zlib
#NaN coordinate
nan = float('nan')
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
    
    def addResult(self, new_result: List[Dict]):
        for result in new_result:
            self.result.append(result.copy())
    
    def delResult(self, index: int):
        self.result.pop(index)

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
    linkcolor = BlobField()
    #Storage data
    storage = BlobField()
    #Path data
    pathdata = BlobField()
    #Collection data
    collectiondata = BlobField()
    #Triangle collection data
    triangledata = BlobField()
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
        self.pointDataFunc = parent.Entities_Point.data #Get current point data.
        self.linkDataFunc = parent.Entities_Link.data #Get current link data.
        self.storageDataFunc = lambda: tuple(
            (parent.mechanism_storage.item(row).text(), parent.mechanism_storage.item(row).expr)
            for row in range(parent.mechanism_storage.count())
        )
        self.isSavedFunc = parent.workbookSaved #Call it to get main window be shown as saved.
        self.linkGroupFunc = parent.emptyLinkGroup #Add empty link with color.
        self.parseFunc = parent.parseExpression #Main window will load the entered expression.
        self.clearFunc = parent.clear #Reset the main window.
        self.loadStorageFunc = parent.loadStorage #Call to load storages.
        self.loadPathFunc = parent.loadPaths #Call after loaded paths.
        '''
        Mentioned in "core.widgets.custom", because DimensionalSynthesis created after FileWidget.
        
        self.CollectDataFunc #Call to get collections data.
        self.TriangleDataFunc #Call to get triangle data.
        self.loadCollectFunc #Call to load collections data.
        self.loadTriangleFunc #Call to load triangle data.
        self.loadAlgorithmFunc #Call after loaded algorithm results.
        '''
        #Close database when destroyed.
        self.destroyed.connect(self.colseDatabase)
        #Undo Stack
        self.FileState = parent.FileState
        #Reset
        self.reset()
    
    #Clear all the things that dependent on database.
    def reset(self):
        self.history_commit = None #peewee Quary(CommitModel) type
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
    
    def connectDatabase(self, fileName):
        self.colseDatabase()
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, UserModel, BranchModel], safe=True)
    
    @pyqtSlot()
    def colseDatabase(self):
        if not db.deferred:
            db.close()
    
    def save(self, fileName, isBranch=False):
        author_name = self.FileAuthor.text() if self.FileAuthor.text() else self.FileAuthor.placeholderText()
        branch_name = '' if isBranch else self.branch_current.text()
        commit_text = self.FileDescription.text()
        while not author_name:
            author_name, ok = QInputDialog.getText(self, "Author", "Please enter author's name:", QLineEdit.Normal, "Anonymous")
            if not ok:
                return
        while not branch_name.isidentifier():
            branch_name, ok = QInputDialog.getText(self, "Branch", "Please enter a branch name:", QLineEdit.Normal, "master")
            if not ok:
                return
        while not commit_text:
            commit_text, ok = QInputDialog.getText(self, "Commit", "Please add a comment:", QLineEdit.Normal, "Update mechanism.")
            if not ok:
                return
        if fileName!=self.fileName.absoluteFilePath() and os.path.isfile(fileName):
            os.remove(fileName)
            print("The original file has been overwritten.")
        self.connectDatabase(fileName)
        isError = False
        with db.atomic():
            if author_name in (user.name for user in UserModel.select()):
                author_model = UserModel.select().where(UserModel.name==author_name).get()
            else:
                author_model = UserModel(name=author_name)
            if branch_name in (branch.name for branch in BranchModel.select()):
                branch_model = BranchModel.select().where(BranchModel.name==branch_name).get()
            else:
                branch_model = BranchModel(name=branch_name)
            pointData = self.pointDataFunc()
            linkcolor = {vlink.name:vlink.colorSTR for vlink in self.linkDataFunc()}
            args = {
                'author':author_model,
                'description':commit_text,
                'mechanism':compress("M[{}]".format(", ".join(vpoint.expr for vpoint in pointData))),
                'linkcolor':compress(linkcolor),
                'storage':compress(self.storageDataFunc()),
                'pathdata':compress(self.pathData),
                'collectiondata':compress(self.CollectDataFunc()),
                'triangledata':compress(self.TriangleDataFunc()),
                'algorithmdata':compress(self.Designs.result),
                'branch':branch_model
            }
            try:
                args['previous'] = CommitModel.select().where(CommitModel.id==self.commit_current_id.value()).get()
            except CommitModel.DoesNotExist:
                args['previous'] = None
            new_commit = CommitModel(**args)
            try:
                author_model.save()
                branch_model.save()
                new_commit.save()
            except Exception as e:
                print(str(e))
                db.rollback()
                isError = True
            else:
                self.history_commit = CommitModel.select().order_by(CommitModel.id)
        if not isError:
            self.read(fileName)
            print("Saving \"{}\" successful.".format(fileName))
        else:
            os.remove(fileName)
            print("An error was occur when saving database. The file was removed.")
    
    def read(self, fileName):
        self.connectDatabase(fileName)
        history_commit = CommitModel.select().order_by(CommitModel.id)
        if len(history_commit):
            self.clearFunc()
            self.reset()
            self.history_commit = history_commit
            for commit in self.history_commit:
                self.addCommit(commit)
            print("{} commits find in database.".format(len(self.history_commit)))
            self.loadCommit(self.history_commit.order_by(-CommitModel.id).get())
            self.fileName = QFileInfo(fileName)
            self.isSavedFunc()
        else:
            QMessageBox.warning(self, "Warning", "This file is a non-committed database.")
    
    #Pick and import the latest mechanism from a branch.
    def importMechanism(self, fileName):
        self.connectDatabase(fileName)
        commit_all = CommitModel.select().join(BranchModel)
        branch_all = BranchModel.select().order_by(BranchModel.name)
        if self.history_commit!=None:
            self.connectDatabase(self.fileName.absoluteFilePath())
        else:
            self.colseDatabase()
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
            previous_id = "#{}".format(commit.previous.id)
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
        try:
            commit = self.history_commit.where(CommitModel.id==id).get()
        except CommitModel.DoesNotExist:
            QMessageBox.warning(self, "Warning", "Commit ID is not exist.")
        except AttributeError:
            QMessageBox.warning(self, "Warning", "Nothing submitted.")
        else:
            self.loadCommit(commit)
    
    #Load the commit pointer.
    def loadCommit(self, commit: CommitModel):
        if self.checkSaved():
            #Reset the main window status.
            self.clearFunc()
            #Load the commit to widgets.
            print("Load commit #{}".format(commit.id))
            self.load_id.emit(commit.id)
            self.commit_current_id.setValue(commit.id)
            self.branch_current.setText(commit.branch.name)
            #Load the expression.
            self.linkGroupFunc(decompress(commit.linkcolor))
            self.parseFunc(decompress(commit.mechanism))
            #Load the storages.
            self.loadStorageFunc(decompress(commit.storage))
            #Load pathdata.
            self.loadPathFunc(decompress(commit.pathdata))
            #Load collectiondata.
            self.loadCollectFunc(decompress(commit.collectiondata))
            #Load triangledata.
            self.loadTriangleFunc(decompress(commit.triangledata))
            #Load algorithmdata.
            self.Designs.addResult(decompress(commit.algorithmdata))
            self.loadAlgorithmFunc()
            #Workbook loaded.
            self.isSavedFunc()
            print("The specified phase has been loaded.")
    
    #Just load the expression. (No clear step!)
    def importCommit(self, commit: CommitModel):
        self.parseFunc(decompress(commit.mechanism))
        print("The specified phase has been merged.")
    
    #Reload the least commit ID.
    @pyqtSlot()
    def on_commit_stash_clicked(self):
        self.loadCommitID(self.commit_current_id.value())
    
    #Load example to new workbook.
    def loadExample(self, isImport=False):
        if self.checkSaved():
            #load example by expression.
            example_name, ok = QInputDialog.getItem(self,
                "Examples", "Select a example to load:", sorted(k for k in example_list), 0, False)
            if ok:
                if not isImport:
                    self.reset()
                    self.clearFunc()
                self.parseFunc(example_list[example_name])
                self.fileName = QFileInfo(example_name)
                self.isSavedFunc()
                print("Example \"{}\" has been loaded.".format(example_name))
    
    #Check and warn if user is not saved yet.
    def checkSaved(self):
        if self.changed:
            reply = QMessageBox.question(self, "Message", "Are you sure to load?\nAny changes won't be saved.",
                (QMessageBox.Ok | QMessageBox.Cancel), QMessageBox.Ok)
            if reply!=QMessageBox.Ok:
                return False
            return True
        return True
    
    #Commit filter (by description and another).
    @pyqtSlot(str)
    def on_commit_search_text_textEdited(self, text):
        if text:
            for row in range(self.CommitTable.rowCount()):
                self.CommitTable.setRowHidden(row, not (
                    (text in self.CommitTable.item(row, 2).text()) or
                    (text in self.CommitTable.item(row, 3).text())
                ))
        else:
            for row in range(self.CommitTable.rowCount()):
                self.CommitTable.setRowHidden(row, False)
    
    #Change default author's name when select another author.
    @pyqtSlot(str)
    def on_AuthorList_currentTextChanged(self, text):
        self.FileAuthor.setPlaceholderText(text)
    
    #Switch to the last commit of branch.
    @pyqtSlot()
    def on_branch_checkout_clicked(self):
        if self.BranchList.currentRow()>-1:
            branch_name = self.BranchList.currentItem().text()
            if branch_name!=self.branch_current.text():
                leastCommit = self.history_commit.join(BranchModel).where(BranchModel.name==branch_name).order_by(-CommitModel.date).get()
                self.loadCommit(leastCommit)
    
    #Delete all commits in the branch.
    @pyqtSlot()
    def on_branch_delete_clicked(self):
        if self.BranchList.currentRow()>-1:
            branch_name = self.BranchList.currentItem().text()
            if branch_name!=self.branch_current.text():
                fileName = self.fileName.absoluteFilePath()
                #Connect on database to remove all the commit in this branch.
                with db.atomic():
                    branch_quary = BranchModel.select().where(BranchModel.name==branch_name)
                    CommitModel.delete().where(CommitModel.branch.in_(branch_quary)).execute()
                    BranchModel.delete().where(BranchModel.name==branch_name).execute()
                db.close()
                print("Branch {} was deleted.".format(branch_name))
                #Reload database.
                self.read(fileName)
            else:
                QMessageBox.warning(self, "Warning", "Cannot delete current branch.")
