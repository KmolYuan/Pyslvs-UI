# -*- coding: utf-8 -*-

"""All of undoable commands in Pyslvs.

+ The add and delete commands has only add and delete.
+ The add commands need to edit Points or Links list
  after it added to table.
+ The delete commands need to clear Points or Links list
  before it deleted from table.

+ The edit command need to know who is included by the VPoint or VLink.

Put the pointer under 'self' when the classes are initialize.
'redo' method will be called when pushing into the stack.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Sequence,
    List,
    Dict,
    Tuple,
    Iterator,
    Union,
)
from core.QtModules import (
    Qt,
    QUndoCommand,
    QTableWidget,
    QTableWidgetItem,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QIcon,
    QPixmap,
)


def _noNoneString(str_list: Union[List[str], Iterator[str]]) -> Iterator[str]:
    """Filter to exclude empty string."""
    return (s for s in str_list if s)


class AddTable(QUndoCommand):
    
    """Add a row at last of the table."""
    
    def __init__(self, table: QTableWidget):
        """Attributes
        
        + Table reference
        """
        super(AddTable, self).__init__()
        self.table = table
    
    def redo(self):
        """Add a empty row and add
        empty text strings into table items.
        """
        row = self.table.rowCount()
        self.table.insertRow(row)
        for column in range(row):
            self.table.setItem(row, column, QTableWidgetItem(''))
    
    def undo(self):
        """Remove the last row directly."""
        self.table.removeRow(self.table.rowCount()-1)


class DeleteTable(QUndoCommand):
    
    """Delete the specified row of table.
    
    When this class has been called, the items should be empty.
    """
    
    def __init__(self, row: int, table: QTableWidget, isRename: bool):
        """Attributes
        
        + Table reference
        + Row
        + Should rename
        """
        super(DeleteTable, self).__init__()
        self.table = table
        self.row = row
        self.isRename = isRename
    
    def redo(self):
        """Remove the row and rename sequence."""
        self.table.removeRow(self.row)
        if self.isRename:
            self.table.rename(self.row)
    
    def undo(self):
        """Rename again then insert a empty row."""
        if self.isRename:
            self.table.rename(self.row)
        self.table.insertRow(self.row)
        for column in range(self.table.columnCount()):
            self.table.setItem(self.row, column, QTableWidgetItem(''))


class FixSequenceNumber(QUndoCommand):
    
    """Fix sequence number when deleting a point."""
    
    def __init__(self, table: QTableWidget, row: int, benchmark: int):
        """Attributes
        
        + Table reference
        + Row
        + Benchmark
        """
        super(FixSequenceNumber, self).__init__()
        self.table = table
        self.row = row
        self.benchmark = benchmark
    
    def redo(self):
        self.sorting(True)
    
    def undo(self):
        self.sorting(False)
    
    def sorting(self, bs: bool):
        """Sorting point number by benchmark."""
        item = self.table.item(self.row, 2)
        if not item.text():
            return
        points = [int(p.replace('Point', '')) for p in item.text().split(',')]
        if bs:
            points = [p-1 if p > self.benchmark else p for p in points]
        else:
            points = [p+1 if p >= self.benchmark else p for p in points]
        points = ['Point{}'.format(p) for p in points]
        item.setText(','.join(points))


class EditPointTable(QUndoCommand):
    
    """Edit Point table.
    
    Copy old data and put it back when called undo.
    """
    
    def __init__(self,
        row: int,
        PointTable: QTableWidgetItem,
        LinkTable: QTableWidgetItem,
        args: Sequence[Union[str, int, float]]
    ):
        super(EditPointTable, self).__init__()
        self.PointTable = PointTable
        self.row = row
        self.LinkTable = LinkTable
        self.args = tuple(args)
        self.OldArgs = self.PointTable.rowTexts(row)
        #Tuple[str] -> Set[str]
        newLinks = set(self.args[0].split(','))
        oldLinks = set(self.OldArgs[0].split(','))
        self.NewLinkItems = []
        self.OldLinkItems = []
        for row in range(self.LinkTable.rowCount()):
            linkName = self.LinkTable.item(row, 0).text()
            if linkName in newLinks - oldLinks:
                self.NewLinkItems.append(row)
            if linkName in oldLinks - newLinks:
                self.OldLinkItems.append(row)
        self.NewLinkItems = tuple(self.NewLinkItems)
        self.OldLinkItems = tuple(self.OldLinkItems)
    
    def redo(self):
        """Write arguments then rewrite the dependents."""
        self.PointTable.editArgs(self.row, *self.args)
        self.writeRows(self.NewLinkItems, self.OldLinkItems)
    
    def undo(self):
        """Rewrite the dependents then write arguments."""
        self.writeRows(self.OldLinkItems, self.NewLinkItems)
        self.PointTable.editArgs(self.row, *self.OldArgs)
    
    def writeRows(self,
        items1: Sequence[int],
        items2: Sequence[int]
    ):
        """Write table function.
        
        + Append the point that relate with these links.
        + Remove the point that irrelevant with these links.
        """
        point_name = 'Point{}'.format(self.row)
        for row in items1:
            newPoints = self.LinkTable.item(row, 2).text().split(',')
            newPoints.append(point_name)
            self.setCell(row, newPoints)
        for row in items2:
            newPoints = self.LinkTable.item(row, 2).text().split(',')
            newPoints.remove(point_name)
            self.setCell(row, newPoints)
    
    def setCell(self, row: int, points: List[str]):
        item = QTableWidgetItem(','.join(_noNoneString(points)))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.LinkTable.setItem(row, 2, item)


class EditLinkTable(QUndoCommand):
    
    """Edit Link table.
    
    Copy old data and put it back when called undo.
    """
    
    def __init__(self,
        row: int,
        LinkTable: QTableWidgetItem,
        PointTable: QTableWidgetItem,
        args: Sequence[str]
    ):
        super(EditLinkTable, self).__init__()
        self.LinkTable = LinkTable
        self.row = row
        self.PointTable = PointTable
        self.args = tuple(args)
        self.OldArgs = self.LinkTable.rowTexts(row, hasName=True)
        #Points: Tuple[int]
        newPoints = self.args[2].split(',')
        oldPoints = self.OldArgs[2].split(',')
        newPoints = set(
            int(index.replace('Point', ''))
            for index in _noNoneString(newPoints)
        )
        oldPoints = set(
            int(index.replace('Point', ''))
            for index in _noNoneString(oldPoints)
        )
        self.NewPointItems = tuple(newPoints - oldPoints)
        self.OldPointItems = tuple(oldPoints - newPoints)
    
    def redo(self):
        """Write arguments then rewrite the dependents."""
        self.LinkTable.editArgs(self.row, *self.args)
        self.rename(self.args, self.OldArgs)
        self.writeRows(self.args[0], self.NewPointItems, self.OldPointItems)
    
    def undo(self):
        """Rewrite the dependents then write arguments."""
        self.writeRows(self.OldArgs[0], self.OldPointItems, self.NewPointItems)
        self.rename(self.OldArgs, self.args)
        self.LinkTable.editArgs(self.row, *self.OldArgs)
    
    def rename(self, Args1: Tuple[str], Args2: Tuple[str]):
        """Adjust link name in all dependents,
        if link name are changed.
        """
        if Args2[0] == Args1[0]:
            return
        for index in _noNoneString(Args2[2].split(',')):
            row = int(index.replace('Point', ''))
            newLinks = self.PointTable.item(row, 1).text().split(',')
            item = QTableWidgetItem(','.join(_noNoneString(
                w.replace(Args2[0], Args1[0])
                for w in newLinks
            )))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.PointTable.setItem(row, 1, item)
    
    def writeRows(self,
        name: str,
        items1: Sequence[int],
        items2: Sequence[int]
    ):
        """Write table function.
        
        + Append the link that relate with these points.
        + Remove the link that irrelevant with these points.
        """
        for row in items1:
            newLinks = self.PointTable.item(row, 1).text().split(',')
            newLinks.append(name)
            self.setCell(row, newLinks)
        for row in items2:
            newLinks = self.PointTable.item(row, 1).text().split(',')
            if name:
                newLinks.remove(name)
            self.setCell(row, newLinks)
    
    def setCell(self, row: int, links: List[str]):
        item = QTableWidgetItem(','.join(_noNoneString(links)))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.PointTable.setItem(row, 1, item)


class AddPath(QUndoCommand):
    
    """Append a new path."""
    
    def __init__(self,
        widget: QListWidget,
        name: str,
        data: Dict[str, Tuple[Tuple[float, float]]],
        path: Tuple[Tuple[float, float]]
    ):
        super(AddPath, self).__init__()
        self.widget = widget
        self.name = name
        self.data = data
        self.path = path
    
    def redo(self):
        """Add new path data."""
        self.data[self.name] = self.path
        self.widget.addItem("{}: {}".format(self.name, ", ".join(
            "[{}]".format(i)
            for i, d in enumerate(self.path) if d
        )))
    
    def undo(self):
        """Remove the last item."""
        self.widget.takeItem(self.widget.count()-1)
        del self.data[self.name]


class DeletePath(QUndoCommand):
    
    """"Delete the specified row of path."""
    
    def __init__(self,
        row: int,
        widget: QListWidget,
        data: Tuple[Tuple[float, float]]
    ):
        super(DeletePath, self).__init__()
        self.row = row
        self.widget = widget
        self.data = data
    
    def redo(self):
        """Delete the path."""
        self.oldItem = self.widget.takeItem(self.row)
        name = self.oldItem.text().split(':')[0]
        self.oldPath = self.data[name]
        del self.data[name]
    
    def undo(self):
        """Append back the path."""
        self.data[self.oldItem.text().split(':')[0]] = self.oldPath
        self.widget.addItem(self.oldItem)
        self.widget.setCurrentRow(self.widget.row(self.oldItem))


