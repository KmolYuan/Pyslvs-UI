# -*- coding: utf-8 -*-

"""SQL database output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QPushButton,
    pyqtSignal,
    QIcon,
    QPixmap,
    QFileInfo,
    QWidget,
    pyqtSlot,
    QInputDialog,
    QLineEdit,
    QMessageBox,
    QTableWidgetItem,
)
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
nan = float('nan')

"""Create a empty Sqlite database object."""
db = SqliteDatabase(None)

class UserModel(Model):
    
    """Show who commited the workbook."""
    
    name = CharField(unique=True)
    
    class Meta:
        database = db

class BranchModel(Model):
    
    """The branch in this workbook."""
    
    name = CharField(unique=True)
    
    class Meta:
        database = db

class CommitModel(Model):
    
    """Commit data: Mechanism and Workbook information.
    
    + Previous and branch commit.
    + Commit time.
    + Workbook information.
    + Expression using Lark parser.
    + Storage data.
    + Path data.
    + Collection data.
    + Triangle collection data.
    + Algorithm data.
    """
    
    previous = ForeignKeyField('self', related_name='next', null=True)
    branch = ForeignKeyField(BranchModel, null=True)
    
    date = DateTimeField(default=datetime.datetime.now)
    
    author = ForeignKeyField(UserModel, null=True)
    description = CharField()
    
    mechanism = BlobField()
    linkcolor = BlobField()
    
    storage = BlobField()
    
    pathdata = BlobField()
    
    collectiondata = BlobField()
    
    triangledata = BlobField()
    
    inputsdata = BlobField()
    
    algorithmdata = BlobField()
    
    class Meta:
        database = db

class LoadCommitButton(QPushButton):
    
    """The button of load commit."""
    
    loaded = pyqtSignal(int)
    
    def __init__(self, id, parent=None):
        super(LoadCommitButton, self).__init__(QIcon(QPixmap(":icons/dataupdate.png")), " #{}".format(id), parent)
        self.setToolTip("Reset to commit #{}.".format(id))
        self.id = id
    
    def mouseReleaseEvent(self, event):
        """Load the commit when release button."""
        super(LoadCommitButton, self).mouseReleaseEvent(event)
        self.loaded.emit(self.id)
    
    def isLoaded(self, id: int):
        """Set enable if this commit is been loaded."""
        self.setEnabled(id != self.id)

class FileWidget(QWidget, Ui_Form):
    
    """The table that stored workbook data,
    including IO functions.
    """
    
    load_id = pyqtSignal(int)
    
    def __init__(self, parent):
        super(FileWidget, self).__init__(parent)
        self.setupUi(self)
        """UI part
        
        + ID
        + Date
        + Description
        + Author
        + Previous
        + Branch
        """
        self.CommitTable.setColumnWidth(0, 70)
        self.CommitTable.setColumnWidth(1, 70)
        self.CommitTable.setColumnWidth(2, 130)
        self.CommitTable.setColumnWidth(3, 70)
        self.CommitTable.setColumnWidth(4, 70)
        self.CommitTable.setColumnWidth(5, 70)
        """The main window functions.
        
        + Get current point data.
        + Get current link data.
        """
        self.pointDataFunc = parent.Entities_Point.data
        self.linkDataFunc = parent.Entities_Link.data
        self.storageDataFunc = lambda: tuple((
            parent.mechanism_storage.item(row).text(),
            parent.mechanism_storage.item(row).expr
        ) for row in range(parent.mechanism_storage.count()))
        """Functions to get and set data.
        
        + Call it to get main window be shown as saved.
        + Add empty link with color.
        + Main window will load the entered expression.
        + Reset the main window.
        + Call to load storages.
        + Call after loaded paths.
        """
        self.isSavedFunc = parent.workbookSaved
        self.linkGroupFunc = parent.emptyLinkGroup
        self.parseFunc = parent.parseExpression
        self.clearFunc = parent.clear
        self.loadStorageFunc = parent.loadStorage
        """Mentioned in 'core.widgets.custom',
        because DimensionalSynthesis created after FileWidget.
        
        self.CollectDataFunc #Call to get collections data.
        self.TriangleDataFunc #Call to get triangle data.
        self.InputsDataFunc #Call to get inputs variables data.
        self.AlgorithmDataFunc #Call to get algorithm data.
        self.pathDataFunc #Call to get path data.
        self.loadCollectFunc #Call to load collections data.
        self.loadTriangleFunc #Call to load triangle data.
        self.loadInputsFunc #Call to load inputs variables data.
        self.loadAlgorithmFunc #Call after loaded algorithm results.
        self.loadPathFunc #Call after loaded paths.
        """
        #Close database when destroyed.
        self.destroyed.connect(self.colseDatabase)
        #Undo Stack
        self.CommandStack = parent.CommandStack
        #Reset
        self.reset()
    
    def reset(self):
        """Clear all the things that dependent on database."""
        #peewee Quary(CommitModel) type
        self.history_commit = None
        self.Script = ""
        self.fileName = QFileInfo("Untitled")
        self.lastTime = datetime.datetime.now()
        self.changed = False
        self.Stack = 0
        self.CommandStack.clear()
        for row in range(self.CommitTable.rowCount()):
            self.CommitTable.removeRow(0)
        self.BranchList.clear()
        self.AuthorList.clear()
        self.FileAuthor.clear()
        self.FileDescription.clear()
        self.branch_current.clear()
        self.commit_search_text.clear()
        self.commit_current_id.setValue(0)
    
    def connectDatabase(self, fileName: str):
        """Connect database."""
        self.colseDatabase()
        db.init(fileName)
        db.connect()
        db.create_tables([CommitModel, UserModel, BranchModel], safe=True)
    
    @pyqtSlot()
    def colseDatabase(self):
        if not db.deferred:
            db.close()
    
    def save(self, fileName: str, isBranch=False):
        """Save database.
        
        + Append to new branch function.
        """
        author_name = self.FileAuthor.text()
        if not author_name:
            author_name = self.FileAuthor.placeholderText()
        branch_name = '' if isBranch else self.branch_current.text()
        commit_text = self.FileDescription.text()
        while not author_name:
            author_name, ok = QInputDialog.getText(self, "Author",
                "Please enter author's name:",
                QLineEdit.Normal,
                "Anonymous"
            )
            if not ok:
                return
        while not branch_name.isidentifier():
            branch_name, ok = QInputDialog.getText(self, "Branch",
                "Please enter a branch name:",
                QLineEdit.Normal,
                "master"
            )
            if not ok:
                return
        while not commit_text:
            commit_text, ok = QInputDialog.getText(self, "Commit",
                "Please add a comment:",
                QLineEdit.Normal,
                "Update mechanism."
            )
            if not ok:
                return
        if (
            (fileName != self.fileName.absoluteFilePath()) and
            os.path.isfile(fileName)
        ):
            os.remove(fileName)
            print("The original file has been overwritten.")
        self.connectDatabase(fileName)
        isError = False
        with db.atomic():
            if author_name in (user.name for user in UserModel.select()):
                author_model = (
                    UserModel
                    .select()
                    .where(UserModel.name==author_name)
                    .get()
                )
            else:
                author_model = UserModel(name=author_name)
            if branch_name in (branch.name for branch in BranchModel.select()):
                branch_model = (
                    BranchModel
                    .select()
                    .where(BranchModel.name==branch_name)
                    .get()
                )
            else:
                branch_model = BranchModel(name=branch_name)
            pointData = self.pointDataFunc()
            linkcolor = {
                vlink.name: vlink.colorSTR
                for vlink in self.linkDataFunc()
            }
            args = {
                'author':author_model,
                'description':commit_text,
                'mechanism':compress("M[{}]".format(", ".join(
                    vpoint.expr for vpoint in pointData
                ))),
                'linkcolor': compress(linkcolor),
                'storage': compress(self.storageDataFunc()),
                'pathdata': compress(self.pathDataFunc()),
                'collectiondata': compress(self.CollectDataFunc()),
                'triangledata': compress(self.TriangleDataFunc()),
                'inputsdata': compress(self.InputsDataFunc()),
                'algorithmdata': compress(self.AlgorithmDataFunc()),
                'branch': branch_model
            }
            try:
                args['previous'] = (
                    CommitModel
                    .select()
                    .where(CommitModel.id == self.commit_current_id.value())
                    .get()
                )
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
                self.history_commit = (
                    CommitModel
                    .select()
                    .order_by(CommitModel.id)
                )
        if isError:
            os.remove(fileName)
            print("The file was removed.")
            return
        self.read(fileName)
        print("Saving \"{}\" successful.".format(fileName))
        size = QFileInfo(fileName).size()
        print("Size: {}".format(
            "{} MB".format(round(size/1024/1024, 2))
            if size / 1024 // 1024
            else "{} KB".format(round(size/1024, 2))
        ))
    
    def read(self, fileName: str):
        """Load database commit."""
        self.connectDatabase(fileName)
        history_commit = CommitModel.select().order_by(CommitModel.id)
        commit_count = len(history_commit)
        if not commit_count:
            QMessageBox.warning(self,
                "Warning",
                "This file is a non-committed database."
            )
            return
        self.clearFunc()
        self.reset()
        self.history_commit = history_commit
        for commit in self.history_commit:
            self.addCommit(commit)
        print("{} commit(s) was find in database.".format(commit_count))
        self.loadCommit(self.history_commit.order_by(-CommitModel.id).get())
        self.fileName = QFileInfo(fileName)
        self.isSavedFunc()
    
    def importMechanism(self, fileName: str):
        """Pick and import the latest mechanism from a branch."""
        self.connectDatabase(fileName)
        commit_all = CommitModel.select().join(BranchModel)
        branch_all = BranchModel.select().order_by(BranchModel.name)
        if self.history_commit!=None:
            self.connectDatabase(self.fileName.absoluteFilePath())
        else:
            self.colseDatabase()
        branch_name, ok = QInputDialog.getItem(self,
            "Branch",
            "Select the latest commit in the branch to load.",
            [branch.name for branch in branch_all],
            0,
            False
        )
        if not ok:
            return
        try:
            commit = (
                commit_all
                .where(BranchModel.name==branch_name)
                .order_by(CommitModel.date)
                .get()
            )
        except CommitModel.DoesNotExist:
            QMessageBox.warning(self,
                "Warning",
                "This file is a non-committed database."
            )
        else:
            self.importCommit(commit)
    
    def addCommit(self, commit: CommitModel):
        """Add commit data to all widgets.
        
        + Commit ID
        + Date
        + Description
        + Author
        + Previous commit
        + Branch
        + Add to table widget.
        """
        row = self.CommitTable.rowCount()
        self.CommitTable.insertRow(row)
        
        self.commit_current_id.setValue(commit.id)
        button = LoadCommitButton(commit.id, self)
        button.loaded.connect(self.loadCommitID)
        self.load_id.connect(button.isLoaded)
        self.CommitTable.setCellWidget(row, 0, button)
        
        date = (
            "{t.year:02d}-{t.month:02d}-{t.day:02d} " +
            "{t.hour:02d}:{t.minute:02d}:{t.second:02d}"
        ).format(t=commit.date)
        
        self.CommitTable.setItem(row, 2, QTableWidgetItem(commit.description))
        
        author_name = commit.author.name
        all_authors = [
            self.AuthorList.item(row).text()
            for row in range(self.AuthorList.count())
        ]
        if author_name not in all_authors:
            self.AuthorList.addItem(author_name)
        
        if commit.previous:
            previous_id = "#{}".format(commit.previous.id)
        else:
            previous_id = "None"
        
        branch_name = commit.branch.name
        all_branchs = [
            self.BranchList.item(row).text()
            for row in range(self.BranchList.count())
        ]
        if branch_name not in all_branchs:
            self.BranchList.addItem(branch_name)
        self.branch_current.setText(branch_name)
        
        for i, text in enumerate([
            date,
            commit.description,
            author_name,
            previous_id,
            branch_name
        ]):
            item = QTableWidgetItem(text)
            item.setToolTip(text)
            self.CommitTable.setItem(row, i+1, item)
    
    def loadCommitID(self, id: int):
        """Check the id is correct."""
        try:
            commit = self.history_commit.where(CommitModel.id==id).get()
        except CommitModel.DoesNotExist:
            QMessageBox.warning(self, "Warning", "Commit ID is not exist.")
        except AttributeError:
            QMessageBox.warning(self, "Warning", "Nothing submitted.")
        else:
            self.loadCommit(commit)
    
    def loadCommit(self, commit: CommitModel):
        """Load the commit pointer."""
        if not self.checkSaved():
            return
        #Reset the main window status.
        self.clearFunc()
        #Load the commit to widgets.
        print("Loading commit #{}.".format(commit.id))
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
        #Load inputsdata.
        self.loadInputsFunc(decompress(commit.inputsdata))
        #Load algorithmdata.
        self.loadAlgorithmFunc(decompress(commit.algorithmdata))
        #Workbook loaded.
        self.isSavedFunc()
        print("The specified phase has been loaded.")
    
    def importCommit(self, commit: CommitModel):
        """Just load the expression. (No clear step!)"""
        self.parseFunc(decompress(commit.mechanism))
        print("The specified phase has been merged.")
    
    @pyqtSlot()
    def on_commit_stash_clicked(self):
        """Reload the least commit ID."""
        self.loadCommitID(self.commit_current_id.value())
    
    def loadExample(self, isImport=False) -> bool:
        """Load example to new workbook."""
        if not self.checkSaved():
            return False
        #load example by expression.
        example_name, ok = QInputDialog.getItem(self,
            "Examples",
            "Select a example to load:",
            sorted(k for k in example_list),
            0,
            False
        )
        if not ok:
            return False
        if not isImport:
            self.reset()
            self.clearFunc()
        self.parseFunc(example_list[example_name])
        self.fileName = QFileInfo(example_name)
        self.isSavedFunc()
        print("Example \"{}\" has been loaded.".format(example_name))
        return True
    
    def checkSaved(self) -> bool:
        """Check and warn if user is not saved yet."""
        if not self.changed:
            return True
        reply = QMessageBox.question(self,
            "Message",
            "Are you sure to load?\nAny changes won't be saved.",
            (QMessageBox.Ok | QMessageBox.Cancel),
            QMessageBox.Ok
        )
        return reply == QMessageBox.Ok
    
    @pyqtSlot(str)
    def on_commit_search_text_textEdited(self, text: str):
        """Commit filter (by description and another)."""
        if not text:
            for row in range(self.CommitTable.rowCount()):
                self.CommitTable.setRowHidden(row, False)
            return
        for row in range(self.CommitTable.rowCount()):
            self.CommitTable.setRowHidden(row, not (
                (text in self.CommitTable.item(row, 2).text()) or
                (text in self.CommitTable.item(row, 3).text())
            ))
    
    @pyqtSlot(str)
    def on_AuthorList_currentTextChanged(self, text: str):
        """Change default author's name when select another author."""
        self.FileAuthor.setPlaceholderText(text)
    
    @pyqtSlot()
    def on_branch_checkout_clicked(self):
        """Switch to the last commit of branch."""
        if not self.BranchList.currentRow() > -1:
            return
        branch_name = self.BranchList.currentItem().text()
        if branch_name != self.branch_current.text():
            leastCommit = (
                self.history_commit
                .join(BranchModel)
                .where(BranchModel.name == branch_name)
                .order_by(-CommitModel.date)
                .get()
            )
            self.loadCommit(leastCommit)
    
    @pyqtSlot()
    def on_branch_delete_clicked(self):
        """Delete all commits in the branch."""
        if not self.BranchList.currentRow() > -1:
            return
        branch_name = self.BranchList.currentItem().text()
        if branch_name != self.branch_current.text():
            fileName = self.fileName.absoluteFilePath()
            #Connect on database to remove all the commit in this branch.
            with db.atomic():
                branch_quary = (
                    BranchModel
                    .select()
                    .where(BranchModel.name == branch_name)
                )
                (
                    CommitModel
                    .delete()
                    .where(CommitModel.branch.in_(branch_quary))
                    .execute()
                )
                (
                    BranchModel
                    .delete()
                    .where(BranchModel.name == branch_name)
                    .execute()
                )
            db.close()
            print("Branch {} was deleted.".format(branch_name))
            #Reload database.
            self.read(fileName)
        else:
            QMessageBox.warning(self,
                "Warning",
                "Cannot delete current branch."
            )
