# -*- coding: utf-8 -*-

"""This module contain the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    List,
    Sequence,
    Dict,
    Union,
    Optional,
)
from abc import ABC, abstractmethod
from math import hypot
from itertools import chain
from core.QtModules import (
    Slot,
    QDialogButtonBox,
    QDialog,
    QDoubleSpinBox,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)
from core.entities import (
    EditPointDialog,
    EditLinkDialog,
)
from core.libs import (
    VJoint,
    VPoint,
    VLink,
    expr_solving,
    Graph,
    edges_view,
)
from core.widgets import (
    AddTable,
    DeleteTable,
    EditPointTable,
    EditLinkTable,
    FixSequenceNumber,
)
from core.widgets import MainWindowUiInterface


class _ScaleDialog(QDialog):

    """Scale mechanism dialog."""

    def __init__(self, parent: QWidget):
        super(_ScaleDialog, self).__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.enlarge = QDoubleSpinBox(self)
        self.shrink = QDoubleSpinBox(self)
        self.__add_option("Enlarge", self.enlarge)
        self.__add_option("Shrink", self.shrink)

        button_box = QDialogButtonBox(self)
        button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.main_layout.addWidget(button_box)

    def __add_option(self, name: str, option: QDoubleSpinBox):
        """Add widgets for option."""
        layout = QHBoxLayout(self)
        label = QLabel(name, self)
        option.setValue(1)
        option.setMaximum(10000)
        option.setMinimum(0.01)
        layout.addWidget(label)
        layout.addWidget(option)
        self.main_layout.addLayout(layout)

    def factor(self) -> float:
        """Return scale value."""
        return self.enlarge.value() / self.shrink.value()


class EntitiesMethodInterface(MainWindowUiInterface, ABC):

    """Abstract class for entities methods."""

    def __edit_point(self, row: Union[int, bool] = False):
        """Edit point function."""
        dlg = EditPointDialog(
            self.EntitiesPoint.data_tuple(),
            self.EntitiesLink.data_tuple(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return

        row_count = self.EntitiesPoint.rowCount()
        type_str = dlg.type_box.currentText().split()[0]
        if type_str != 'R':
            type_str += f":{dlg.angle_box.value() % 360}"
        args = (
            ','.join(
                dlg.selected.item(link).text()
                for link in range(dlg.selected.count())
            ),
            type_str,
            dlg.color_box.currentText(),
            dlg.x_box.value(),
            dlg.y_box.value()
        )
        if row is False:
            self.CommandStack.beginMacro(f"Add {{Point{row_count}}}")
            self.CommandStack.push(AddTable(self.EntitiesPoint))
            row = row_count
        else:
            row = dlg.name_box.currentIndex()
            self.CommandStack.beginMacro(f"Edit {{Point{row}}}")
        self.CommandStack.push(EditPointTable(
            row,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        self.CommandStack.endMacro()

    def __edit_link(self, row: Union[int, bool] = False):
        """Edit link function."""
        dlg = EditLinkDialog(
            self.EntitiesPoint.data_tuple(),
            self.EntitiesLink.data_tuple(),
            row,
            self
        )
        dlg.show()
        if not dlg.exec_():
            return
        name = dlg.name_edit.text()
        args = [
            name,
            dlg.color_box.currentText(),
            ','.join(
                dlg.selected.item(point).text()
                for point in range(dlg.selected.count())
            )
        ]
        if row is False:
            self.CommandStack.beginMacro(f"Add {{Link: {name}}}")
            self.CommandStack.push(AddTable(self.EntitiesLink))
            row = self.EntitiesLink.rowCount() - 1
        else:
            row = dlg.name_box.currentIndex()
            self.CommandStack.beginMacro(f"Edit {{Link: {name}}}")
        self.CommandStack.push(EditLinkTable(
            row,
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.endMacro()

    def __get_link_serial_number(self) -> str:
        """Return a new serial number name of link."""
        names = {
            self.EntitiesLink.item(row, 0).text()
            for row in range(self.EntitiesLink.rowCount())
        }
        i = 1
        while f"link_{i}" in names:
            i += 1
        return f"link_{i}"

    @Slot(name='on_action_delete_link_triggered')
    def delete_link(self, row: int):
        """Push delete link command to stack.

        Remove link will not remove the points.
        """
        if not row > 0:
            return
        args = self.EntitiesLink.row_text(row, has_name=True)
        args[2] = ''
        name = self.EntitiesLink.item(row, 0).text()
        self.CommandStack.beginMacro(f"Delete {{Link: {name}}}")
        self.CommandStack.push(EditLinkTable(
            row,
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.push(DeleteTable(
            row,
            self.EntitiesLink,
            is_rename=False
        ))
        self.CommandStack.endMacro()

    @Slot(name='on_action_delete_point_triggered')
    def delete_point(self, row: int):
        """Push delete point command to stack."""
        args = self.EntitiesPoint.row_text(row)
        args[0] = ''
        self.CommandStack.beginMacro(f"Delete {{Point{row}}}")
        for i in reversed([
            i for i, (b, d, a) in enumerate(self.InputsWidget.input_pairs())
            if row in {b, d}
        ]):
            self.InputsWidget.remove_var(i)
        self.CommandStack.push(EditPointTable(
            row,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        for i in range(self.EntitiesLink.rowCount()):
            self.CommandStack.push(FixSequenceNumber(
                self.EntitiesLink,
                i,
                row
            ))
        self.CommandStack.push(DeleteTable(
            row,
            self.EntitiesPoint,
            is_rename=True
        ))
        self.InputsWidget.variable_excluding(row)
        self.CommandStack.endMacro()

    @Slot(float, float)
    def q_add_normal_point(self, x: float, y: float):
        """Add point group using alt key."""
        if self.SynthesisTab.currentIndex() == 2:
            self.add_target_point()
        else:
            self.add_point(x, y)

    def add_normal_point(self):
        """Add a point (not fixed)."""
        self.add_point(self.mouse_pos_x, self.mouse_pos_y)

    def add_fixed_point(self):
        """Add a point (fixed)."""
        self.add_point(self.mouse_pos_x, self.mouse_pos_y, 'ground', 'Blue')

    def add_point(
        self,
        x: float,
        y: float,
        links: str = "",
        color: str = 'Green',
        type_num: int = VJoint.R,
        angle: float = 0.
    ) -> int:
        """Add an ordinary point. Return the row count of new point."""
        row_count = self.EntitiesPoint.rowCount()
        self.CommandStack.beginMacro(f"Add {{Point{row_count}}}")
        self.CommandStack.push(AddTable(self.EntitiesPoint))
        self.CommandStack.push(EditPointTable(
            row_count,
            self.EntitiesPoint,
            self.EntitiesLink,
            (links, ('R', f'P:{angle}', f'RP:{angle}')[type_num], color, x, y)
        ))
        self.CommandStack.endMacro()
        return row_count

    def add_points(self, p_attr: Sequence[Tuple[float, float, str, str, int, float]]):
        """Add multiple points."""
        for attr in p_attr:
            self.add_point(*attr)

    def add_points_by_graph(
        self,
        graph: Graph,
        pos: Dict[int, Tuple[float, float]],
        ground_link: Optional[int]
    ):
        """Add points by NetworkX graph and position dict."""
        base_count = self.EntitiesPoint.rowCount()
        self.CommandStack.beginMacro(
            "Merge mechanism kit from {Number and Type Synthesis}"
        )

        for i in range(len(pos)):
            x, y = pos[i]
            self.add_point(x, y)

        ground: Optional[int] = None
        for link in graph.nodes:
            self.add_link(self.__get_link_serial_number(), 'Blue', [
                base_count + n for n, edge in edges_view(graph) if link in edge
            ])
            if link == ground_link:
                ground = self.EntitiesLink.rowCount() - 1
        self.CommandStack.endMacro()
        if ground_link is not None:
            self.constrain_link(ground)

    @Slot(list)
    def add_normal_link(self, points: Sequence[int]):
        """Add a link."""
        self.add_link(self.__get_link_serial_number(), 'Blue', points)

    def add_link(self, name: str, color: str, points: Optional[Sequence[int]] = None):
        """Push a new link command to stack."""
        if points is None:
            points: List[int] = []
        link_args = [name, color, ','.join(f'Point{i}' for i in points)]
        self.CommandStack.beginMacro(f"Add {{Link: {name}}}")
        self.CommandStack.push(AddTable(self.EntitiesLink))
        self.CommandStack.push(EditLinkTable(
            self.EntitiesLink.rowCount() - 1,
            self.EntitiesLink,
            self.EntitiesPoint,
            link_args
        ))
        self.CommandStack.endMacro()

    def new_point(self):
        """Create a point with arguments."""
        self.__edit_point()

    @Slot(name='on_action_edit_point_triggered')
    def edit_point(self):
        """Edit a point with arguments."""
        row = self.EntitiesPoint.currentRow()
        self.__edit_point(row if (row > -1) else 0)

    def lock_points(self):
        """Turn a group of points to fixed on ground or not."""
        to_fixed = self.action_point_context_lock.isChecked()
        for row in self.EntitiesPoint.selected_rows():
            new_links = self.EntitiesPoint.item(row, 1).text().split(',')
            if to_fixed:
                if 'ground' not in new_links:
                    new_links.append('ground')
            else:
                if 'ground' in new_links:
                    new_links.remove('ground')
            args = self.EntitiesPoint.row_text(row)
            args[0] = ','.join(s for s in new_links if s)
            self.CommandStack.beginMacro(f"Edit {{Point{row}}}")
            self.CommandStack.push(EditPointTable(
                row,
                self.EntitiesPoint,
                self.EntitiesLink,
                args
            ))
            self.CommandStack.endMacro()

    def clone_point(self):
        """Clone a point (with orange color)."""
        row = self.EntitiesPoint.currentRow()
        args = self.EntitiesPoint.row_text(row)
        args[2] = 'Orange'
        row_count = self.EntitiesPoint.rowCount()
        self.CommandStack.beginMacro(f"Clone {{Point{row}}} as {{Point{row_count}}}")
        self.CommandStack.push(AddTable(self.EntitiesPoint))
        self.CommandStack.push(EditPointTable(
            row_count,
            self.EntitiesPoint,
            self.EntitiesLink,
            args
        ))
        self.CommandStack.endMacro()

    @Slot(name="on_action_scale_points_triggered")
    def __set_scale(self):
        """Scale the mechanism."""
        dlg = _ScaleDialog(self)
        if not dlg.exec_():
            return

        factor = dlg.factor()
        self.CommandStack.beginMacro(f"Scale mechanism: {factor}")
        for row in range(self.EntitiesPoint.rowCount()):
            args = self.EntitiesPoint.row_text(row)
            args[3] = float(args[3]) * factor
            args[4] = float(args[4]) * factor
            self.CommandStack.push(EditPointTable(
                row,
                self.EntitiesPoint,
                self.EntitiesLink,
                args
            ))
        self.CommandStack.endMacro()

    @Slot(tuple)
    def set_free_move(
        self,
        args: Sequence[Tuple[int, Tuple[float, float, float]]]
    ):
        """Free move function."""
        points_text = ", ".join(f"Point{c[0]}" for c in args)
        self.CommandStack.beginMacro(f"Moved {{{points_text}}}")
        for row, (x, y, angle) in args:
            args = self.EntitiesPoint.row_text(row)
            args[3] = x
            args[4] = y
            if args[1] != 'R':
                args[1] = f"{args[1].split(':')[0]}:{angle:.02f}"
            self.CommandStack.push(EditPointTable(
                row,
                self.EntitiesPoint,
                self.EntitiesLink,
                args
            ))
        self.CommandStack.endMacro()

    @Slot(int, name='on_link_free_move_base_currentIndexChanged')
    def __reload_adjust_link_base(self, base: int):
        """Set the base and other option."""
        if base == -1:
            return

        self.link_free_move_other.clear()
        vlinks: Tuple[VLink, ...] = self.EntitiesLink.data_tuple()
        for link in self.EntitiesPoint.item_data(base).links:
            if link == 'ground':
                continue
            for i in vlinks[self.EntitiesLink.find_name(link)].points:
                if i == base:
                    continue
                self.link_free_move_other.addItem(f"Point{i}")

    @Slot(name='on_link_free_move_reset_clicked')
    @Slot(int, name='on_link_free_move_other_currentIndexChanged')
    def __reload_adjust_link_other(self, other: Optional[int] = None):
        """Set the link length value."""
        p = self.link_free_move_other.currentText()
        if not p:
            return

        vpoint1 = self.EntitiesPoint.item_data(self.link_free_move_base.currentIndex())
        vpoint2 = self.EntitiesPoint.item_data(int(p.replace("Point", "")))
        distance = hypot(vpoint2.cx - vpoint1.cx, vpoint2.cy - vpoint1.cy)
        self.link_free_move_spinbox.blockSignals(True)
        self.link_free_move_spinbox.setValue(distance)
        self.link_free_move_spinbox.blockSignals(False)
        if other is None:
            self.__adjust_link(distance)

    @Slot(float, name='on_link_free_move_spinbox_valueChanged')
    def __adjust_link(self, value: float):
        """Preview the free move result."""
        base = self.link_free_move_base.currentIndex()
        p = self.link_free_move_other.currentText()
        if not p:
            return

        other = int(p.replace("Point", ""))
        if -1 in {base, other}:
            return

        vpoints = self.EntitiesPoint.data_tuple()
        mapping = {n: f'P{n}' for n in range(len(vpoints))}
        mapping[base, other] = value
        try:
            result = expr_solving(
                self.get_triangle(),
                mapping,
                vpoints,
                tuple(v[-1] for v in self.InputsWidget.input_pairs())
            )
        except ValueError:
            return

        self.MainCanvas.adjust_link(result)

    @Slot(name='on_action_new_link_triggered')
    def new_link(self):
        """Create a link with arguments.

        + Last than one point:

            - Create a new link

        + Search method:

            - Find the intersection between points that was
                including any link.
            - Add the points that is not in the intersection
                to the link.

        + If no, just create a new link by selected points.
        """
        rows = self.EntitiesPoint.selected_rows()
        if not len(rows) > 1:
            self.__edit_link()
            return

        links_all = list(chain(*(
            self.EntitiesPoint.get_links(row) for row in rows
        )))
        count_0 = False
        for p in set(links_all):
            if links_all.count(p) > 1:
                count_0 = True
                break
        if not links_all or not count_0:
            self.add_normal_link(rows)
            return

        name = max(set(links_all), key=links_all.count)
        row = self.EntitiesLink.find_name(name)
        self.CommandStack.beginMacro(f"Edit {{Link: {name}}}")
        args = self.EntitiesLink.row_text(row, has_name=True)
        points = set(self.EntitiesLink.get_points(row))
        points.update(rows)
        args[2] = ','.join(f'Point{p}' for p in points)
        self.CommandStack.push(EditLinkTable(
            row,
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.endMacro()

    @Slot(name='on_action_edit_link_triggered')
    def edit_link(self):
        """Edit a link with arguments."""
        self.__edit_link(self.EntitiesLink.currentRow())

    @Slot()
    def release_ground(self):
        """Clone ground to a new link, then make ground no points."""
        name = self.__get_link_serial_number()
        args = [name, 'Blue', self.EntitiesLink.item(0, 2).text()]
        self.CommandStack.beginMacro(f"Release ground to {{Link: {name}}}")
        # Free all points.
        self.CommandStack.push(EditLinkTable(
            0,
            self.EntitiesLink,
            self.EntitiesPoint,
            ['ground', 'White', '']
        ))
        # Create new link.
        self.CommandStack.push(AddTable(self.EntitiesLink))
        self.CommandStack.push(EditLinkTable(
            self.EntitiesLink.rowCount() - 1,
            self.EntitiesLink,
            self.EntitiesPoint,
            args
        ))
        self.CommandStack.endMacro()

    @Slot()
    def constrain_link(self, row1: Optional[int] = None, row2: int = 0):
        """Turn a link to ground, then delete this link."""
        if row1 is None:
            row1 = self.EntitiesLink.currentRow()
        name = self.EntitiesLink.item(row1, 0).text()
        link_args = self.EntitiesLink.row_text(row1, has_name=True)
        link_args[2] = ''
        new_points = sorted(
            set(self.EntitiesLink.item(0, 2).text().split(',')) |
            set(self.EntitiesLink.item(row1, 2).text().split(','))
        )
        base_args = self.EntitiesLink.row_text(row2, has_name=True)
        base_args[2] = ','.join(e for e in new_points if e)
        self.CommandStack.beginMacro(f"Constrain {{Link: {name}}} to ground")
        # Turn to ground.
        self.CommandStack.push(EditLinkTable(
            row2,
            self.EntitiesLink,
            self.EntitiesPoint,
            base_args
        ))
        # Free all points and delete the link.
        self.CommandStack.push(EditLinkTable(
            row1,
            self.EntitiesLink,
            self.EntitiesPoint,
            link_args
        ))
        self.CommandStack.push(DeleteTable(
            row1,
            self.EntitiesLink,
            is_rename=False
        ))
        self.CommandStack.endMacro()

    def delete_points(self):
        """Delete the selected points.
        Be sure that the points will has new position after deleted.
        """
        selections = self.EntitiesPoint.selected_rows()
        for i, p in enumerate(selections):
            if p > selections[i - 1]:
                row = p - i
            else:
                row = p
            self.delete_point(row)

    def delete_links(self):
        """Delete the selected links.
        Be sure that the links will has new position after deleted.
        """
        selections = self.EntitiesLink.selected_rows()
        selections = tuple(
            p - i + int(0 in selections) if p > selections[i - 1] else p
            for i, p in enumerate(selections)
        )
        for row in selections:
            self.delete_link(row)

    def set_coords_as_current(self):
        """Update points position as current coordinate."""
        vpoints = self.EntitiesPoint.data_tuple()
        self.set_free_move(tuple(
            (row, (vpoint.cx, vpoint.cy, vpoint.angle))
            for row, vpoint in enumerate(vpoints)
        ))

    @abstractmethod
    def get_triangle(self, vpoints: Optional[Tuple[VPoint]] = None) -> List[Tuple[str]]:
        ...
