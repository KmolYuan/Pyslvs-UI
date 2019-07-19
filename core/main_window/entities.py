# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

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
from pyslvs import (
    VJoint,
    VPoint,
    expr_solving,
    Graph,
    edges_view,
    ExpressionStack,
)
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
from core.entities import EditPointDialog, EditLinkDialog
from core.widgets import (
    AddTable,
    DeleteTable,
    EditPointTable,
    EditLinkTable,
    FixSequenceNumber,
)
from core.widgets import MainWindowBase


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


class EntitiesMethodInterface(MainWindowBase, ABC):

    """Abstract class for entities methods."""

    def __edit_point(self, row: Union[int, bool] = False):
        """Edit point function."""
        dlg = EditPointDialog(self.vpoint_list, self.vlink_list, row, self)
        dlg.show()
        if not dlg.exec():
            dlg.deleteLater()
            return

        row_count = self.entities_point.rowCount()
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
            self.command_stack.beginMacro(f"Add {{Point{row_count}}}")
            self.command_stack.push(AddTable(self.vpoint_list, self.entities_point))
            row = row_count
        else:
            row = dlg.name_box.currentIndex()
            self.command_stack.beginMacro(f"Edit {{Point{row}}}")

        dlg.deleteLater()

        self.command_stack.push(EditPointTable(
            row,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.command_stack.endMacro()

    def __edit_link(self, row: Union[int, bool] = False):
        """Edit link function."""
        dlg = EditLinkDialog(self.vpoint_list, self.vlink_list, row, self)
        dlg.show()
        if not dlg.exec():
            dlg.deleteLater()
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
            self.command_stack.beginMacro(f"Add {{Link: {name}}}")
            self.command_stack.push(AddTable(self.vlink_list, self.entities_link))
            row = self.entities_link.rowCount() - 1
        else:
            row = dlg.name_box.currentIndex()
            self.command_stack.beginMacro(f"Edit {{Link: {name}}}")

        dlg.deleteLater()

        self.command_stack.push(EditLinkTable(
            row,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.command_stack.endMacro()

    def __get_link_serial_number(self) -> str:
        """Return a new serial number name of link."""
        names = {
            self.entities_link.item(row, 0).text()
            for row in range(self.entities_link.rowCount())
        }
        i = 1
        while f"link_{i}" in names:
            i += 1
        return f"link_{i}"

    @Slot(name='on_action_delete_link_triggered')
    def delete_link(self, row: Optional[int] = None):
        """Push delete link command to stack.

        Remove link will not remove the points.
        """
        if row is None:
            row = self.entities_link.currentRow()
        if row < 1:
            return
        args = self.entities_link.row_data(row)
        args[2] = ''
        name = self.entities_link.item(row, 0).text()
        self.command_stack.beginMacro(f"Delete {{Link: {name}}}")
        self.command_stack.push(EditLinkTable(
            row,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.command_stack.push(DeleteTable(
            row,
            self.vlink_list,
            self.entities_link,
            is_rename=False
        ))
        self.command_stack.endMacro()

    @Slot(name='on_action_delete_point_triggered')
    def delete_point(self, row: Optional[int] = None):
        """Push delete point command to stack."""
        if row is None:
            row = self.entities_point.currentRow()
        if row < 0:
            return
        args = self.entities_point.row_data(row)
        args[0] = ''
        self.command_stack.beginMacro(f"Delete {{Point{row}}}")
        for i in reversed([
            i for i, (b, d, a) in enumerate(self.inputs_widget.input_pairs())
            if row in {b, d}
        ]):
            self.inputs_widget.remove_var(i)
        self.command_stack.push(EditPointTable(
            row,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        for i in range(self.entities_link.rowCount()):
            self.command_stack.push(FixSequenceNumber(
                self.entities_link,
                i,
                row
            ))
        self.command_stack.push(DeleteTable(
            row,
            self.vpoint_list,
            self.entities_point,
            is_rename=True
        ))
        self.inputs_widget.variable_excluding(row)
        self.command_stack.endMacro()

    @Slot(float, float)
    def add_point_by_pos(self, x: float, y: float):
        """Add point group using alt key."""
        if self.main_panel.currentIndex() == self.synthesis_tab_widget.currentIndex() == 2:
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
        type_num: VJoint = VJoint.R,
        angle: float = 0.
    ) -> int:
        """Add an ordinary point. Return the row count of new point."""
        row_count = self.entities_point.rowCount()
        self.command_stack.beginMacro(f"Add {{Point{row_count}}}")
        self.command_stack.push(AddTable(self.vpoint_list, self.entities_point))
        if type_num == VJoint.R:
            type_str = 'R'
        elif type_num == VJoint.P:
            type_str = f'P:{angle}'
        else:
            type_str = f'RP:{angle}'
        self.command_stack.push(EditPointTable(
            row_count,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            (links, type_str, color, x, y)
        ))
        self.command_stack.endMacro()
        return row_count

    def add_points(
        self,
        p_attr: Sequence[Tuple[float, float, str, str, int, float]]
    ):
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
        base_count = self.entities_point.rowCount()
        self.command_stack.beginMacro(
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
                ground = self.entities_link.rowCount() - 1
        self.command_stack.endMacro()
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
        self.command_stack.beginMacro(f"Add {{Link: {name}}}")
        self.command_stack.push(AddTable(self.vlink_list, self.entities_link))
        self.command_stack.push(EditLinkTable(
            self.entities_link.rowCount() - 1,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            link_args
        ))
        self.command_stack.endMacro()

    def new_point(self):
        """Create a point with arguments."""
        self.__edit_point()

    @Slot(name='on_action_edit_point_triggered')
    def edit_point(self):
        """Edit a point with arguments."""
        row = self.entities_point.currentRow()
        self.__edit_point(row if (row > -1) else 0)

    def lock_points(self):
        """Turn a group of points to fixed on ground or not."""
        to_fixed = self.action_point_context_lock.isChecked()
        for row in self.entities_point.selected_rows():
            new_links = self.entities_point.item(row, 1).text().split(',')
            if to_fixed:
                if 'ground' not in new_links:
                    new_links.append('ground')
            else:
                if 'ground' in new_links:
                    new_links.remove('ground')
            args = self.entities_point.row_data(row)
            args[0] = ','.join(s for s in new_links if s)
            self.command_stack.beginMacro(f"Edit {{Point{row}}}")
            self.command_stack.push(EditPointTable(
                row,
                self.vpoint_list,
                self.vlink_list,
                self.entities_point,
                self.entities_link,
                args
            ))
            self.command_stack.endMacro()

    def clone_point(self):
        """Clone a point (with orange color)."""
        row = self.entities_point.currentRow()
        args = self.entities_point.row_data(row)
        args[2] = 'Orange'
        row_count = self.entities_point.rowCount()
        self.command_stack.beginMacro(f"Clone {{Point{row}}} as {{Point{row_count}}}")
        self.command_stack.push(AddTable(self.vpoint_list, self.entities_point))
        self.command_stack.push(EditPointTable(
            row_count,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.command_stack.endMacro()

    @Slot(name="on_action_scale_points_triggered")
    def __set_scale(self):
        """Scale the mechanism."""
        dlg = _ScaleDialog(self)
        if not dlg.exec():
            dlg.deleteLater()
            return

        factor = dlg.factor()
        dlg.deleteLater()

        self.command_stack.beginMacro(f"Scale mechanism: {factor}")
        for row in range(self.entities_point.rowCount()):
            args = self.entities_point.row_data(row)
            args[3] *= factor
            args[4] *= factor
            self.command_stack.push(EditPointTable(
                row,
                self.vpoint_list,
                self.vlink_list,
                self.entities_point,
                self.entities_link,
                args
            ))
        self.command_stack.endMacro()

    @Slot(tuple)
    def set_free_move(
        self,
        args: Sequence[Tuple[int, Tuple[float, float, float]]]
    ):
        """Free move function."""
        points_text = ", ".join(f"Point{c[0]}" for c in args)
        self.command_stack.beginMacro(f"Moved {{{points_text}}}")
        for row, (x, y, angle) in args:
            args = self.entities_point.row_data(row)
            args[3] = x
            args[4] = y
            if args[1] != 'R':
                args[1] = f"{args[1].split(':')[0]}:{angle:.02f}"
            self.command_stack.push(EditPointTable(
                row,
                self.vpoint_list,
                self.vlink_list,
                self.entities_point,
                self.entities_link,
                args
            ))
        self.command_stack.endMacro()

    @Slot(int, name='on_link_free_move_base_currentIndexChanged')
    def __reload_adjust_link_base(self, base: int):
        """Set the base and other option."""
        if base == -1:
            return
        self.link_free_move_other.clear()
        for link in self.vpoint_list[base].links:
            if link == 'ground':
                continue
            for i in self.vlink_list[self.entities_link.find_name(link)].points:
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

        vpoint1 = self.vpoint_list[self.link_free_move_base.currentIndex()]
        vpoint2 = self.vpoint_list[int(p.replace("Point", ""))]
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

        mapping = {n: f'P{n}' for n in range(len(self.vpoint_list))}
        mapping[base, other] = value
        try:
            result = expr_solving(
                self.get_triangle(),
                mapping,
                self.vpoint_list,
                tuple(v[-1] for v in self.inputs_widget.input_pairs())
            )
        except ValueError:
            return

        self.main_canvas.adjust_link(result)

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
        rows = self.entities_point.selected_rows()
        if not len(rows) > 1:
            self.__edit_link()
            return

        links_all = list(chain(*(
            self.entities_point.get_links(row) for row in rows
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
        row = self.entities_link.find_name(name)
        self.command_stack.beginMacro(f"Edit {{Link: {name}}}")
        args = self.entities_link.row_data(row)
        points = set(self.entities_link.get_points(row))
        points.update(rows)
        args[2] = ','.join(f'Point{p}' for p in points)
        self.command_stack.push(EditLinkTable(
            row,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.command_stack.endMacro()

    @Slot(name='on_action_edit_link_triggered')
    def edit_link(self):
        """Edit a link with arguments."""
        self.__edit_link(self.entities_link.currentRow())

    @Slot()
    def release_ground(self):
        """Clone ground to a new link, then make ground no points."""
        name = self.__get_link_serial_number()
        args = [name, 'Blue', self.entities_link.item(0, 2).text()]
        self.command_stack.beginMacro(f"Release ground to {{Link: {name}}}")
        # Free all points.
        self.command_stack.push(EditLinkTable(
            0,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            ['ground', 'White', '']
        ))
        # Create new link.
        self.command_stack.push(AddTable(self.vlink_list, self.entities_link))
        self.command_stack.push(EditLinkTable(
            self.entities_link.rowCount() - 1,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            args
        ))
        self.command_stack.endMacro()

    @Slot()
    def constrain_link(self, row1: Optional[int] = None, row2: int = 0):
        """Turn a link to ground, then delete this link."""
        if row1 is None:
            row1 = self.entities_link.currentRow()
        name = self.entities_link.item(row1, 0).text()
        link_args = self.entities_link.row_data(row1)
        link_args[2] = ''
        new_points = sorted(
            set(self.entities_link.item(0, 2).text().split(',')) |
            set(self.entities_link.item(row1, 2).text().split(','))
        )
        base_args = self.entities_link.row_data(row2)
        base_args[2] = ','.join(e for e in new_points if e)
        self.command_stack.beginMacro(f"Constrain {{Link: {name}}} to ground")
        # Turn to ground.
        self.command_stack.push(EditLinkTable(
            row2,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            base_args
        ))
        # Free all points and delete the link.
        self.command_stack.push(EditLinkTable(
            row1,
            self.vpoint_list,
            self.vlink_list,
            self.entities_point,
            self.entities_link,
            link_args
        ))
        self.command_stack.push(DeleteTable(
            row1,
            self.vlink_list,
            self.entities_link,
            is_rename=False
        ))
        self.command_stack.endMacro()

    @Slot()
    def delete_selected_points(self):
        """Delete the selected points.
        Be sure that the points will has new position after deleted.
        """
        selections = self.entities_point.selected_rows()
        for i, p in enumerate(selections):
            if p > selections[i - 1]:
                row = p - i
            else:
                row = p
            self.delete_point(row)

    @Slot()
    def delete_selected_links(self):
        """Delete the selected links.
        Be sure that the links will has new position after deleted.
        """
        selections = self.entities_link.selected_rows()
        selections = tuple(
            p - i + int(0 in selections) if p > selections[i - 1] else p
            for i, p in enumerate(selections)
        )
        for row in selections:
            self.delete_link(row)

    def set_coords_as_current(self):
        """Update points position as current coordinate."""
        self.set_free_move(tuple(
            (row, (vpoint.cx, vpoint.cy, vpoint.angle))
            for row, vpoint in enumerate(self.vpoint_list)
        ))

    @abstractmethod
    def get_triangle(self, vpoints: Optional[Tuple[VPoint]] = None) -> ExpressionStack:
        ...
