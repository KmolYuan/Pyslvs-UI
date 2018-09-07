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
        """Add a empty row and add empty text strings into table items."""
        row = self.table.rowCount()
        self.table.insertRow(row)
        for column in range(row):
            self.table.setItem(row, column, QTableWidgetItem(''))
    
    def undo(self):
        """Remove the last row directly."""
        self.table.removeRow(self.table.rowCount() - 1)


class DeleteTable(QUndoCommand):
    
    """Delete the specified row of table.
    
    When this class has been called, the items should be empty.
    """
    
    def __init__(self, row: int, table: QTableWidget, is_rename: bool):
        """Attributes
        
        + Table reference
        + Row
        + Should rename
        """
        super(DeleteTable, self).__init__()
        self.table = table
        self.row = row
        self.is_rename = is_rename
    
    def redo(self):
        """Remove the row and rename sequence."""
        self.table.removeRow(self.row)
        if self.is_rename:
            self.table.rename(self.row)
    
    def undo(self):
        """Rename again then insert a empty row."""
        if self.is_rename:
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
        self.__sorting(True)
    
    def undo(self):
        self.__sorting(False)
    
    def __sorting(self, bs: bool):
        """Sorting point number by benchmark."""
        item = self.table.item(self.row, 2)
        if not item.text():
            return
        points = [int(p.replace('Point', '')) for p in item.text().split(',')]
        if bs:
            points = [p - 1 if p > self.benchmark else p for p in points]
        else:
            points = [p + 1 if p >= self.benchmark else p for p in points]
        item.setText(','.join([f'Point{p}' for p in points]))


class EditPointTable(QUndoCommand):
    
    """Edit Point table.
    
    Copy old data and put it back when called undo.
    """
    
    def __init__(
        self,
        row: int,
        point_table: QTableWidgetItem,
        link_table: QTableWidgetItem,
        args: Sequence[Union[str, int, float]]
    ):
        super(EditPointTable, self).__init__()
        self.point_table = point_table
        self.row = row
        self.link_table = link_table
        self.args = tuple(args)
        self.old_args: str = self.point_table.rowTexts(row)
        # Tuple[str] -> Set[str]
        new_links = set(self.args[0].split(','))
        old_links = set(self.old_args[0].split(','))
        self.new_link_items = []
        self.old_link_items = []
        for row in range(self.link_table.rowCount()):
            link_name = self.link_table.item(row, 0).text()
            if link_name in (new_links - old_links):
                self.new_link_items.append(row)
            if link_name in (old_links - new_links):
                self.old_link_items.append(row)
        self.new_link_items = tuple(self.new_link_items)
        self.old_link_items = tuple(self.old_link_items)
    
    def redo(self):
        """Write arguments then rewrite the dependents."""
        self.point_table.editArgs(self.row, *self.args)
        self.__writeRows(self.new_link_items, self.old_link_items)
    
    def undo(self):
        """Rewrite the dependents then write arguments."""
        self.__writeRows(self.old_link_items, self.new_link_items)
        self.point_table.editArgs(self.row, *self.old_args)
    
    def __writeRows(
        self,
        items1: Sequence[int],
        items2: Sequence[int]
    ):
        """Write table function.
        
        + Append the point that relate with these links.
        + Remove the point that irrelevant with these links.
        """
        point_name = f'Point{self.row}'
        for row in items1:
            new_points = self.link_table.item(row, 2).text().split(',')
            new_points.append(point_name)
            self.__setCell(row, new_points)
        for row in items2:
            new_points = self.link_table.item(row, 2).text().split(',')
            new_points.remove(point_name)
            self.__setCell(row, new_points)
    
    def __setCell(self, row: int, points: List[str]):
        item = QTableWidgetItem(','.join(_noNoneString(points)))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.link_table.setItem(row, 2, item)


class EditLinkTable(QUndoCommand):
    
    """Edit Link table.
    
    Copy old data and put it back when called undo.
    """
    
    def __init__(
        self,
        row: int,
        link_table: QTableWidgetItem,
        point_table: QTableWidgetItem,
        args: Sequence[str]
    ):
        super(EditLinkTable, self).__init__()
        self.link_table = link_table
        self.row = row
        self.point_table = point_table
        self.args = tuple(args)
        self.old_args = self.link_table.rowTexts(row, has_name=True)
        # Points: Tuple[int]
        new_points = self.args[2].split(',')
        old_points = self.old_args[2].split(',')
        new_points = set(
            int(index.replace('Point', ''))
            for index in _noNoneString(new_points)
        )
        old_points = set(
            int(index.replace('Point', ''))
            for index in _noNoneString(old_points)
        )
        self.new_point_items = tuple(new_points - old_points)
        self.old_point_items = tuple(old_points - new_points)
    
    def redo(self):
        """Write arguments then rewrite the dependents."""
        self.link_table.editArgs(self.row, *self.args)
        self.__rename(self.args, self.old_args)
        self.__writeRows(self.args[0], self.new_point_items, self.old_point_items)
    
    def undo(self):
        """Rewrite the dependents then write arguments."""
        self.__writeRows(self.old_args[0], self.old_point_items, self.new_point_items)
        self.__rename(self.old_args, self.args)
        self.link_table.editArgs(self.row, *self.old_args)
    
    def __rename(self, arg1: Tuple[str, ...], arg2: Tuple[str, ...]):
        """Adjust link name in all dependents,
        if link name are changed.
        """
        if arg2[0] == arg1[0]:
            return
        for index in _noNoneString(arg2[2].split(',')):
            row = int(index.replace('Point', ''))
            new_links = self.point_table.item(row, 1).text().split(',')
            item = QTableWidgetItem(','.join(_noNoneString(
                w.replace(arg2[0], arg1[0])
                for w in new_links
            )))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.point_table.setItem(row, 1, item)
    
    def __writeRows(
        self,
        name: str,
        items1: Sequence[int],
        items2: Sequence[int]
    ):
        """Write table function.
        
        + Append the link that relate with these points.
        + Remove the link that irrelevant with these points.
        """
        for row in items1:
            new_links = self.point_table.item(row, 1).text().split(',')
            new_links.append(name)
            self.__setCell(row, new_links)
        for row in items2:
            new_links = self.point_table.item(row, 1).text().split(',')
            if name:
                new_links.remove(name)
            self.__setCell(row, new_links)
    
    def __setCell(self, row: int, links: List[str]):
        item = QTableWidgetItem(','.join(_noNoneString(links)))
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.point_table.setItem(row, 1, item)


class AddPath(QUndoCommand):
    
    """Append a new path."""
    
    def __init__(
        self,
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
        self.widget.addItem(f"{self.name}: " + ", ".join(
            f"[{i}]" for i, d in enumerate(self.path) if d
        ))
    
    def undo(self):
        """Remove the last item."""
        self.widget.takeItem(self.widget.count()-1)
        del self.data[self.name]


class DeletePath(QUndoCommand):
    
    """"Delete the specified row of path."""
    
    def __init__(self, row: int, widget: QListWidget, data: List[Tuple[float, float]]):
        super(DeletePath, self).__init__()
        self.row = row
        self.widget = widget
        self.data = data
        self.old_item = self.widget.item(self.row)
        self.name = self.old_item.text().split(':')[0]
        self.old_path = self.data[self.name]

    def redo(self):
        """Delete the path."""
        self.widget.takeItem(self.row)
        del self.data[self.name]
    
    def undo(self):
        """Append back the path."""
        self.data[self.old_item.text().split(':')[0]] = self.old_path
        self.widget.addItem(self.old_item)
        self.widget.setCurrentRow(self.widget.row(self.old_item))


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
