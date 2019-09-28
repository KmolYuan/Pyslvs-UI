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
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Sequence,
    List,
    Dict,
    Tuple,
    Iterator,
    Iterable,
    Union,
    Optional,
)
from abc import abstractmethod
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QUndoCommand,
    QTableWidgetItem,
    QListWidget,
    QListWidgetItem,
    QLineEdit,
    QWidget,
)
from qtpy.QtGui import QIcon, QPixmap
from pyslvs import VJoint, VPoint, VLink, color_rgb
from pyslvs_ui.core.qt_patch import QABCMeta
from .tables import (
    BaseTableWidget,
    PointTableWidget,
    LinkTableWidget,
)

_Path = Sequence[Tuple[float, float]]
_ITEM_FLAGS = Qt.ItemIsSelectable | Qt.ItemIsEnabled


def _no_empty(str_list: Union[List[str], Iterator[str]]) -> Iterator[str]:
    """Filter to exclude empty string."""
    yield from (s for s in str_list if s)


def _args2vpoint(args: Sequence[Union[str, float]]) -> Optional[VPoint]:
    """Make arguments as a VPoint object."""
    link = _no_empty(args[0].split(','))
    if args[1] == '':
        return None
    elif args[1] == 'R':
        type_int = VJoint.R
        angle = 0
    else:
        t, angle_str = args[1].split(':')
        angle = float(angle_str)
        if t == 'P':
            type_int = VJoint.P
        else:
            type_int = VJoint.RP
    return VPoint(link, type_int, angle, args[2], args[3], args[4], color_rgb)


def _args2vlink(args: Sequence[str]) -> Optional[VLink]:
    """Make arguments as a VLink object."""
    if args[0] == '':
        return None
    points = [int(p.replace('Point', '')) for p in _no_empty(args[2].split(','))]
    return VLink(args[0], args[1], points, color_rgb)


class _FusedTable(QUndoCommand, metaclass=QABCMeta):

    """Table command of fused type."""

    @abstractmethod
    def __init__(
        self,
        entities_list: List[Union[VPoint, VLink, None]],
        table: BaseTableWidget,
        parent: Optional[QWidget] = None
    ):
        super(_FusedTable, self).__init__(parent)
        self.entities_list = entities_list
        self.table = table
        self.table_type = type(table)


class AddTable(_FusedTable):

    """Add a row at last of the table."""

    def __init__(
        self,
        entities_list: List[Union[VPoint, VLink, None]],
        table: BaseTableWidget,
        parent: Optional[QWidget] = None
    ):
        """Attributes

        + Table reference
        """
        super(AddTable, self).__init__(entities_list, table, parent)

    def redo(self) -> None:
        """Add a empty row and add empty text strings into table items."""
        self.entities_list.append(None)
        row = self.table.rowCount()
        self.table.insertRow(row)
        for column in range(row):
            self.table.setItem(row, column, QTableWidgetItem(''))

    def undo(self) -> None:
        """Remove the last row directly."""
        self.table.removeRow(self.table.rowCount() - 1)
        self.entities_list.pop()


class DeleteTable(_FusedTable):

    """Delete the specified row of table.

    !!! When this class has been called, the item must be empty.
    """

    def __init__(
        self,
        row: int,
        entities_list: List[Union[VPoint, VLink, None]],
        table: BaseTableWidget,
        is_rename: bool,
        parent: Optional[QWidget] = None
    ):
        """Attributes

        + Table reference
        + Row
        + Should rename
        """
        super(DeleteTable, self).__init__(entities_list, table, parent)
        self.row = row
        self.is_rename = is_rename

    def redo(self) -> None:
        """Remove the row and rename sequence."""
        self.entities_list.pop(self.row)
        self.table.removeRow(self.row)
        if self.is_rename:
            self.table.rename(self.row)

    def undo(self) -> None:
        """Rename again then insert a empty row."""
        if self.is_rename:
            self.table.rename(self.row)
        self.entities_list.insert(self.row, None)
        self.table.insertRow(self.row)
        for column in range(self.table.columnCount()):
            self.table.setItem(self.row, column, QTableWidgetItem(''))