class AddStorage(QUndoCommand):
    
    """Append a new storage."""
    
    def __init__(self, name: str, widget: QListWidget, mechanism: str):
        super(AddStorage, self).__init__()
        self.name = name
        self.widget = widget
        self.mechanism = mechanism
    
    def redo(self):
        """Add mechanism expression to 'expr' attribute."""
        item = QListWidgetItem(self.name)
        item.expr = self.mechanism
        item.setIcon(QIcon(QPixmap(":/icons/mechanism.png")))
        self.widget.addItem(item)
    
    def undo(self):
        """Remove the last item."""
        self.widget.takeItem(self.widget.count()-1)


class DeleteStorage(QUndoCommand):
    
    """Delete the specified row of storage."""
    
    def __init__(self, row: int, widget: QListWidget):
        super(DeleteStorage, self).__init__()
        self.row = row
        self.widget = widget
        self.name = widget.item(row).text()
        self.mechanism = widget.item(row).expr
    
    def redo(self):
        """Remove the row directly."""
        self.widget.takeItem(self.row)
    
    def undo(self):
        """Create a new item and recover expression."""
        item = QListWidgetItem(self.name)
        item.expr = self.mechanism
        item.setIcon(QIcon(QPixmap(":/icons/mechanism.png")))
        self.widget.insertItem(self.row, item)


