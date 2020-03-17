# -*- coding: utf-8 -*-

"""The widget of 'Inputs' tab."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

import csv
from typing import TYPE_CHECKING, Tuple, Dict, Sequence, Iterator, Optional
from copy import copy
from qtpy.QtCore import Signal, Slot, QTimer, QPoint
from qtpy.QtWidgets import (
    QWidget,
    QMenu,
    QMessageBox,
    QInputDialog,
    QListWidgetItem,
    QApplication,
)
from pyslvs import VJoint
from pyslvs_ui.info import logger
from .rotatable import QRotatableView
from .inputs_ui import Ui_Form
from .undo_redo import AddInput, DeleteInput, AddPath, DeletePath
if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase

_Coord = Tuple[float, float]
_Paths = Sequence[Sequence[_Coord]]


def _variable_int(text: str) -> int:
    """Change variable text to index."""
    return int(text.split()[-1].replace("Point", ""))


class InputsWidget(QWidget, Ui_Form):
    """There has following functions:

    + Function of mechanism variables settings.
    + Path recording.
    """
    about_to_resolve = Signal()

    def __init__(self, parent: MainWindowBase) -> None:
        super(InputsWidget, self).__init__(parent)
        self.setupUi(self)

        # parent's function pointer
        self.free_move_button = parent.free_move_button
        self.entities_point = parent.entities_point
        self.entities_link = parent.entities_link
        self.vpoints = parent.vpoint_list
        self.vlinks = parent.vlink_list
        self.main_canvas = parent.main_canvas
        self.solve = parent.solve
        self.reload_canvas = parent.reload_canvas
        self.output_to = parent.output_to
        self.conflict = parent.conflict
        self.dof = parent.dof
        self.right_input = parent.right_input
        self.command_stack = parent.command_stack
        self.set_coords_as_current = parent.set_coords_as_current
        self.get_back_position = parent.get_back_position

        # Angle panel
        self.dial = QRotatableView(self)
        self.dial.setStatusTip("Input widget of rotatable joint.")
        self.dial.setEnabled(False)
        self.dial.value_changed.connect(self.__update_var)
        self.dial_spinbox.valueChanged.connect(self.__set_var)
        self.inputs_dial_layout.addWidget(self.dial)

        # Play button
        self.variable_stop.clicked.connect(self.variable_value_reset)

        # Timer for play button
        self.inputs_play_shaft = QTimer()
        self.inputs_play_shaft.setInterval(10)
        self.inputs_play_shaft.timeout.connect(self.__change_index)

        # Change the point coordinates with current position
        self.update_pos.clicked.connect(self.set_coords_as_current)

        # Inputs record context menu
        self.pop_menu_record_list = QMenu(self)
        self.record_list.customContextMenuRequested.connect(
            self.__record_list_context_menu
        )
        self.__path_data: Dict[str, _Paths] = {}

    def clear(self) -> None:
        """Clear function to reset widget status."""
        self.__path_data.clear()
        for _ in range(self.record_list.count() - 1):
            self.record_list.takeItem(1)
        self.variable_list.clear()

    def __set_angle_mode(self) -> None:
        """Change to angle input."""
        self.dial.set_minimum(0)
        self.dial.set_maximum(360)
        self.dial_spinbox.setMinimum(0)
        self.dial_spinbox.setMaximum(360)

    def __set_unit_mode(self) -> None:
        """Change to unit input."""
        self.dial.set_minimum(-500)
        self.dial.set_maximum(500)
        self.dial_spinbox.setMinimum(-500)
        self.dial_spinbox.setMaximum(500)

    def path_data(self) -> Dict[str, _Paths]:
        """Return current path data."""
        return self.__path_data

    @Slot(tuple)
    def set_selection(self, selections: Sequence[int]) -> None:
        """Set one selection from canvas."""
        self.joint_list.setCurrentRow(selections[0])

    @Slot()
    def clear_selection(self) -> None:
        """Clear the points selection."""
        self.driver_list.clear()
        self.joint_list.setCurrentRow(-1)

    @Slot(int, name='on_joint_list_currentRowChanged')
    def __update_relate_points(self, _=None) -> None:
        """Change the point row from input widget."""
        self.driver_list.clear()

        item: Optional[QListWidgetItem] = self.joint_list.currentItem()
        if item is None:
            return
        p0 = _variable_int(item.text())
        base_point = self.vpoints[p0]
        type_int = base_point.type
        if type_int == VJoint.R:
            for i, vpoint in enumerate(self.vpoints):
                if i == p0:
                    continue
                if base_point.same_link(vpoint):
                    if base_point.grounded() and vpoint.grounded():
                        continue
                    self.driver_list.addItem(f"[{vpoint.type_str}] Point{i}")
        elif type_int in {VJoint.P, VJoint.RP}:
            self.driver_list.addItem(f"[{base_point.type_str}] Point{p0}")

    @Slot(int, name='on_driver_list_currentRowChanged')
    def __set_add_var_enabled(self, _=None) -> None:
        """Set enable of 'add variable' button."""
        driver = self.driver_list.currentIndex()
        self.variable_add.setEnabled(driver != -1)

    @Slot(name='on_variable_add_clicked')
    def __add_inputs_variable(
        self,
        p0: Optional[int] = None,
        p1: Optional[int] = None
    ) -> None:
        """Add variable with '->' sign."""
        if p0 is None:
            item: Optional[QListWidgetItem] = self.joint_list.currentItem()
            if item is None:
                return
            p0 = _variable_int(item.text())
        if p1 is None:
            item = self.driver_list.currentItem()
            if item is None:
                return
            p1 = _variable_int(item.text())

        # Check DOF
        if self.dof() <= self.input_count():
            QMessageBox.warning(
                self,
                "Wrong DOF",
                "The number of variable must no more than degrees of freedom."
            )
            return

        # Check same link
        if not self.vpoints[p0].same_link(self.vpoints[p1]):
            QMessageBox.warning(
                self,
                "Wrong pair",
                "The base point and driver point should at the same link."
            )
            return

        # Check repeated pairs
        for p0_, p1_, a in self.input_pairs():
            if {p0, p1} == {p0_, p1_} and self.vpoints[p0].type == VJoint.R:
                QMessageBox.warning(
                    self,
                    "Wrong pair",
                    "There already have a same pair."
                )
                return

        if p0 == p1:
            # One joint by offset
            value = self.vpoints[p0].true_offset()
        else:
            # Two joints by angle
            value = self.vpoints[p0].slope_angle(self.vpoints[p1])
        self.command_stack.push(AddInput('->'.join((
            f'Point{p0}',
            f"Point{p1}",
            f"{value:.02f}",
        )), self.variable_list))

    def add_inputs_variables(self, variables: Sequence[Tuple[int, int]]) -> None:
        """Add from database."""
        for p0, p1 in variables:
            self.__add_inputs_variable(p0, p1)

    @Slot(QListWidgetItem, name='on_variable_list_itemClicked')
    def __dial_ok(self, _=None) -> None:
        """Set the angle of base link and drive link."""
        if self.inputs_play_shaft.isActive():
            return
        row = self.variable_list.currentRow()
        enabled = row > -1
        rotatable = (
            enabled
            and not self.free_move_button.isChecked()
            and self.right_input()
        )
        self.dial.setEnabled(rotatable)
        self.dial_spinbox.setEnabled(rotatable)
        self.oldVar = self.dial.value()
        self.variable_play.setEnabled(rotatable)
        self.variable_speed.setEnabled(rotatable)
        item: Optional[QListWidgetItem] = self.variable_list.currentItem()
        if item is None:
            return
        expr = item.text().split('->')
        p0 = int(expr[0].replace('Point', ''))
        p1 = int(expr[1].replace('Point', ''))
        value = float(expr[2])
        if p0 == p1:
            self.__set_unit_mode()
        else:
            self.__set_angle_mode()
        self.dial.set_value(value if enabled else 0)

    def variable_excluding(self, row: Optional[int] = None) -> None:
        """Remove variable if the point was been deleted. Default: all."""
        one_row: bool = row is not None
        for i, (b, d, a) in enumerate(self.input_pairs()):
            # If this is not origin point any more
            if one_row and row != b:
                continue
            self.command_stack.push(DeleteInput(i, self.variable_list))

    @Slot(name='on_variable_remove_clicked')
    def remove_var(self, row: int = -1) -> None:
        """Remove and reset angle."""
        if row == -1:
            row = self.variable_list.currentRow()
        if not row > -1:
            return
        self.variable_stop.click()
        self.command_stack.push(DeleteInput(row, self.variable_list))
        self.get_back_position()
        self.solve()

    def interval(self) -> float:
        """Return interval value."""
        return self.record_interval.value()

    def input_count(self) -> int:
        """Use to show input variable count."""
        return self.variable_list.count()

    def input_pairs(self) -> Iterator[Tuple[int, int, float]]:
        """Back as point number code."""
        for row in range(self.variable_list.count()):
            var = self.variable_list.item(row).text().split('->')
            p0 = int(var[0].replace('Point', ''))
            p1 = int(var[1].replace('Point', ''))
            angle = float(var[2])
            yield p0, p1, angle

    def variable_reload(self) -> None:
        """Auto check the points and type."""
        self.joint_list.clear()
        for i in range(self.entities_point.rowCount()):
            type_text = self.entities_point.item(i, 2).text()
            self.joint_list.addItem(f"[{type_text}] Point{i}")
        self.variable_value_reset()

    @Slot(float)
    def __set_var(self, value: float) -> None:
        self.dial.set_value(value)

    @Slot(float)
    def __update_var(self, value: float) -> None:
        """Update the value when rotating QDial."""
        item = self.variable_list.currentItem()
        self.dial_spinbox.blockSignals(True)
        self.dial_spinbox.setValue(value)
        self.dial_spinbox.blockSignals(False)
        if item:
            item_text = item.text().split('->')
            item_text[-1] = f"{value:.02f}"
            item.setText('->'.join(item_text))
            self.about_to_resolve.emit()
        if (
            self.record_start.isChecked()
            and abs(self.oldVar - value) > self.record_interval.value()
        ):
            self.main_canvas.record_path()
            self.oldVar = value

    def variable_value_reset(self) -> None:
        """Reset the value of QDial."""
        if self.inputs_play_shaft.isActive():
            self.variable_play.setChecked(False)
            self.inputs_play_shaft.stop()
        self.get_back_position()
        for i, (p0, p1, a) in enumerate(self.input_pairs()):
            self.variable_list.item(i).setText('->'.join([
                f'Point{p0}',
                f'Point{p1}',
                f"{self.vpoints[p0].slope_angle(self.vpoints[p1]):.02f}",
            ]))
        self.__dial_ok()
        self.solve()

    @Slot(bool, name='on_variable_play_toggled')
    def __play(self, toggled: bool) -> None:
        """Triggered when play button was changed."""
        self.dial.setEnabled(not toggled)
        self.dial_spinbox.setEnabled(not toggled)
        if toggled:
            self.inputs_play_shaft.start()
        else:
            self.inputs_play_shaft.stop()
            if self.update_pos_option.isChecked():
                self.set_coords_as_current()

    @Slot()
    def __change_index(self) -> None:
        """QTimer change index."""
        index = self.dial.value()
        speed = self.variable_speed.value()
        extreme_rebound = (
            self.conflict.isVisible()
            and self.extremeRebound.isChecked()
        )
        if extreme_rebound:
            speed = -speed
            self.variable_speed.setValue(speed)
        index += speed * 0.06 * (3 if extreme_rebound else 1)
        self.dial.set_value(index)

    @Slot(bool, name='on_record_start_toggled')
    def __start_record(self, toggled: bool) -> None:
        """Save to file path data."""
        if toggled:
            self.main_canvas.record_start(int(
                self.dial_spinbox.maximum() / self.record_interval.value()
            ))
            return
        path = self.main_canvas.get_record_path()
        name, ok = QInputDialog.getText(
            self,
            "Recording completed!",
            "Please input name tag:"
        )
        i = 0
        name = name or f"Record_{i}"
        while name in self.__path_data:
            name = f"Record_{i}"
            i += 1
        QMessageBox.information(
            self,
            "Record",
            "The name tag is being used or empty."
        )
        self.add_path(name, path)

    def add_path(self, name: str, path: _Paths) -> None:
        """Add path function."""
        self.command_stack.push(AddPath(
            self.record_list,
            name,
            self.__path_data,
            path
        ))
        self.record_list.setCurrentRow(self.record_list.count() - 1)

    def load_paths(self, paths: Dict[str, _Paths]) -> None:
        """Add multiple path."""
        for name, path in paths.items():
            self.add_path(name, path)

    @Slot(name='on_record_remove_clicked')
    def __remove_path(self) -> None:
        """Remove path data."""
        row = self.record_list.currentRow()
        if not row > 0:
            return
        self.command_stack.push(DeletePath(
            row,
            self.record_list,
            self.__path_data
        ))
        self.record_list.setCurrentRow(self.record_list.count() - 1)
        self.reload_canvas()

    @Slot(QListWidgetItem, name='on_record_list_itemDoubleClicked')
    def __path_dlg(self, item: QListWidgetItem) -> None:
        """View path data."""
        name = item.text().split(":")[0]
        try:
            data = self.__path_data[name]
        except KeyError:
            return

        points_text = ", ".join(f"Point{i}" for i in range(len(data)))
        if QMessageBox.question(
            self,
            "Path data",
            f"This path data including {points_text}.",
            (QMessageBox.Save | QMessageBox.Close),
            QMessageBox.Close
        ) != QMessageBox.Save:
            return
        file_name = self.output_to(
            "path data",
            ["Comma-Separated Values (*.csv)", "Text file (*.txt)"]
        )
        if not file_name:
            return
        with open(file_name, 'w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream)
            for point in data:
                for coordinate in point:
                    writer.writerow(coordinate)
                writer.writerow(())
        logger.info(f"Output path data: {file_name}")

    @Slot(QPoint)
    def __record_list_context_menu(self, p: QPoint) -> None:
        """Show the context menu.

        Show path [0], [1], ...
        Or copy path coordinates.
        """
        row = self.record_list.currentRow()
        if not row > -1:
            return
        showall_action = self.pop_menu_record_list.addAction("Show all")
        showall_action.index = -1
        copy_action = self.pop_menu_record_list.addAction("Copy as new")
        name = self.record_list.item(row).text().split(':')[0]
        if name in self.__path_data:
            data = self.__path_data[name]
        else:
            # Auto preview path
            data = self.main_canvas.path_preview
        targets = 0
        for text in ("Show", "Copy data from"):
            self.pop_menu_record_list.addSeparator()
            for i, path in enumerate(data):
                if len(set(path)) > 1:
                    action = self.pop_menu_record_list.addAction(f"{text} Point{i}")
                    action.index = i
                    targets += 1
        copy_action.setEnabled(targets > 0)
        action = self.pop_menu_record_list.exec_(self.record_list.mapToGlobal(p))
        if action is None:
            self.pop_menu_record_list.clear()
            return
        text = action.text()
        if action == copy_action:
            # Copy path data
            num = 0
            name_copy = f"{name}_{num}"
            while name_copy in self.__path_data:
                name_copy = f"{name}_{num}"
                num += 1
            self.add_path(name_copy, copy(data))
        elif text.startswith("Copy data from"):
            # Copy data to clipboard (csv)
            QApplication.clipboard().setText('\n'.join(
                f"[{x}, {y}]," for x, y in data[action.index]
            ))
        elif text.startswith("Show"):
            # Switch points enabled status
            if action.index == -1:
                self.record_show.setChecked(True)
            self.main_canvas.set_path_show(action.index)
        self.pop_menu_record_list.clear()

    @Slot(bool, name='on_record_show_toggled')
    def __set_path_show(self, toggled: bool) -> None:
        """Show all paths or hide."""
        self.main_canvas.set_path_show(-1 if toggled else -2)

    @Slot(int, name='on_record_list_currentRowChanged')
    def __set_path(self, _=None) -> None:
        """Reload the canvas when switch the path."""
        if not self.record_show.isChecked():
            self.record_show.setChecked(True)
        self.reload_canvas()

    def current_path(self) -> _Paths:
        """Return current path data to main canvas.

        + No path.
        + Show path data.
        + Auto preview.
        """
        row = self.record_list.currentRow()
        if row in {0, -1}:
            return ()
        path_name = self.record_list.item(row).text().split(':')[0]
        return self.__path_data.get(path_name, ())

    @Slot(name='on_variable_up_clicked')
    @Slot(name='on_variable_down_clicked')
    def __set_variable_priority(self) -> None:
        row = self.variable_list.currentRow()
        if not row > -1:
            return
        item = self.variable_list.currentItem()
        self.variable_list.insertItem(
            row + (-1 if self.sender() == self.variable_up else 1),
            self.variable_list.takeItem(row)
        )
        self.variable_list.setCurrentItem(item)