class FixSequenceNumber(QUndoCommand):

    """Fix sequence number when deleting a point."""

    def __init__(
        self,
        vlink_list: List[VLink],
        link_table: LinkTableWidget,
        row: int,
        benchmark: int,
        parent: Optional[QWidget] = None
    ):
        """Attributes

        + Table reference
        + Row
        + Benchmark
        """
        super(FixSequenceNumber, self).__init__(parent)
        self.link_table = link_table
        self.vlink_list = vlink_list
        self.row = row
        self.benchmark = benchmark

    def redo(self) -> None:
        self.__sorting(True)

    def undo(self) -> None:
        self.__sorting(False)

    def __sorting(self, benchmark: bool) -> None:
        """Sorting point number by benchmark."""
        vlink = self.vlink_list[self.row]
        if not vlink.points:
            return
        points = list(vlink.points)
        if benchmark:
            points = [p - 1 if p > self.benchmark else p for p in points]
        else:
            points = [p + 1 if p >= self.benchmark else p for p in points]
        vlink.set_points(points)
        item = self.link_table.item(self.row, 2)
        item.setText(','.join([f'Point{p}' for p in points]))


class _EditFusedTable(QUndoCommand, metaclass=QABCMeta):

    """Edit table command of fused type."""

    @abstractmethod
    def __init__(
        self,
        row: int,
        vpoint_list: List[VPoint],
        vlink_list: List[VLink],
        point_table: PointTableWidget,
        link_table: LinkTableWidget,
        args_list: Sequence[Union[str, float]],
        parent: Optional[QWidget] = None
    ):
        super(_EditFusedTable, self).__init__(parent)
        self.row = row
        self.vpoint_list = vpoint_list
        self.vlink_list = vlink_list
        self.point_table = point_table
        self.link_table = link_table
        self.args = tuple(args_list)


class EditPointTable(_EditFusedTable):

    """Edit Point table.

    Copy old data and put it back when called undo.
    """

    def __init__(self, row: int, *args) -> None:
        super(EditPointTable, self).__init__(row, *args)
        self.old_args = self.point_table.row_data(row)
        # Links: Set[str]
        new_links = set(self.args[0].split(','))
        old_links = set(self.old_args[0].split(','))
        new_link_items = []
        old_link_items = []
        for row, vlink in enumerate(self.vlink_list):
            name = '' if vlink is None else vlink.name
            if name in (new_links - old_links):
                new_link_items.append(row)
            if name in (old_links - new_links):
                old_link_items.append(row)
        self.new_link_items = tuple(new_link_items)
        self.old_link_items = tuple(old_link_items)

    def redo(self) -> None:
        """Write arguments then rewrite the dependents."""
        self.vpoint_list[self.row] = _args2vpoint(self.args)
        self.point_table.edit_point(self.row, *self.args)
        self.__write_links(self.new_link_items, self.old_link_items)

    def undo(self) -> None:
        """Rewrite the dependents then write arguments."""
        self.__write_links(self.old_link_items, self.new_link_items)
        self.point_table.edit_point(self.row, *self.old_args)
        self.vpoint_list[self.row] = _args2vpoint(self.old_args)

    def __write_links(self, add: Sequence[int], sub: Sequence[int]) -> None:
        """Write table function.

        + Append the point that relate with these links.
        + Remove the point that irrelevant with these links.
        """
        for row in add:
            new_points = list(self.vlink_list[row].points)
            new_points.append(self.row)
            self.__set_cell(row, new_points)
        for row in sub:
            new_points = list(self.vlink_list[row].points)
            new_points.remove(self.row)
            self.__set_cell(row, new_points)

    def __set_cell(self, row: int, points: Iterable[int]) -> None:
        item = QTableWidgetItem(','.join(f'Point{p}' for p in points))
        item.setFlags(_ITEM_FLAGS)
        self.link_table.setItem(row, 2, item)
        self.vlink_list[row].set_points(points)