class AddStorageName(QUndoCommand):
    
    """Update name of storage name."""
    
    def __init__(self, name: str, widget: QLineEdit):
        super(AddStorageName, self).__init__()
        self.name = name
        self.widget = widget
    
    def redo(self):
        """Set the name text."""
        self.widget.setText(self.name)
    
    def undo(self):
        """Clear the name text."""
        self.widget.clear()


class ClearStorageName(QUndoCommand):
    
    """Clear the storage name"""
    
    def __init__(self, widget: QLineEdit):
        super(ClearStorageName, self).__init__()
        self.name = widget.text() or widget.placeholderText()
        self.widget = widget
    
    def redo(self):
        """Clear name text."""
        self.widget.clear()
    
    def undo(self):
        """Set the name text."""
        self.widget.setText(self.name)


class AddVariable(QUndoCommand):
    
    """Add a variable to list widget."""
    
    def __init__(self, text: str, widget: QListWidget):
        super(AddVariable, self).__init__()
        self.item = QListWidgetItem(text)
        self.item.setToolTip(text)
        self.widget = widget
    
    def redo(self):
        """Add to widget."""
        self.widget.addItem(self.item)
    
    def undo(self):
        """Take out the item."""
        self.widget.takeItem(self.widget.row(self.item))


class DeleteVariable(QUndoCommand):
    
    """Remove the variable item."""
    
    def __init__(self, row: int, widget: QListWidget):
        super(DeleteVariable, self).__init__()
        self.item = widget.item(row)
        self.widget = widget
    
    def redo(self):
        """Take out the item."""
        self.widget.takeItem(self.widget.row(self.item))
    
    def undo(self):
        """Add to widget."""
        self.widget.addItem(self.item)
