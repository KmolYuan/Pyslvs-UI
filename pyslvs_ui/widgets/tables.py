# -*- coding: utf-8 -*-

"""Custom table of Points and Links.
Also contains selection status label.
"""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from abc import abstractmethod
from dataclasses import astuple
from time import process_time
from typing import (
    TYPE_CHECKING, Tuple, List, Iterator, Sequence, Union, Optional,
    TypeVar, Generic,
)
from qtpy.QtCore import Signal, Qt, QTimer, Slot
from qtpy.QtWidgets import (
    QTableWidget,
    QSizePolicy,
    QAbstractItemView,
    QTableWidgetItem,
    QApplication,
    QTableWidgetSelectionRange,
    QHeaderView,
    QLabel,
    QWidget,
)
from qtpy.QtGui import QKeyEvent
from pyslvs import EStack, VPoint, VLink, PointArgs, LinkArgs
from pyslvs_ui.qt_patch import QABCMeta
from pyslvs_ui.graphics import color_icon

if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase

_Data = TypeVar('_Data', VPoint, VLink)
_Coord = Tuple[float, float]


class BaseTableWidget(QTableWidget, Generic[_Data], metaclass=QABCMeta):
    """Two tables has some shared function."""
    headers: Sequence[str] = ()

    row_selection_changed = Signal(list)
    delete_request = Signal()

    @abstractmethod
    def __init__(self, row: int, parent: QWidget):
        super(BaseTableWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setStatusTip("This table will show about the entities items in "
                          "current view mode.")
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.setRowCount(row)
        self.setColumnCount(len(self.headers))
        for i, e in enumerate(self.headers):
            self.setHorizontalHeaderItem(i, QTableWidgetItem(e))

        # Table widget column width
        header = self.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        @Slot()
        def emit_selection_changed() -> None:
            self.row_selection_changed.emit(self.selected_rows())

        self.itemSelectionChanged.connect(emit_selection_changed)

    def row_text(self, row: int, *, has_name: bool) -> List[str]:
        """Get the whole row of texts.

        + Edit point: has_name = False
        + Edit link: has_name = True
        """
        texts = []
        for column in self.effective_range(has_name):
            item = self.item(row, column)
            if item is None:
                texts.append('')
            else:
                texts.append(item.text())
        return texts

    @abstractmethod
    def effective_range(self, has_name: bool) -> Iterator[int]:
        """Return valid column range for row text."""
        raise NotImplementedError

    def selected_rows(self) -> List[int]:
        """Get what row is been selected."""
        return [row for row in range(self.rowCount())
                if self.item(row, 0).isSelected()]

    def selectAll(self) -> None:
        """Override method of select all function."""
        self.setFocus(Qt.ShortcutFocusReason)
        super(BaseTableWidget, self).selectAll()

    def set_selections(self, selections: Sequence[int],
                       key_detect: bool = False) -> None:
        """Auto select function, get the signal from canvas."""
        self.setFocus()
        keyboard_modifiers = QApplication.keyboardModifiers()
        if key_detect:
            if keyboard_modifiers == Qt.ShiftModifier:
                continue_select = True
                not_select = False
            elif keyboard_modifiers == Qt.ControlModifier:
                continue_select = True
                not_select = True
            else:
                continue_select = False
                not_select = False
            self.__set_selected_ranges(
                selections,
                is_continue=continue_select,
                un_select=not_select
            )
        else:
            self.__set_selected_ranges(
                selections,
                is_continue=(keyboard_modifiers == Qt.ShiftModifier),
                un_select=False
            )

    def __set_selected_ranges(
        self,
        selections: Sequence[int],
        *,
        is_continue: bool,
        un_select: bool
    ):
        """Different mode of select function."""
        selected_rows = self.selected_rows()
        if not is_continue:
            self.clearSelection()
        self.setCurrentCell(selections[-1], 0)
        for row in selections:
            is_selected = (row not in selected_rows) if un_select else True
            self.setRangeSelected(
                QTableWidgetSelectionRange(row, 0, row, self.columnCount() - 1),
                is_selected
            )
            self.scrollToItem(self.item(row, 0))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Hit the delete key,
        will emit delete signal from this table.
        """
        if event.key() == Qt.Key_Delete:
            self.delete_request.emit()

    def clear(self) -> None:
        """Overridden the clear function, just removed all items."""
        for row in range(self.rowCount()):
            self.removeRow(0)

    @Slot()
    def clearSelection(self) -> None:
        """Overridden the 'clear_selection' slot to emit
        'row_selection_changed'"""
        super(BaseTableWidget, self).clearSelection()
        self.row_selection_changed.emit([])


class PointTableWidget(BaseTableWidget[VPoint]):
    """Custom table widget for points."""
    headers = ('Number', 'Links', 'Type', 'Color', 'X', 'Y', 'Current')
    selectionLabelUpdate = Signal(list)

    def __init__(self, parent: QWidget):
        super(PointTableWidget, self).__init__(0, parent)

    def edit_point(self, row: int, arg: PointArgs) -> None:
        """Edit a point."""
        for i, e in enumerate((f'Point{row}',)
                              + astuple(arg)
                              + (f"({arg.x}, {arg.y})",)):
            item = QTableWidgetItem(str(e))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i == 3:
                item.setIcon(color_icon(e))
            self.setItem(row, i, item)

    def row_data(self, row: int) -> PointArgs:
        """Return row data for 'edit_point' method."""
        args = self.row_text(row, has_name=False)
        x = float(args[3]) if args[3] else 0.
        y = float(args[4]) if args[4] else 0.
        return PointArgs(args[0], args[1], args[2], x, y)

    def rename(self, row: int) -> None:
        """When index changed, the points need to rename."""
        for j in range(row, self.rowCount()):
            self.setItem(j, 0, QTableWidgetItem(f'Point{j}'))

    def current_position(self, row: int) -> List[_Coord]:
        """Get the current coordinate from a point."""
        type_str = self.item(row, 2).text().split(':')
        coords_text = self.item(row, 6).text().replace(';', ',')
        coords = eval(f"[{coords_text}]")
        if (type_str[0] in {'P', 'RP'}) and len(coords) == 1:
            x, y = coords[0]
            self.item(row, 6).setText("; ".join([f"({x:.06f}, {y:.06f})"] * 2))
            coords.append(coords[0])
        return coords

    def update_current_position(
        self,
        coords: Sequence[Union[_Coord, Tuple[_Coord, _Coord]]]
    ) -> None:
        """Update the current coordinate for a point."""
        for i, c in enumerate(coords):
            if isinstance(c[0], float):
                x, y = c
                text = f"({x:.06f}, {y:.06f})"
            else:
                (x1, y1), (x2, y2) = c
                text = f"({x1:.06f}, {y1:.06f}); ({x2:.06f}, {y2:.06f})"
            item = QTableWidgetItem(text)
            item.setToolTip(text)
            self.setItem(i, 6, item)

    def get_back_position(self) -> None:
        """Let all the points go back to origin coordinate."""
        self.update_current_position(tuple(
            (float(self.item(row, 4).text()), float(self.item(row, 5).text()))
            for row in range(self.rowCount())
        ))

    def get_links(self, row: int) -> List[str]:
        item = self.item(row, 1)
        if not item:
            return []
        return [s for s in item.text().split(',') if s]

    def set_selections(self, selections: Sequence[int],
                       key_detect: bool = False) -> None:
        """Need to update selection label on status bar."""
        super(PointTableWidget, self).set_selections(selections, key_detect)
        self.selectionLabelUpdate.emit(self.selected_rows())

    def effective_range(self, has_name: bool) -> Iterator[int]:
        """Row range that can be delete."""
        if has_name:
            yield from range(self.columnCount())
        else:
            yield from range(1, self.columnCount() - 1)

    @Slot()
    def clearSelection(self) -> None:
        """Overridden the 'clear_selection' slot,
        so it will emit signal to clean the selection.
        """
        super(PointTableWidget, self).clearSelection()
        self.selectionLabelUpdate.emit([])


class LinkTableWidget(BaseTableWidget[VLink]):
    """Custom table widget for link."""
    headers = ('Name', 'Color', 'Points')

    def __init__(self, parent: QWidget):
        super(LinkTableWidget, self).__init__(1, parent)
        self.setDragDropMode(QAbstractItemView.DropOnly)
        self.setAcceptDrops(True)
        self.edit_link(0, LinkArgs(VLink.FRAME, 'White', ''))

    def edit_link(self, row: int, arg: LinkArgs):
        """Edit a link."""
        for i, e in enumerate(astuple(arg)):
            item = QTableWidgetItem(e)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if i == 1:
                item.setIcon(color_icon(e))
            self.setItem(row, i, item)

    def row_data(self, row: int) -> LinkArgs:
        """Return row data for 'edit_link' method."""
        return LinkArgs(*self.row_text(row, has_name=True))

    def find_name(self, name: str) -> int:
        """Return row index by input name."""
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if not item:
                continue
            if name == item.text():
                return row
        return -1

    def get_points(self, row: int) -> List[int]:
        """Get all point names."""
        item = self.item(row, 2)
        if not item:
            return []
        link_str = item.text()
        return [int(s.replace('Point', '')) for s in link_str.split(',') if s]

    def effective_range(self, has_name: bool) -> Iterator[int]:
        """Row range that can be delete."""
        yield from range(self.columnCount())

    def clear(self) -> None:
        """We should keep the frame left."""
        super(LinkTableWidget, self).clear()
        self.setRowCount(1)
        self.edit_link(0, LinkArgs(VLink.FRAME, 'White', ''))


class ExprTableWidget(BaseTableWidget):
    """Expression table.

    + Free move request: link name, length
    """
    exprs: List[Tuple[str, ...]]

    headers = ('Function', 'p0', 'p1', 'p2', 'p3', 'p4', 'target')

    def __init__(self, parent: QWidget):
        super(ExprTableWidget, self).__init__(0, parent)
        self.exprs = []

    def set_expr(self, es: EStack, unsolved: Sequence[int]):
        """Set the table items for new coming expression."""
        exprs = es.as_list()
        if exprs != self.exprs:
            self.clear()
            self.setRowCount(len(exprs) + len(unsolved))
        row = 0
        for expr in exprs:
            # Target
            self.setItem(row, self.columnCount() - 1,
                         QTableWidgetItem(expr[-1]))
            # Parameters
            for column, text in enumerate(expr[:-1]):
                item = QTableWidgetItem(text)
                item.setToolTip(text)
                self.setItem(row, column, item)
            row += 1
        for p in unsolved:
            # Declaration
            self.setItem(row, 0, QTableWidgetItem("Unsolved"))
            # Target
            self.setItem(row, self.columnCount() - 1, QTableWidgetItem(f"P{p}"))
            row += 1
        self.exprs = exprs

    def effective_range(self, has_name: bool) -> Iterator[int]:
        """Return column count."""
        yield from range(self.columnCount())

    def clear(self) -> None:
        """Emit to close the link free move widget."""
        super(ExprTableWidget, self).clear()


class SelectionLabel(QLabel):
    """This QLabel can show distance in status bar."""

    def __init__(self, parent: MainWindowBase):
        super(SelectionLabel, self).__init__(parent)
        self.update_select_point()
        self.vpoints = parent.vpoint_list

    @Slot()
    @Slot(list)
    def update_select_point(self, points: Optional[List[int]] = None) -> None:
        """Get points and distance from Point table widget."""
        if points is None:
            points = []
        p_count = len(points)
        if not p_count:
            self.setText("No selection.")
            return
        text = "Selected: "
        text += " - ".join(str(p) for p in points)
        if p_count > 1:
            distances = []
            angles = []
            for i in range(min(p_count, 3)):
                if i == 0:
                    continue
                vpoint0 = self.vpoints[points[i - 1]]
                vpoint1 = self.vpoints[points[i]]
                distances.append(f"{vpoint1.distance(vpoint0):.06}")
                angles.append(f"{vpoint0.slope_angle(vpoint1):.06}°")
            ds_t = ", ".join(distances)
            as_t = ", ".join(angles)
            text += f" | {ds_t} | {as_t}"
        self.setText(text)

    @Slot(float, float)
    def update_mouse_position(self, x: float, y: float) -> None:
        """Get the mouse position from canvas when press the middle button."""
        self.setText(f"Mouse at: ({x:.04f}, {y:.04f})")


class FPSLabel(QLabel):
    """This QLabel can show FPS of main canvas in status bar."""

    def __init__(self, parent: QWidget):
        super(FPSLabel, self).__init__(parent)
        self.__t0 = process_time()
        self.__frame_timer = QTimer()
        self.__frame_timer.timeout.connect(self.__update_text)
        self.__frame_timer.start(1000)

    @Slot()
    def __update_text(self) -> None:
        """Update FPS with timer."""
        t1 = process_time() - self.__t0
        fps = 1 / t1 if t1 else 1
        self.setText(f"FPS: {fps:6.02f}")

    @Slot()
    def update_text(self) -> None:
        """Update FPS with timer."""
        self.__update_text()
        self.__t0 = process_time()