class EditLinkTable(_EditFusedTable):

    """Edit Link table.

    Copy old data and put it back when called undo.
    """

    def __init__(self, row: int, *args) -> None:
        super(EditLinkTable, self).__init__(row, *args)
        self.old_args = self.link_table.row_data(row)
        # Points: Set[int]
        new_points = {
            int(index.replace('Point', ''))
            for index in _no_empty(self.args[2].split(','))
        }
        old_points = {
            int(index.replace('Point', ''))
            for index in _no_empty(self.old_args[2].split(','))
        }
        self.new_point_items = tuple(new_points - old_points)
        self.old_point_items = tuple(old_points - new_points)

    def redo(self) -> None:
        """Write arguments then rewrite the dependents."""
        self.vlink_list[self.row] = _args2vlink(self.args)
        self.link_table.edit_link(self.row, *self.args)
        self.__rename(self.args[0], self.old_args)
        self.__write_points(self.args[0], self.new_point_items, self.old_point_items)

    def undo(self) -> None:
        """Rewrite the dependents then write arguments."""
        self.__write_points(self.old_args[0], self.old_point_items, self.new_point_items)
        self.__rename(self.old_args[0], self.args)
        self.link_table.edit_link(self.row, *self.old_args)
        self.vlink_list[self.row] = _args2vlink(self.old_args)

    def __rename(self, new_name: str, args: Sequence[str]) -> None:
        """Adjust link name in all dependents, if link name are changed."""
        if args[0] == new_name:
            return
        for index in _no_empty(args[2].split(',')):
            row = int(index.replace('Point', ''))
            item = QTableWidgetItem(','.join(
                link.replace(args[0], new_name)
                for link in self.vpoint_list[row].links
            ))
            item.setFlags(_ITEM_FLAGS)
            self.point_table.setItem(row, 1, item)
            self.vpoint_list[row].replace_link(args[0], new_name)

    def __write_points(self, name: str, add: Sequence[int], sub: Sequence[int]) -> None:
        """Write table function.

        + Append the link that relate with these points.
        + Remove the link that irrelevant with these points.
        """
        for row in add:
            new_links = list(self.vpoint_list[row].links)
            new_links.append(name)
            self.__set_cell(row, new_links)
        for row in sub:
            new_links = list(self.vpoint_list[row].links)
            if name:
                new_links.remove(name)
            self.__set_cell(row, new_links)

    def __set_cell(self, row: int, links: Iterable[str]) -> None:
        item = QTableWidgetItem(','.join(links))
        item.setFlags(_ITEM_FLAGS)
        self.point_table.setItem(row, 1, item)
        self.vpoint_list[row].set_links(links)


class AddPath(QUndoCommand):

    """Append a new path."""

    def __init__(
        self,
        widget: QListWidget,
        name: str,
        data: Dict[str, _Path],
        path: _Path,
        parent: Optional[QWidget] = None
    ) -> None:
        super(AddPath, self).__init__(parent)
        self.setText(f"Add {{Path: {name}}}")
        self.widget = widget
        self.name = name
        self.data = data
        self.path = path
        self.targets = [i for i, d in enumerate(self.path) if len(set(d)) > 1]

    def redo(self) -> None:
        """Add new path data."""
        self.data[self.name] = self.path
        self.widget.addItem(f"{self.name}: " + ", ".join(f"[{i}]" for i in self.targets))

    def undo(self) -> None:
        """Remove the last item."""
        self.widget.takeItem(self.widget.count() - 1)
        self.data.pop(self.name)


class DeletePath(QUndoCommand):

    """"Delete the specified row of path."""

    def __init__(
        self,
        row: int,
        widget: QListWidget,
        data: Dict[str, _Path],
        parent: Optional[QWidget] = None
    ) -> None:
        super(DeletePath, self).__init__(parent)
        self.setText(f"Delete {{Path: {widget.item(row).text()}}}")
        self.row = row
        self.widget = widget
        self.data = data
        self.old_item = self.widget.item(self.row)
        self.name = self.old_item.text().split(':')[0]
        self.old_path = self.data[self.name]

    def redo(self) -> None:
        """Delete the path."""
        self.widget.takeItem(self.row)
        self.data.pop(self.name)

    def undo(self) -> None:
        """Append back the path."""
        self.data[self.old_item.text().split(':')[0]] = self.old_path
        self.widget.addItem(self.old_item)
        self.widget.setCurrentRow(self.widget.row(self.old_item))


