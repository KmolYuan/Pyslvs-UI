# -*- coding: utf-8 -*-

"""'dimensional_synthesis' module contains
dimensional synthesis functional interfaces.
"""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    cast,
    TYPE_CHECKING,
    List,
    Tuple,
    Sequence,
    Dict,
    Iterable,
    Callable,
    Union,
    Optional,
    Any,
)
from math import hypot
import pprint
from copy import deepcopy
from re import finditer
from openpyxl import load_workbook
from qtpy.QtCore import Slot, QModelIndex
from qtpy.QtWidgets import (
    QWidget,
    QApplication,
    QMessageBox,
    QHeaderView,
    QListWidgetItem,
    QInputDialog,
    QDoubleSpinBox,
    QTableWidgetItem,
    QProgressDialog,
    QRadioButton,
)
from qtpy.QtGui import QIcon, QPixmap
from pyslvs import (
    VLink,
    vpoints_configure,
    expr_solving,
    parse_pos,
    parse_vpoints,
    parse_vlinks,
    efd_fitting,
)
from pyslvs.metaheuristics import PARAMS, DEFAULT_PARAMS, AlgorithmType
from pyslvs_ui.graphics import PreviewCanvas
from pyslvs_ui.synthesis import CollectionsDialog
from .dialogs import (
    AlgorithmOptionDialog,
    EditPathDialog,
    ProgressDialog,
    PreviewDialog,
    ChartDialog,
)
from .dimension_widget_ui import Ui_Form
if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase

__all__ = ['DimensionalSynthesis']
_Coord = Tuple[float, float]
_PATH_PATTERN = r"([+-]?\d+\.?\d*)[\t ]*[,/]?[\t ]*([+-]?\d+\.?\d*)[ji]?;?\s*"


