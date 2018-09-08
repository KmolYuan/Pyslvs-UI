# -*- coding: utf-8 -*-

"""SQL database output function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from os import remove as os_remove
from os.path import isfile
import datetime
from zlib import compress, decompress
from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    BlobField,
    ForeignKeyField,
    DateTimeField,
)
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
from core.libs import example_list
from .overview import WorkbookOverview
from .Ui_database import Ui_Form
nan = float('nan')


def _compress(obj: object) -> bytes:
    """Use to encode the Python script as bytes code."""
    return compress(bytes(repr(obj), encoding="utf8"), 5)


def _decompress(obj: bytes) -> object:
    """Use to decode the Python script."""
    return eval(decompress(obj).decode())


"""Create a empty Sqlite database object."""
_db = SqliteDatabase(None)


class UserModel(Model):
    
    """Show who commited the workbook."""
    
    name = CharField(unique=True)
    
    class Meta:
        database = _db


class BranchModel(Model):
    
    """The branch in this workbook."""
    
    name = CharField(unique=True)
    
    class Meta:
        database = _db


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
    + Input variables data.
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
        database = _db


class LoadCommitButton(QPushButton):
    
    """The button of load commit."""
    
    loaded = pyqtSignal(int)
    
    def __init__(self, id: int, parent: QWidget):
        super(LoadCommitButton, self).__init__(
            QIcon(QPixmap(":icons/dataupdate.png")),
            f" # {id}",
            parent
        )
        self.setToolTip(f"Reset to commit # {id}.")
        self.id = id
    
    def mouseReleaseEvent(self, event):
        """Load the commit when release button."""
        super(LoadCommitButton, self).mouseReleaseEvent(event)
        self.loaded.emit(self.id)
    
    def isLoaded(self, id: int):
        """Set enable if this commit is been loaded."""
        self.setEnabled(id != self.id)


class FileWidget(QWidget, Ui_Form):
    
    """The table that stored workbook data and changes."""
    
    load_id = pyqtSignal(int)
    
    def __init__(self, parent: QWidget):
        """Set attributes.
        
        + UI part
        + The main window functions
        + Functions to get and set data
        + External functions.
        """
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
        self.pointExprFunc = parent.EntitiesPoint.expression
        self.linkExprFunc = parent.EntitiesLink.dataDict
        self.storageDataFunc = parent.getStorage
        """Functions to get and set data.
        
        + Call it to get main window be shown as saved.
        + Add empty link with color.
        + Main window will load the entered expression.
        + Reset the main window.
        + Call to load storages.
        + Call after loaded paths.
        """
        self.checkFileChanged = parent.checkFileChanged
        self.isSavedFunc = parent.workbookSaved
        self.addLinksFunc = parent.addEmptyLinks
        self.parseFunc = parent.parseExpression
        self.clearFunc = parent.clear
        self.addStorageFunc = parent.addMultipleStorage
        
        # Call to get collections data.
        self.CollectDataFunc = parent.CollectionTabPage.CollectDataFunc
        # Call to get triangle data.
        self.TriangleDataFunc = parent.CollectionTabPage.TriangleDataFunc
        # Call to get inputs variables data.
        self.InputsDataFunc = parent.InputsWidget.inputPair
        # Call to get algorithm data.
        self.AlgorithmDataFunc = parent.DimensionalSynthesis.mechanismData
        # Call to get path data.
        self.pathDataFunc = parent.InputsWidget.pathData
        # Call to load collections data.
        self.loadCollectFunc = parent.CollectionTabPage.StructureWidget.addCollections
        # Call to load triangle data.
        self.loadTriangleFunc = parent.CollectionTabPage.TriangularIterationWidget.addCollections
        # Call to load inputs variables data.
        self.loadInputsFunc = parent.InputsWidget.addInputsVariables
        # Call after loaded algorithm results.
        self.loadAlgorithmFunc = parent.DimensionalSynthesis.loadResults
        # Call after loaded paths.
        self.loadPathFunc = parent.InputsWidget.loadPaths
        
        # Close database when destroyed.
        self.destroyed.connect(self.__closeDatabase)
        # Undo Stack
        self.commandClear = parent.CommandStack.clear
        # Reset
        self.reset()
    
    def reset(self):
        """Clear all the things that dependent on database."""
        # peewee Quary(CommitModel) type
        self.history_commit = None
        self.Script = ""
        self.file_name = QFileInfo("Untitled")
        self.lastTime = datetime.datetime.now()
        self.changed = False
        self.Stack = 0
        self.commandClear()
        for row in range(self.CommitTable.rowCount()):
            self.CommitTable.removeRow(0)
        self.BranchList.clear()
        self.AuthorList.clear()
        self.FileAuthor.clear()
        self.FileDescription.clear()
        self.branch_current.clear()
        self.commit_search_text.clear()
        self.commit_current_id.setValue(0)
        self.__closeDatabase()
    
    def __connectDatabase(self, file_name: str):
        """Connect database."""
        self.__closeDatabase()
        _db.init(file_name)
        _db.connect()
        _db.create_tables([CommitModel, UserModel, BranchModel], safe=True)
    
    @pyqtSlot()
    def __closeDatabase(self):
        if not _db.deferred:
            _db.close()
    
    def save(self, file_name: str, isBranch: bool = False):
        """Save database, append commit to new branch function."""
        author_name = self.FileAuthor.text() or self.FileAuthor.placeholderText()
        branch_name = '' if isBranch else self.branch_current.text()
        commit_text = self.FileDescription.text()
        while not author_name:
            author_name, ok = QInputDialog.getText(
                self,
                "Author",
                "Please enter author's name:",
                QLineEdit.Normal,
                "Anonymous"
            )
            if not ok:
                return
        while not branch_name.isidentifier():
            branch_name, ok = QInputDialog.getText(
                self,
                "Branch",
                "Please enter a branch name:",
                QLineEdit.Normal,
                "master"
            )
            if not ok:
                return
        while not commit_text:
            commit_text, ok = QInputDialog.getText(
                self,
                "Commit",
                "Please add a comment:",
                QLineEdit.Normal,
                "Update mechanism."
            )
            if not ok:
                return
        if (file_name != self.file_name.absoluteFilePath()) and isfile(file_name):
            os_remove(file_name)
            print("The original file has been overwritten.")
        self.__connectDatabase(file_name)
        isError = False
        with _db.atomic():
            if author_name in (user.name for user in UserModel.select()):
                author_model = (UserModel
                    .select()
                    .where(UserModel.name == author_name)
                    .get())
            else:
                author_model = UserModel(name=author_name)
            if branch_name in (branch.name for branch in BranchModel.select()):
                branch_model = (BranchModel
                    .select()
                    .where(BranchModel.name == branch_name)
                    .get())
            else:
                branch_model = BranchModel(name=branch_name)
            args = {
                'author': author_model,
                'description': commit_text,
                'mechanism': _compress(self.pointExprFunc()),
                'linkcolor': _compress(self.linkExprFunc()),
                'storage': _compress(self.storageDataFunc()),
                'pathdata': _compress(self.pathDataFunc()),
                'collectiondata': _compress(self.CollectDataFunc()),
                'triangledata': _compress(self.TriangleDataFunc()),
                'inputsdata': _compress(tuple(self.InputsDataFunc(has_angles=False))),
                'algorithmdata': _compress(self.AlgorithmDataFunc()),
                'branch': branch_model,
            }
            try:
                args['previous'] = (CommitModel
                    .select()
                    .where(CommitModel.id == self.commit_current_id.value())
                    .get())
            except CommitModel.DoesNotExist:
                args['previous'] = None
            new_commit = CommitModel(**args)
            try:
                author_model.save()
                branch_model.save()
                new_commit.save()
            except Exception as e:
                print(str(e))
                _db.rollback()
                isError = True
            else:
                self.history_commit = CommitModel.select().order_by(CommitModel.id)
        if isError:
            os_remove(file_name)
            print("The file was removed.")
            return
        self.read(file_name, showdlg = False)
        print(f"Saving \"{file_name}\" successful.")
        size = QFileInfo(file_name).size()
        print("Size: " + (
            f"{size / 1024 / 1024:.02f} MB"
            if size / 1024 // 1024 else
            f"{size / 1024:.02f} KB"
        ))
    
    def read(self, file_name: str, *, showdlg: bool = True):
        """Load database commit."""
        self.__connectDatabase(file_name)
        history_commit = CommitModel.select().order_by(CommitModel.id)
        commit_count = len(history_commit)
        if not commit_count:
            QMessageBox.warning(
                self,
                "Warning",
                "This file is a non-committed database."
            )
            return
        self.clearFunc()
        self.reset()
        self.history_commit = history_commit
        for commit in self.history_commit:
            self.__addCommit(commit)
        print(f"{commit_count} commit(s) was find in database.")
        self.__loadCommit(
            self.history_commit.order_by(-CommitModel.id).get(),
            showdlg = showdlg
        )
        self.file_name = QFileInfo(file_name)
        self.isSavedFunc()
    
    def importMechanism(self, file_name: str):
        """Pick and import the latest mechanism from a branch."""
        self.__connectDatabase(file_name)
        commit_all = CommitModel.select().join(BranchModel)
        branch_all = BranchModel.select().order_by(BranchModel.name)
        if self.history_commit:
            self.__connectDatabase(self.file_name.absoluteFilePath())
        else:
            self.__closeDatabase()
        branch_name, ok = QInputDialog.getItem(
            self,
            "Branch",
            "Select the latest commit in the branch to load.",
            [branch.name for branch in branch_all],
            0,
            False
        )
        if not ok:
            return
        try:
            commit = (commit_all
                .where(BranchModel.name==branch_name)
                .order_by(CommitModel.date)
                .get())
        except CommitModel.DoesNotExist:
            QMessageBox.warning(
                self,
                "Warning",
                "This file is a non-committed database."
            )
        else:
            self.__importCommit(commit)
    
    def __addCommit(self, commit: CommitModel):
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
        button.loaded.connect(self.__loadCommitID)
        self.load_id.connect(button.isLoaded)
        self.CommitTable.setCellWidget(row, 0, button)
        
        self.CommitTable.setItem(row, 2, QTableWidgetItem(commit.description))
        
        author_name = commit.author.name
        for row in range(self.AuthorList.count()):
            if author_name == self.AuthorList.item(row).text():
                break
        else:
            self.AuthorList.addItem(author_name)
        
        branch_name = commit.branch.name
        for row in range(self.BranchList.count()):
            if branch_name == self.BranchList.item(row).text():
                break
        else:
            self.BranchList.addItem(branch_name)
        self.branch_current.setText(branch_name)
        t = commit.date
        for i, text in enumerate((
            f"{t.year:02d}-{t.month:02d}-{t.day:02d} "
            f"{t.hour:02d}:{t.minute:02d}:{t.second:02d}",
            commit.description,
            author_name,
            f"#{commit.previous.id}" if commit.previous else "None",
            branch_name
        )):
            item = QTableWidgetItem(text)
            item.setToolTip(text)
            self.CommitTable.setItem(row, i + 1, item)
    
    def __loadCommitID(self, id: int):
        """Check the id is correct."""
        try:
            commit = self.history_commit.where(CommitModel.id == id).get()
        except CommitModel.DoesNotExist:
            QMessageBox.warning(self, "Warning", "Commit ID is not exist.")
        except AttributeError:
            QMessageBox.warning(self, "Warning", "Nothing submitted.")
        else:
            self.__loadCommit(commit)
    
    def __loadCommit(self, commit: CommitModel, *, showdlg: bool = True):
        """Load the commit pointer."""
        if self.checkFileChanged():
            return
        # Reset the main window status.
        self.clearFunc()
        # Load the commit to widgets.
        print(f"Loading commit # {commit.id}.")
        self.load_id.emit(commit.id)
        self.commit_current_id.setValue(commit.id)
        self.branch_current.setText(commit.branch.name)
        # Load the expression.
        self.addLinksFunc(_decompress(commit.linkcolor))
        self.parseFunc(_decompress(commit.mechanism))
        # Load the storages.
        self.addStorageFunc(_decompress(commit.storage))
        # Load pathdata.
        self.loadPathFunc(_decompress(commit.pathdata))
        # Load collectiondata.
        self.loadCollectFunc(_decompress(commit.collectiondata))
        # Load triangledata.
        self.loadTriangleFunc(_decompress(commit.triangledata))
        # Load inputsdata.
        self.loadInputsFunc(_decompress(commit.inputsdata))
        # Load algorithmdata.
        self.loadAlgorithmFunc(_decompress(commit.algorithmdata))
        # Workbook loaded.
        self.isSavedFunc()
        print("The specified phase has been loaded.")
        # Show overview dialog.
        dlg = WorkbookOverview(commit, _decompress, self)
        dlg.show()
        dlg.exec_()
    
    def __importCommit(self, commit: CommitModel):
        """Just load the expression. (No clear step!)"""
        self.parseFunc(_decompress(commit.mechanism))
        print("The specified phase has been merged.")
    
    @pyqtSlot(name='on_commit_stash_clicked')
    def stash(self):
        """Reload the least commit ID."""
        self.__loadCommitID(self.commit_current_id.value())
    
    def loadExample(self, isImport: bool = False) -> bool:
        """Load example to new workbook."""
        if self.checkFileChanged():
            return False
        # load example by expression.
        example_name, ok = QInputDialog.getItem(
            self,
            "Examples",
            "Select an example to load:",
            sorted(example_list),
            0,
            False
        )
        if not ok:
            return False
        expr, inputs = example_list[example_name]
        if not isImport:
            self.reset()
            self.clearFunc()
        self.parseFunc(expr)
        if not isImport:
            # Import without input data.
            self.loadInputsFunc(inputs)
        self.file_name = QFileInfo(example_name)
        self.isSavedFunc()
        print(f"Example \"{example_name}\" has been loaded.")
        return True
    
    @pyqtSlot(str, name='on_commit_search_text_textEdited')
    def __setSearchText(self, text: str):
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
    
    @pyqtSlot(str, name='on_AuthorList_currentTextChanged')
    def __setAuthor(self, text: str):
        """Change default author's name when select another author."""
        self.FileAuthor.setPlaceholderText(text)
    
    @pyqtSlot(name='on_branch_checkout_clicked')
    def __checkoutBranch(self):
        """Switch to the last commit of branch."""
        if not self.BranchList.currentRow() > -1:
            return
        branch_name = self.BranchList.currentItem().text()
        if branch_name == self.branch_current.text():
            return
        leastCommit = (self.history_commit
            .join(BranchModel)
            .where(BranchModel.name == branch_name)
            .order_by(-CommitModel.date)
            .get())
        self.__loadCommit(leastCommit)
    
    @pyqtSlot(name='on_branch_delete_clicked')
    def __deleteBranch(self):
        """Delete all commits in the branch."""
        if not self.BranchList.currentRow() > -1:
            return
        branch_name = self.BranchList.currentItem().text()
        if branch_name == self.branch_current.text():
            QMessageBox.warning(
                self,
                "Warning",
                "Cannot delete current branch."
            )
            return
        file_name = self.file_name.absoluteFilePath()
        # Connect on database to remove all the commit in this branch.
        with _db.atomic():
            (CommitModel
                .delete()
                .where(
                    CommitModel.branch.in_(BranchModel
                        .select()
                        .where(BranchModel.name == branch_name)
                    )
                )
                .execute())
            (BranchModel
                .delete()
                .where(BranchModel.name == branch_name)
                .execute())
        _db.close()
        print(f"Branch {branch_name} was deleted.")
        # Reload database.
        self.read(file_name)