class AddStorage(QUndoCommand):

    """Append a new storage."""

    def __init__(
        self,
        name: str,
        widget: QListWidget,
        mechanism: str,
        parent: Optional[QWidget] = None
    ) -> None:
        super(AddStorage, self).__init__(parent)
        self.setText(f"Add {{Mechanism: {name}}}")
        self.name = name
        self.widget = widget
        self.mechanism = mechanism

    def redo(self) -> None:
        """Add mechanism expression to 'expr' attribute."""
        item = QListWidgetItem(self.name)
        item.expr = self.mechanism
        item.setIcon(QIcon(QPixmap(":/icons/mechanism.png")))
        self.widget.addItem(item)

    def undo(self) -> None:
        """Remove the last item."""
        self.widget.takeItem(self.widget.count() - 1)


class DeleteStorage(QUndoCommand):

    """Delete the specified row of storage."""

    def __init__(
        self,
        row: int,
        widget: QListWidget,
        parent: Optional[QWidget] = None
    ) -> None:
        super(DeleteStorage, self).__init__(parent)
        self.setText(f"Delete {{Mechanism: {widget.item(row).text()}}}")
        self.row = row
        self.widget = widget
        self.name = widget.item(row).text()
        self.mechanism = widget.item(row).expr

    def redo(self) -> None:
        """Remove the row directly."""
        self.widget.takeItem(self.row)

    def undo(self) -> None:
        """Create a new item and recover expression."""
        item = QListWidgetItem(self.name)
        item.expr = self.mechanism
        item.setIcon(QIcon(QPixmap(":/icons/mechanism.png")))
        self.widget.insertItem(self.row, item)


class AddStorageName(QUndoCommand):

    """Update name of storage name."""

    def __init__(
        self,
        name: str,
        widget: QLineEdit,
        parent: Optional[QWidget] = None
    ) -> None:
        super(AddStorageName, self).__init__(parent)
        self.name = name
        self.widget = widget

    def redo(self) -> None:
        """Set the name text."""
        self.widget.setText(self.name)

    def undo(self) -> None:
        """Clear the name text."""
        self.widget.clear()


class ClearStorageName(QUndoCommand):

    """Clear the storage name"""

    def __init__(self, widget: QLineEdit, parent: Optional[QWidget] = None) -> None:
        super(ClearStorageName, self).__init__(parent)
        self.name = widget.text() or widget.placeholderText()
        self.widget = widget

    def redo(self) -> None:
        """Clear name text."""
        self.widget.clear()

    def undo(self) -> None:
        """Set the name text."""
        self.widget.setText(self.name)


class AddInput(QUndoCommand):

    """Add a variable to list widget."""

    def __init__(
        self,
        name: str,
        widget: QListWidget,
        parent: Optional[QWidget] = None
    ) -> None:
        super(AddInput, self).__init__(parent)
        self.setText(f"Add variable of {name}")
        self.item = QListWidgetItem(name)
        self.item.setToolTip(name)
        self.widget = widget

    def redo(self) -> None:
        """Add to widget."""
        self.widget.addItem(self.item)

    def undo(self) -> None:
        """Take out the item."""
        self.widget.takeItem(self.widget.row(self.item))


class DeleteInput(QUndoCommand):

    """Remove the variable item."""

    def __init__(
        self,
        row: int,
        widget: QListWidget,
        parent: Optional[QWidget] = None
    ) -> None:
        super(DeleteInput, self).__init__(parent)
        self.setText(f"Remove variable of {{Point{row}}}")
        self.item = widget.item(row)
        self.widget = widget

    def redo(self) -> None:
        """Take out the item."""
        self.widget.takeItem(self.widget.row(self.item))

    def undo(self) -> None:
        """Add to widget."""
        self.widget.addItem(self.item)