class DimensionalSynthesis(QWidget, Ui_Form):

    """Dimensional synthesis widget.

    User can run the dimensional synthesis here.
    """

    def __init__(self, parent: MainWindowBase) -> None:
        """Reference names:

        + Iteration collections.
        + Result data.
        + Main window function references.
        """
        super(DimensionalSynthesis, self).__init__(parent)
        self.setupUi(self)
        self.mech: Dict[str, Any] = {}
        self.path: Dict[int, List[_Coord]] = {}
        # Some reference of 'collections'
        self.collections = parent.collections.configure_widget.collections
        self.get_collection = parent.get_configure
        self.input_from = parent.input_from
        self.output_to = parent.output_to
        self.save_reply_box = parent.save_reply_box
        self.project_no_save = parent.project_no_save
        self.merge_result = parent.merge_result
        self.update_ranges = parent.main_canvas.update_ranges
        self.set_solving_path = parent.main_canvas.set_solving_path
        self.prefer = parent.prefer
        # Data and functions
        self.mechanism_data: List[Dict[str, Any]] = []
        self.alg_options: Dict[str, Union[int, float]] = {}
        self.alg_options.update(DEFAULT_PARAMS)
        self.alg_options.update(PARAMS[AlgorithmType.DE])
        # Canvas
        self.preview_canvas = PreviewCanvas(self)
        self.preview_layout.addWidget(self.preview_canvas)
        # Splitter
        self.main_splitter.setStretchFactor(0, 10)
        self.main_splitter.setStretchFactor(1, 100)
        self.up_splitter.setSizes([80, 100])
        self.down_splitter.setSizes([20, 80])
        # Table widget column width
        header = self.parameter_list.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.algorithm_options: Dict[AlgorithmType, QRadioButton] = {}
        for option in PARAMS:
            button = QRadioButton(option.value, self)
            button.clicked.connect(self.__set_algorithm_default)
            self.algorithm_options[option] = button
            self.algorithm_layout.addWidget(button)
        self.clear()

    def clear(self) -> None:
        """Clear all sub-widgets."""
        self.mechanism_data.clear()
        self.result_list.clear()
        self.__clear_settings()
        self.__has_result()

    def __clear_settings(self) -> None:
        """Clear sub-widgets that contain the setting."""
        self.clear_path(ask=False)
        self.path.clear()
        self.mech.clear()
        self.preview_canvas.clear()
        self.profile_name.clear()
        self.algorithm_options[AlgorithmType.DE].setChecked(True)
        self.__set_algorithm_default()
        self.parameter_list.setRowCount(0)
        self.target_points.clear()
        self.target_label.setVisible(self.has_target())
        self.expression_string.clear()
        self.update_range()
        self.__able_to_generate()

    def has_target(self) -> bool:
        """Return True if the panel is no target settings."""
        return self.target_points.count() > 0

    @Slot(name='on_clear_button_clicked')
    def __user_clear(self) -> None:
        if not self.profile_name.text():
            return
        if QMessageBox.question(
            self,
            "Clear setting",
            "Do you want to clear the setting?"
        ) == QMessageBox.Yes:
            self.__clear_settings()

    def load_results(self, mechanism_data: Sequence[Dict[str, Any]]) -> None:
        """Append results of project database to memory."""
        for e in mechanism_data:
            self.mechanism_data.append(e)
            self.__add_result(e)

    def __current_path_changed(self) -> None:
        """Call the canvas to update to current target path."""
        self.set_solving_path({
            f"P{name}": tuple(path) for name, path in self.path.items()
        })
        self.__able_to_generate()

    def current_path(self) -> List[_Coord]:
        """Return the pointer of current target path."""
        item = self.target_points.currentItem()
        if item is None:
            return []
        return self.path[int(item.text().replace('P', ''))]

    @Slot(str, name='on_target_points_currentTextChanged')
    def __set_target(self, _=None) -> None:
        """Switch to the current target path."""
        self.path_list.clear()
        for x, y in self.current_path():
            self.path_list.addItem(f"({x:.04f}, {y:.04f})")
        self.__current_path_changed()

    @Slot(name='on_path_clear_clicked')
    def clear_path(self, *, ask: bool = True) -> None:
        """Clear the current target path."""
        if ask:
            if QMessageBox.question(
                self,
                "Clear path",
                "Are you sure to clear the current path?"
            ) != QMessageBox.Yes:
                return
        self.current_path().clear()
        self.path_list.clear()
        self.__current_path_changed()

    @Slot(name='on_path_copy_clicked')
    def __copy_path(self) -> None:
        """Copy the current path coordinates to clipboard."""
        QApplication.clipboard().setText('\n'.join(
            f"{x},{y}" for x, y in self.current_path()
        ))

    @Slot(name='on_path_paste_clicked')
    def __paste_path(self) -> None:
        """Paste path data from clipboard."""
        self.__read_path_from_csv(QApplication.clipboard().text())

    @Slot(name='on_import_csv_button_clicked')
    def __import_csv(self) -> None:
        """Paste path data from a text file."""
        file_name = self.input_from(
            "path data",
            ["Text file (*.txt)", "Comma-Separated Values (*.csv)"]
        )
        if not file_name:
            return
        with open(file_name, 'r', encoding='utf-8', newline='') as f:
            data = f.read()
        self.__read_path_from_csv(data)

    def __read_path_from_csv(self, raw: str) -> None:
        """Turn string to float then add them to current target path."""
        for m in finditer(_PATH_PATTERN, raw):
            self.add_point(float(m.group(1) or 0), float(m.group(2) or 0))

    @Slot(name='on_save_path_button_clicked')
    def __save_path(self):
        """Save current path."""
        path = self.current_path()
        if not path:
            return
        file_name = self.output_to("Path file", ["Text file (*.txt)"])
        if not file_name:
            return
        with open(file_name, 'w+', encoding='utf-8') as f:
            f.write("\n".join(f"{x}, {y}" for x, y in path))
        self.save_reply_box("Path file", file_name)

    @Slot(name='on_import_xlsx_button_clicked')
    def __import_xlsx(self) -> None:
        """Paste path data from a Excel file."""
        file_name = self.input_from(
            "Excel project",
            ["Microsoft Office Excel (*.xlsx *.xlsm *.xltx *.xltm)"]
        )
        if not file_name:
            return
        wb = load_workbook(file_name)
        sheets = wb.get_sheet_names()
        name, ok = QInputDialog.getItem(self, "Sheets", "Select a sheet:", sheets, 0)
        if not ok:
            return
        ws = wb.get_sheet_by_name(sheets.index(name))
        # Keep finding until there is no value
        i = 1
        while True:
            sx = ws.cell(i, 1).value
            sy = ws.cell(i, 2).value
            if None in {sx, sy}:
                break
            try:
                self.add_point(float(sx), float(sy))
            except (IndexError, AttributeError):
                QMessageBox.warning(
                    self,
                    "File error",
                    "Wrong format.\n"
                    "The data sheet seems to including non-digital cell."
                )
                break
            i += 1

    @Slot(name='on_edit_path_button_clicked')
    def __adjust_path(self) -> None:
        """Show up path adjust dialog and
        get back the changes of current target path.
        """
        dlg = EditPathDialog(self)
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()
        self.__current_path_changed()

    @Slot(name='on_efd_button_clicked')
    def __efd_path(self) -> None:
        """Elliptical Fourier Descriptors."""
        path = self.current_path()
        n, ok = QInputDialog.getInt(
            self,
            "Elliptical Fourier Descriptors",
            "The number of points:",
            len(path), 3
        )
        if not ok:
            return
        dlg = QProgressDialog("Path transform.", "Cancel", 0, 1, self)
        dlg.setWindowTitle("Elliptical Fourier Descriptors")
        dlg.show()
        self.set_path(efd_fitting(path, n))
        dlg.setValue(1)
        dlg.deleteLater()

    def add_point(self, x: float, y: float) -> None:
        """Add path data to list widget and current target path."""
        self.current_path().append((x, y))
        self.path_list.addItem(f"({x:.04f}, {y:.04f})")
        self.path_list.setCurrentRow(self.path_list.count() - 1)
        self.__current_path_changed()

    def set_path(self, path: Iterable[Tuple[float, float]]) -> None:
        """Set the current path."""
        self.clear_path(ask=False)
        for x, y in path:
            self.add_point(x, y)
        self.__current_path_changed()

    @Slot(float, float)
    def set_point(self, x: float, y: float) -> None:
        """Set the coordinate of current target path."""
        if not self.edit_target_point_button.isChecked():
            return
        for i, (cx, cy) in enumerate(self.current_path()):
            if hypot(x - cx, y - cy) < 5:
                index = i
                self.path_list.setCurrentRow(index)
                break
        else:
            return
        self.current_path()[index] = (x, y)
        self.path_list.item(index).setText(f"({x:.04f}, {y:.04f})")
        self.__current_path_changed()

    @Slot(name='on_close_path_clicked')
    def __close_path(self) -> None:
        """Add a the last point same as first point."""
        path = self.current_path()
        if self.path_list.count() > 1 and path[0] != path[-1]:
            self.add_point(*path[0])

    @Slot(name='on_point_up_clicked')
    def __move_up_point(self) -> None:
        """Target point move up."""
        row = self.path_list.currentRow()
        if not (row > 0 and self.path_list.count() > 1):
            return
        path = self.current_path()
        path.insert(row - 1, (path[row][0], path[row][1]))
        path.pop(row + 1)
        c = self.path_list.currentItem().text()[1:-1].split(", ")
        self.path_list.insertItem(row - 1, f"({c[0]}, {c[1]})")
        self.path_list.takeItem(row + 1)
        self.path_list.setCurrentRow(row - 1)
        self.__current_path_changed()

    @Slot(name='on_point_down_clicked')
    def __move_down_point(self) -> None:
        """Target point move down."""
        row = self.path_list.currentRow()
        if not (
            row < self.path_list.count() - 1
            and self.path_list.count() > 1
        ):
            return
        path = self.current_path()
        path.insert(row + 2, (path[row][0], path[row][1]))
        path.pop(row)
        c = self.path_list.currentItem().text()[1:-1].split(", ")
        self.path_list.insertItem(row + 2, f"{c[0]}, {c[1]}")
        self.path_list.takeItem(row)
        self.path_list.setCurrentRow(row + 1)
        self.__current_path_changed()

    @Slot(name='on_point_delete_clicked')
    def __delete_point(self) -> None:
        """Delete a target point."""
        row = self.path_list.currentRow()
        if not row > -1:
            return
        self.current_path().pop(row)
        self.path_list.takeItem(row)
        self.__current_path_changed()

    def __able_to_generate(self) -> None:
        """Set button enable if all the data are already."""
        self.point_num.setText(
            "<p><span style=\"font-size:12pt;"
            f"color:#00aa00;\">{self.path_list.count()}</span></p>"
        )
        n = bool(
            self.mech
            and self.path_list.count() > 2
            and self.expression_string.text()
        )
        for button in (
            self.save_path_button,
            self.edit_path_button,
            self.efd_button,
            self.synthesis_button,
        ):
            button.setEnabled(n)

    @Slot(name='on_synthesis_button_clicked')
    def __synthesis(self) -> None:
        """Start synthesis."""
        # Check if the number of target points are same.
        length = -1
        for path in self.path.values():
            if length < 0:
                length = len(path)
            if len(path) != length:
                QMessageBox.warning(
                    self,
                    "Target Error",
                    "The length of target paths should be the same."
                )
                return
        # Get the algorithm type
        for option, button in self.algorithm_options.items():
            if button.isChecked():
                algorithm = option
                break
        else:
            raise ValueError("no option")
        # Deep copy it so the pointer will not the same
        mech = deepcopy(self.mech)
        mech['expression'] = parse_vpoints(mech.pop('expression', []))
        mech['target'] = deepcopy(self.path)

        def name_in_table(target_name: str) -> int:
            """Find a target_name and return the row from the table."""
            for r in range(self.parameter_list.rowCount()):
                if self.parameter_list.item(r, 0).text() == target_name:
                    return r
            return -1

        placement: Dict[int, Tuple[float, float, float]] = mech['placement']
        for name in placement:
            row = name_in_table(f"P{name}")
            placement[name] = (
                self.parameter_list.cellWidget(row, 2).value(),
                self.parameter_list.cellWidget(row, 3).value(),
                self.parameter_list.cellWidget(row, 4).value(),
            )
        # Start progress dialog
        dlg = ProgressDialog(algorithm, mech, self.alg_options, self)
        dlg.show()
        if not dlg.exec_():
            dlg.deleteLater()
            return
        mechanisms_plot: List[Dict[str, Any]] = []
        for data in dlg.mechanisms:
            mechanisms_plot.append({
                'time_fitness': data.pop('time_fitness'),
                'Algorithm': data['Algorithm'],
            })
            self.mechanism_data.append(data)
            self.__add_result(data)
        self.__set_time(dlg.time_spend)
        self.project_no_save()
        dlg.deleteLater()
        dlg = ChartDialog("Convergence Data", mechanisms_plot, self)
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()

    def __set_time(self, time: float) -> None:
        """Set the time label."""
        self.timeShow.setText(
            f"<html><head/><body><p><span style=\"font-size:16pt\">"
            f"{int(time // 60):02d}min {time % 60:05.02f}s"
            f"</span></p></body></html>"
        )

    def __add_result(self, result: Dict[str, Any]) -> None:
        """Add result items, except add to the list."""
        item = QListWidgetItem(result['Algorithm'])
        interrupt = result['interrupted']
        if interrupt == 'False':
            interrupt_icon = "task_completed.png"
        elif interrupt == 'N/A':
            interrupt_icon = "question.png"
        else:
            interrupt_icon = "interrupted.png"
        item.setIcon(QIcon(QPixmap(f":/icons/{interrupt_icon}")))
        if interrupt == 'False':
            interrupt_text = "No interrupt."
        else:
            interrupt_text = f"Interrupt at: {interrupt}"
        text = f"{result['Algorithm']} ({interrupt_text})"
        if interrupt == 'N/A':
            text += "\n※Completeness is unknown."
        item.setToolTip(text)
        self.result_list.addItem(item)

    @Slot(name='on_delete_button_clicked')
    def __delete_result(self) -> None:
        """Delete a result."""
        row = self.result_list.currentRow()
        if not row > -1:
            return
        if QMessageBox.question(
            self,
            "Delete",
            "Delete this result from list?"
        ) != QMessageBox.Yes:
            return
        self.mechanism_data.pop(row)
        self.result_list.takeItem(row)
        self.project_no_save()
        self.__has_result()

    @Slot(QModelIndex, name='on_result_list_clicked')
    def __has_result(self, *_) -> None:
        """Set enable if there has any result."""
        enable = self.result_list.currentRow() > -1
        for button in (
            self.merge_button,
            self.delete_button,
            self.result_load_settings,
            self.result_clipboard
        ):
            button.setEnabled(enable)

    @Slot(QModelIndex, name='on_result_list_doubleClicked')
    def __show_result(self, _=None) -> None:
        """Double click result item can show up preview dialog."""
        row = self.result_list.currentRow()
        if not row > -1:
            return
        dlg = PreviewDialog(self.mechanism_data[row], self.__get_path(row), self)
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()

    @Slot(name='on_merge_button_clicked')
    def __merge_result(self) -> None:
        """Merge mechanism into main canvas."""
        row = self.result_list.currentRow()
        if not row > -1:
            return
        if QMessageBox.question(
            self,
            "Merge",
            "Add the result expression into storage?"
        ) == QMessageBox.Yes:
            expression: str = self.mechanism_data[row]['expression']
            self.merge_result(expression, self.__get_path(row))

    def __get_path(self, row: int) -> List[List[_Coord]]:
        """Using result data to generate paths of mechanism."""
        result = self.mechanism_data[row]
        expression: str = result['expression']
        same: Dict[int, int] = result['same']
        inputs: List[Tuple[Tuple[int, int], Tuple[float, float]]] = result['input']
        input_list = []
        for (b, d), _ in inputs:
            for i in range(b):
                if i in same:
                    b -= 1
            for i in range(d):
                if i in same:
                    d -= 1
            input_list.append((b, d))
        vpoints = parse_vpoints(expression)
        expr = vpoints_configure(vpoints, input_list)
        b, d = input_list[0]
        base_angle = vpoints[b].slope_angle(vpoints[d])
        path: List[List[_Coord]] = [[] for _ in range(len(vpoints))]
        for angle in range(360 + 1):
            try:
                result_list = expr_solving(
                    expr,
                    {i: f"P{i}" for i in range(len(vpoints))},
                    vpoints,
                    [base_angle + angle] + [0] * (len(input_list) - 1)
                )
            except ValueError:
                nan = float('nan')
                for i in range(len(vpoints)):
                    path[i].append((nan, nan))
            else:
                for i in range(len(vpoints)):
                    coord = result_list[i]
                    if type(coord[0]) is tuple:
                        path[i].append(cast(_Coord, coord[1]))
                    else:
                        path[i].append(cast(_Coord, coord))
        return path

    @Slot(name='on_result_clipboard_clicked')
    def __copy_result_text(self) -> None:
        """Copy pretty print result as text."""
        QApplication.clipboard().setText(
            pprint.pformat(self.mechanism_data[self.result_list.currentRow()])
        )

    @Slot(name='on_save_profile_clicked')
    def __save_profile(self) -> None:
        """Save as new profile to collection widget."""
        if not self.mech:
            return
        name, ok = QInputDialog.getText(
            self,
            "Profile name",
            "Please enter the profile name:"
        )
        if not ok:
            return
        i = 0
        while (not name) and (name not in self.collections):
            name = f"Structure_{i}"
            i += 1
        mech = deepcopy(self.mech)
        for key in ('placement', 'target'):
            for mp in mech[key]:
                mech[key][mp] = None
        self.collections[name] = mech
        self.project_no_save()

    @Slot(name='on_load_profile_clicked')
    def __load_profile(self) -> None:
        """Load profile from collections dialog."""
        dlg = CollectionsDialog(
            self.collections,
            self.get_collection,
            self.project_no_save,
            self.prefer.tick_mark_option,
            self.preview_canvas.monochrome,
            self
        )
        dlg.show()
        if not dlg.exec_():
            dlg.deleteLater()
            return
        params = dlg.params
        name = dlg.name
        dlg.deleteLater()
        del dlg
        # Check the profile
        if not (params['target'] and params['input'] and params['placement']):
            QMessageBox.warning(
                self,
                "Invalid profile",
                "The profile is not configured yet."
            )
            return
        self.__set_profile(name, params)

    def __set_profile(self, profile_name: str, params: Dict[str, Any]) -> None:
        """Set profile to sub-widgets."""
        self.__clear_settings()
        self.mech = deepcopy(params)
        expression: str = self.mech['expression']
        self.expression_string.setText(expression)
        target: Dict[int, List[_Coord]] = self.mech['target']
        for p in sorted(target):
            self.target_points.addItem(f"P{p}")
            if target[p]:
                self.path[p] = target[p].copy()
            else:
                self.path[p] = []
        if self.has_target():
            self.target_points.setCurrentRow(0)
        self.target_label.setVisible(self.has_target())
        # Parameter of link length and input angle.
        link_list = []
        for vlink in parse_vlinks(expression):
            if len(vlink.points) < 2 or vlink.name == VLink.FRAME:
                continue
            a = vlink.points[0]
            b = vlink.points[1]
            link_list.append((a, b))
            for c in vlink.points[2:]:
                for d in (a, b):
                    link_list.append((c, d))
        link_count = len(link_list)
        inputs: List[Tuple[Tuple[int, int], List[float]]] = self.mech['input']
        self.parameter_list.setRowCount(0)
        placement: Dict[int, Optional[Tuple[float, float, float]]] = self.mech['placement']
        # Table settings
        self.parameter_list.setRowCount(len(inputs) + len(placement) + link_count)
        row = 0

        def spinbox(
            v: float,
            *,
            minimum: float = 0.,
            maximum: float = 9999.,
            prefix: bool = False
        ) -> QDoubleSpinBox:
            double_spinbox = QDoubleSpinBox()
            double_spinbox.setMinimum(minimum)
            double_spinbox.setMaximum(maximum)
            double_spinbox.setValue(v)
            if prefix:
                double_spinbox.setPrefix("±")
            return double_spinbox

        def set_angle(index1: int, index2: int) -> Callable[[float], None]:
            """Return a slot function use to set angle value."""
            @Slot(float)
            def func(value: float) -> None:
                inputs[index1][1][index2] = value
            return func

        # Angles
        for i, ((b, d), se) in enumerate(inputs):
            self.parameter_list.setItem(row, 0, QTableWidgetItem(f"P{b}->P{d}"))
            self.parameter_list.setItem(row, 1, QTableWidgetItem('input'))
            s1 = spinbox(se[0], maximum=360.)
            s2 = spinbox(se[1], maximum=360.)
            self.parameter_list.setCellWidget(row, 2, s1)
            self.parameter_list.setCellWidget(row, 3, s2)
            s1.valueChanged.connect(set_angle(i, 0))
            s2.valueChanged.connect(set_angle(i, 1))
            row += 1

        # Grounded joints
        self.preview_canvas.from_profile(self.mech)
        pos_list = parse_pos(expression)
        for node, ref in sorted(self.preview_canvas.same.items()):
            pos_list.insert(node, pos_list[ref])
        for p in sorted(placement):
            coord = placement[p]
            self.parameter_list.setItem(row, 0, QTableWidgetItem(f"P{p}"))
            self.parameter_list.setItem(row, 1, QTableWidgetItem('placement'))
            x, y = self.preview_canvas.pos[p]
            for i, s in enumerate([
                spinbox(coord[0] if coord else x, minimum=-9999.),
                spinbox(coord[1] if coord else y, minimum=-9999.),
                spinbox(coord[2] if coord else 25., prefix=True),
            ]):
                s.valueChanged.connect(self.update_range)
                self.parameter_list.setCellWidget(row, i + 2, s)
            row += 1
        # Default value of upper and lower
        upper_list: List[float] = self.mech.get('upper', [0.] * link_count)
        lower_list: List[float] = self.mech.get('lower', [0.] * link_count)
        self.mech['upper'] = upper_list
        self.mech['lower'] = lower_list

        def set_by_center(
            index: int,
            get_range: Callable[[], float]
        ) -> Callable[[float], None]:
            """Return a slot function use to set limit value by center."""
            @Slot(float)
            def func(value: float) -> None:
                range_value = get_range()
                upper_list[index] = value + range_value
                lower_list[index] = value - range_value
            return func

        def set_by_range(
            index: int,
            get_value: Callable[[], float]
        ) -> Callable[[float], None]:
            """Return a slot function use to set limit value by range."""
            @Slot(float)
            def func(value: float) -> None:
                center = get_value()
                upper_list[index] = center + value
                lower_list[index] = center - value
            return func

        # Links
        for i, (a, b) in enumerate(sorted(link_list)):
            self.parameter_list.setItem(row, 0, QTableWidgetItem(f"P{a}<->P{b}"))
            link_length = self.preview_canvas.distance(a, b)
            self.parameter_list.setItem(row, 1, QTableWidgetItem('link'))
            # Set values
            if upper_list[i] == 0.:
                upper_list[i] = link_length + 50
            if lower_list[i] <= 0.:
                lower_list[i] = link_length - 50
                lower_list[i] = 0. if lower_list[i] < 0 else lower_list[i]
            # Spinbox
            error_range = (upper_list[i] - lower_list[i]) / 2
            s1 = spinbox(error_range + lower_list[i])
            s2 = spinbox(error_range, prefix=True)
            self.parameter_list.setCellWidget(row, 2, s1)
            self.parameter_list.setCellWidget(row, 4, s2)
            s1.valueChanged.connect(set_by_center(i, s2.value))
            s2.valueChanged.connect(set_by_range(i, s1.value))
            row += 1
        self.update_range()
        self.profile_name.setText(profile_name)
        # Default value of algorithm option.
        if 'settings' in self.mech:
            self.alg_options.update(self.mech['settings'])
        else:
            self.__set_algorithm_default()
        self.__able_to_generate()

    @Slot(name='on_result_load_settings_clicked')
    def __load_result_settings(self) -> None:
        """Load settings from a result."""
        self.__has_result()
        row = self.result_list.currentRow()
        if not row > -1:
            return
        self.__clear_settings()
        result = self.mechanism_data[row]
        for option, button in self.algorithm_options.items():
            if result['Algorithm'] == option.value:
                button.setChecked(True)
                break
        else:
            raise ValueError("no option")
        # Copy to mechanism params
        self.__set_profile("External setting", result)
        self.__set_time(result['time'])
        # Load settings
        self.alg_options.clear()
        self.alg_options.update(result['settings'])

    @Slot()
    def __set_algorithm_default(self) -> None:
        """Set the algorithm settings to default."""
        self.alg_options.clear()
        self.alg_options.update(DEFAULT_PARAMS)
        for option, button in self.algorithm_options.items():
            if button.isChecked():
                self.alg_options.update(PARAMS[option])

    @Slot(name='on_advance_button_clicked')
    def __show_advance(self) -> None:
        """Get the settings from advance dialog."""
        for option, button in self.algorithm_options.items():
            if button.isChecked():
                algorithm = option
                break
        else:
            raise ValueError("no option")
        dlg = AlgorithmOptionDialog(algorithm, self.alg_options, self)
        dlg.show()
        if not dlg.exec_():
            dlg.deleteLater()
            return
        self.alg_options['report'] = dlg.report.value()
        self.alg_options.pop('max_gen', None)
        self.alg_options.pop('min_fit', None)
        self.alg_options.pop('max_time', None)
        if dlg.max_gen_option.isChecked():
            self.alg_options['max_gen'] = dlg.max_gen.value()
        elif dlg.min_fit_option.isChecked():
            self.alg_options['min_fit'] = dlg.min_fit.value()
        elif dlg.max_time_option.isChecked():
            # Three spinbox value translate to second.
            self.alg_options['max_time'] = (
                dlg.max_time_h.value() * 3600
                + dlg.max_time_m.value() * 60
                + dlg.max_time_s.value()
            )
        else:
            raise ValueError("invalid option")
        pop_size = dlg.pop_size.value()
        if algorithm == AlgorithmType.RGA:
            self.alg_options['nPop'] = pop_size
        elif algorithm == AlgorithmType.Firefly:
            self.alg_options['n'] = pop_size
        elif algorithm == AlgorithmType.DE:
            self.alg_options['NP'] = pop_size
        elif algorithm == AlgorithmType.TLBO:
            self.alg_options['class_size'] = pop_size
        for row in range(dlg.alg_table.rowCount()):
            option = dlg.alg_table.item(row, 0).text()
            self.alg_options[option] = dlg.alg_table.cellWidget(row, 1).value()
        dlg.deleteLater()

    @Slot()
    def update_range(self) -> None:
        """Update range values to main canvas."""
        def t(x: int, y: int) -> Union[str, float]:
            item = self.parameter_list.item(x, y)
            if item is None:
                w: QDoubleSpinBox = self.parameter_list.cellWidget(x, y)
                return w.value()
            else:
                return item.text()

        self.update_ranges({
            cast(str, t(row, 0)): (
                cast(float, t(row, 2)),
                cast(float, t(row, 3)),
                cast(float, t(row, 4)),
            ) for row in range(self.parameter_list.rowCount())
            if t(row, 1) == 'placement'
        })

    @Slot(name='on_expr_copy_clicked')
    def __copy_expr(self) -> None:
        """Copy profile expression."""
        text = self.expression_string.text()
        if text:
            QApplication.clipboard().setText(text)
