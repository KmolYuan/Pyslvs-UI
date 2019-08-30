# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple,
    Sequence,
    Dict,
    Callable,
    Iterator,
    Union,
)
from abc import ABC
from lark.exceptions import LarkError
from pygments.lexers.python import Python3Lexer
from pyslvs import __version__, parse_params, PMKSLexer
from core.QtModules import (
    Slot,
    qt_image_format,
    QApplication,
    QWidget,
    QMessageBox,
    QDesktopServices,
    QUrl,
    QInputDialog,
    QFile,
    QFileInfo,
    QFileDialog,
    QProgressDialog,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QCheckBox,
    QLineEdit,
    QMimeData,
    QDragEnterEvent,
    QDropEvent,
)
from core.info import (
    ARGUMENTS,
    logger,
    PyslvsAbout,
    check_update,
    kernel_list,
)
from core.io import (
    ScriptDialog,
    slvs_process_script,
    SlvsParser,
    SlvsOutputDialog,
    DxfOutputDialog,
    str_between,
)
from core.widgets import AddTable, EditPointTable
from .actions import ActionMethodInterface

_PREFIX = f"# Generate by Pyslvs {__version__}\n# Project "
Settings: type = Union[int, float, bool, str]


class IOMethodInterface(ActionMethodInterface, ABC):

    """Abstract class for action methods."""

    def __v_to_slvs(self) -> Callable[[], Iterator[Tuple[int, int]]]:
        """Solvespace edges."""

        def func() -> Iterator[Tuple[int, int]]:
            for vlink in self.vlink_list:
                if vlink.name == 'ground':
                    continue
                for i, p in enumerate(vlink.points):
                    if i == 0:
                        continue
                    yield (vlink.points[0], p)
                    if i > 1:
                        yield (vlink.points[i-1], p)

        return func

    def __read_slvs(self, file_name: str):
        """Read slvs format.

        + Choose a group.
        + Read the entities of the group.
        """
        parser = SlvsParser(file_name)
        if not parser.is_valid():
            QMessageBox.warning(
                self,
                "Format error",
                "The format is not support."
            )
            return
        groups = parser.get_groups()
        if not groups:
            QMessageBox.warning(
                self,
                "Format error",
                "The model file is empty."
            )
            return
        group, ok = QInputDialog.getItem(
            self,
            "Solvespace groups",
            "Choose a group:\n"
            "(Please know that the group must contain a sketch only.)",
            ["@".join(g) for g in groups],
            0,
            False
        )
        if not ok:
            return
        self.clear()
        self.database_widget.reset()
        logger.debug(f"Read from group: {group}")
        self.parse_expression(parser.parse(group.split('@')[0]))

    def __settings(self) -> Tuple[Tuple[QWidget, Settings], ...]:
        """Give the settings of all option widgets."""
        return (
            (self.line_width_option, 3),
            (self.font_size_option, 14),
            (self.path_width_option, 3),
            (self.scalefactor_option, 10),
            (self.selection_radius_option, 10),
            (self.link_trans_option, 0),
            (self.margin_factor_option, 5),
            (self.joint_size_option, 5),
            (self.zoom_by_option, 0),
            (self.snap_option, 1),
            (self.background_option, ""),
            (self.background_opacity_option, 1),
            (self.background_scale_option, 1),
            (self.background_offset_x_option, 0),
            (self.background_offset_y_option, 0),
            (self.undo_limit_option, 32),
            (self.planar_solver_option, 0),
            (self.path_preview_option, self.path_preview_option.count() - 1),
            (self.title_full_path_option, False),
            (self.console_error_option, False),
            (self.monochrome_option, False),
            # "Do not save the settings" by default.
            (self.dontsave_option, True),
        )

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Drag file in to our window."""
        mime_data: QMimeData = event.mimeData()
        if not mime_data.hasUrls():
            return
        for url in mime_data.urls():
            suffix = QFileInfo(url.toLocalFile()).completeSuffix()
            if suffix in {'pyslvs.yml', 'pyslvs', 'slvs'}:
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        """Drop file in to our window."""
        file_name = event.mimeData().urls()[-1].toLocalFile()
        self.__load_file(file_name)
        event.acceptProposedAction()

    def workbook_no_save(self):
        """Workbook not saved signal."""
        self.database_widget.changed = True
        not_yet_saved = " (not yet saved)"
        self.setWindowTitle(
            self.windowTitle().replace(not_yet_saved, '') + not_yet_saved
        )

    def workbook_saved(self):
        """Workbook saved signal."""
        self.database_widget.changed = False
        self.__set_window_title_full_path()

    @Slot(name='on_title_full_path_option_clicked')
    def __set_window_title_full_path(self):
        """Set the option 'window title will show the full path'."""
        file_name = self.database_widget.file_name()
        if self.title_full_path_option.isChecked():
            title = file_name.absoluteFilePath()
        else:
            title = file_name.fileName()
        saved_text = " (not yet saved)" if self.database_widget.changed else ''
        self.setWindowTitle(f"Pyslvs - {title}{saved_text}")

    def __open_url(self, url: str):
        """Use to open link."""
        QDesktopServices.openUrl(QUrl(url))
        self.showMinimized()

    @Slot(name='on_action_mde_tw_triggered')
    def __show_help(self):
        """Open website: mde.tw"""
        self.__open_url("http://mde.tw")

    @Slot(name='on_action_pyslvs_com_triggered')
    def __show_dot_com(self):
        """Open website: pyslvs.com"""
        self.__open_url("http://www.pyslvs.com/blog/index.html")

    @Slot(name='on_action_github_repository_triggered')
    def __show_github(self):
        """Open website: Github repository"""
        self.__open_url("https://github.com/KmolYuan/Pyslvs-UI")

    @Slot(name='on_action_documentation_triggered')
    def __show_doc(self):
        """Open website: Readthedocs"""
        self.__open_url("https://pyslvs-ui.readthedocs.io")

    @Slot(name='on_action_about_triggered')
    def __about(self):
        """Open Pyslvs about."""
        dlg = PyslvsAbout(self)
        dlg.show()
        dlg.exec()
        dlg.deleteLater()

    @Slot(name='on_action_example_triggered')
    def __load_example(self):
        """Load examples from 'DatabaseWidget'. Return true if succeeded."""
        if self.database_widget.load_example():
            self.__show_expr()
            self.main_canvas.zoom_to_fit()

    @Slot(name='on_action_import_example_triggered')
    def __import_example(self):
        """Import a example and merge it to canvas."""
        self.database_widget.load_example(is_import=True)

    @Slot(name='on_action_new_workbook_triggered')
    def __new_workbook(self):
        """Create (Clean) a new workbook."""
        if self.check_file_changed():
            return
        self.clear()
        self.database_widget.reset()
        logger.info("Created a new workbook.")

    def clear(self):
        """Clear to create commit stage."""
        self.free_move_disable.trigger()
        self.mechanism_storage_name_tag.clear()
        self.mechanism_storage.clear()
        self.collection_tab_page.clear()
        self.structure_synthesis.clear()
        self.inputs_widget.clear()
        self.dimensional_synthesis.clear()
        self.entities_point.clear()
        self.entities_link.clear()
        self.vpoint_list.clear()
        self.vlink_list[1:] = []
        self.entities_expr.clear()
        self.solve()

    @Slot(name='on_action_import_pmks_url_triggered')
    def __import_pmks_url(self):
        """Load PMKS URL and turn it to expression."""
        url, ok = QInputDialog.getText(
            self,
            "PMKS URL input",
            "Please input link string:"
        )
        if not ok:
            return
        if not url:
            QMessageBox.warning(
                self,
                "Loading failed",
                "Your link is in an incorrect format."
            )
            return
        try:
            for s in url.split('?')[-1].split('&'):
                if 'mech=' in s:
                    expr = s.replace('mech=', '').split('|')
                    break
            else:
                raise ValueError

            text_list = [s for s in expr if s not in ('', " ", '\n')]
            expr.clear()
            while text_list:
                item = text_list.pop(0).split(',')[:-1]
                for i, e in enumerate(reversed(item)):
                    if e in {'R', 'P', 'RP'}:
                        t = -(i + 1)
                        break
                else:
                    raise ValueError
                links = item[:t]
                item = item[t:]
                type_text = f"{item[0]}:{item[-1]}" if item[0] != 'R' else 'R'
                links_text = ", ".join(links)
                expr.append(f"J[{type_text}, P[{item[1]}, {item[2]}], L[{links_text}]]")
            expr = "M[" + ", ".join(expr) + "]"
        except (ValueError, IndexError):
            QMessageBox.warning(
                self,
                "Loading failed",
                "Your link is in an incorrect format."
            )
        else:
            self.parse_expression(expr)

    def parse_expression(self, expr: str):
        """Parse expression."""
        try:
            args_list = parse_params(expr)
        except LarkError:
            QMessageBox.warning(
                self,
                "Loading failed",
                f"Your expression is in an incorrect format."
            )
        else:
            for args in args_list:
                links = args[0].split(',')
                link_names = {vlink.name for vlink in self.vlink_list}
                for link_name in links:
                    # If link name not exist.
                    if link_name not in link_names:
                        self.add_link(link_name, 'Blue')
                row_count = self.entities_point.rowCount()
                self.command_stack.beginMacro(f"Add {{Point{row_count}}}")
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

    def add_empty_links(self, link_color: Dict[str, str]):
        """Use to add empty link when loading database."""
        for name, color in link_color.items():
            if name != 'ground':
                self.add_link(name, color)

    @Slot(name='on_action_load_file_triggered')
    def __load_file(self, file_name: str = ""):
        """Load a supported format in Pyslvs."""
        if self.check_file_changed():
            return

        if not file_name:
            file_name = self.input_from("Workbook database", [
                "Pyslvs YAML file (*.pyslvs.yml)",
                "Pyslvs workbook (*.pyslvs)",
                "Solvespace module (*.slvs)",
            ])
            if not file_name:
                return

        suffix = QFileInfo(file_name).completeSuffix()
        if suffix == 'pyslvs.yml':
            self.yaml_editor.load(file_name)
        elif suffix == 'pyslvs':
            self.database_widget.read(file_name)
        elif suffix == 'slvs':
            self.__read_slvs(file_name)

        self.main_canvas.zoom_to_fit()

    @Slot(name='on_action_import_database_triggered')
    def __import_database(self):
        """Import from workbook."""
        if self.check_file_changed():
            return
        file_name = self.input_from(
            "Workbook database (Import)",
            ["Pyslvs workbook (*.pyslvs)"]
        )
        if not file_name:
            return
        self.database_widget.import_mechanism(file_name)

    @Slot(name='on_action_save_triggered')
    def save(self):
        """Save action. (YAML)"""
        if self.database_widget.file_name().completeSuffix() == 'pyslvs.yml':
            self.yaml_editor.save()
            self.workbook_saved()
        else:
            self.__save_as()

    @Slot(name='on_action_save_as_triggered')
    def __save_as(self):
        """Save as action. (YAML)"""
        file_name = self.output_to("YAML profile", ["Pyslvs YAML file (*.pyslvs.yml)"])
        if file_name:
            self.yaml_editor.save(file_name)
            self.workbook_saved()
            self.save_reply_box("YAML Profile", file_name)

    @Slot(name='on_action_commit_triggered')
    def commit(self, is_branch: bool = False):
        """Save action. (Database)"""
        file_name = self.database_widget.file_name().absoluteFilePath()
        if self.database_widget.file_name().suffix() == 'pyslvs':
            self.database_widget.save(file_name, is_branch)
        else:
            self.__commit_as(is_branch)

    @Slot(name='on_action_commit_as_triggered')
    def __commit_as(self, is_branch: bool = False):
        """Save as action. (Database)"""
        file_name = self.output_to("workbook", ["Pyslvs workbook (*.pyslvs)"])
        if file_name:
            self.database_widget.save(file_name, is_branch)
            self.save_reply_box("Workbook", file_name)

    @Slot(name='on_action_export_slvs_triggered')
    def __export_slvs(self):
        """Solvespace 2d save function."""
        dlg = SlvsOutputDialog(
            self.env,
            self.database_widget.file_name().baseName(),
            self.vpoint_list,
            self.__v_to_slvs(),
            self
        )
        dlg.show()
        if dlg.exec():
            path = dlg.path_edit.text() or dlg.path_edit.placeholderText()
            self.set_locate(path)
            self.save_reply_box("Solvespace sketch", path)

        dlg.deleteLater()

    @Slot(name='on_action_export_dxf_triggered')
    def __export_dxf(self):
        """DXF 2d save function."""
        dlg = DxfOutputDialog(
            self.env,
            self.database_widget.file_name().baseName(),
            self.vpoint_list,
            self.__v_to_slvs(),
            self
        )
        dlg.show()
        if dlg.exec():
            path = dlg.path_edit.text() or dlg.path_edit.placeholderText()
            self.set_locate(path)
            self.save_reply_box("Drawing Exchange Format", path)

        dlg.deleteLater()

    @Slot(name='on_action_export_image_triggered')
    def __export_image(self):
        """Picture save function."""
        pixmap = self.main_canvas.grab()
        file_name = self.output_to("picture", qt_image_format)
        if not file_name:
            return
        pixmap.save(file_name)
        self.save_reply_box("Picture", file_name)

    def output_to(self, format_name: str, format_choose: Sequence[str]) -> str:
        """Simple to support multiple format."""
        file_name, suffix = QFileDialog.getSaveFileName(
            self,
            f"Save to {format_name}...",
            self.env + '/' + self.database_widget.file_name().baseName(),
            ';;'.join(format_choose)
        )
        if file_name:
            suffix = str_between(suffix, '(', ')').split('*')[-1]
            logger.debug(f"Format: {suffix}")
            if QFileInfo(file_name).completeSuffix() != suffix[1:]:
                file_name += suffix
            self.set_locate(QFileInfo(file_name).absolutePath())
        return file_name

    def save_reply_box(self, title: str, file_name: str):
        """Show message when successfully saved."""
        size = QFileInfo(file_name).size()
        logger.debug("Size: " + (
            f"{size / 1024 / 1024:.02f} MB"
            if size / 1024 // 1024 else
            f"{size / 1024:.02f} KB"
        ))
        QMessageBox.information(
            self,
            f"Initial Saved: {title}",
            f"Successfully saved:\n{file_name}"
        )
        logger.info(f"Initial saved: [\"{file_name}\"]")

    def input_from(
        self,
        format_name: str,
        format_choose: Sequence[str],
        multiple: bool = False
    ) -> str:
        """Get file name(s)."""
        args = (
            f"Open {format_name} file{'s' if multiple else ''}...",
            self.env,
            ';;'.join(format_choose)
        )
        if multiple:
            file_name_s, suffix = QFileDialog.getOpenFileNames(self, *args)
        else:
            file_name_s, suffix = QFileDialog.getOpenFileName(self, *args)
        if file_name_s:
            suffix = str_between(suffix, '(', ')').split('*')[-1]
            logger.debug(f"Format: {suffix}")
            if type(file_name_s) is str:
                self.set_locate(QFileInfo(file_name_s).absolutePath())
            else:
                self.set_locate(QFileInfo(file_name_s[0]).absolutePath())
        return file_name_s

    @Slot(name='on_action_export_pmks_url_triggered')
    def __save_pmks(self):
        """Output to PMKS as URL."""
        url = "http://designengrlab.github.io/PMKS/pmks.html?mech="
        url_table = []
        for row in range(len(self.vpoint_list)):
            type_and_angle = self.entities_point.item(row, 2).text().split(':')
            point_data = [
                self.entities_point.item(row, 1).text(),
                type_and_angle[0],
                self.entities_point.item(row, 4).text(),
                self.entities_point.item(row, 5).text(),
            ]
            if len(type_and_angle) == 2:
                point_data.append(type_and_angle[1])
            point_data.append('tfff')
            url_table.append(','.join(point_data))
        url += '|'.join(url_table) + '|'
        text = '\n'.join((
            "Copy and past this link to web browser:\n",
            url + '\n',
            "If you have installed Microsoft Silverlight in "
            "Internet Explorer as default browser, "
            "just click \"Open\" button to open it in PMKS website."
        ))
        reply = QMessageBox.information(
            self,
            "PMKS web server",
            text,
            (QMessageBox.Save | QMessageBox.Open | QMessageBox.Close),
            QMessageBox.Save
        )
        if reply == QMessageBox.Open:
            self.__open_url(url)
        elif reply == QMessageBox.Save:
            QApplication.clipboard().setText(url)

    @Slot(name='on_action_export_image_clipboard_triggered')
    def __save_picture_clipboard(self):
        """Capture the canvas image to clipboard."""
        QApplication.clipboard().setPixmap(self.main_canvas.grab())
        QMessageBox.information(
            self,
            "Captured!",
            "Canvas widget picture is copy to clipboard."
        )

    @Slot(name='on_action_exprsion_triggered')
    def __show_expr(self):
        """Output as expression."""
        expr = [vpoint.expr() for vpoint in self.vpoint_list]
        context = ",\n".join(" " * 4 + e for e in expr)
        script = _PREFIX + f"\"{self.database_widget.file_name().baseName()}\"\n"
        if context:
            script += f"M[\n{context}\n]"
        else:
            script += "M[]"
        dlg = ScriptDialog(
            script,
            PMKSLexer(),
            "Pyslvs expression",
            ["Text file (*.txt)"],
            self,
            compressed_script="M[" + ','.join(expr).replace(", ", ",") + "]" if expr else ""
        )
        dlg.show()
        dlg.exec()
        dlg.deleteLater()

    @Slot(name='on_action_python_script_triggered')
    def __show_py_script(self):
        """Output to Python script for Jupyter notebook."""
        dlg = ScriptDialog(
            _PREFIX + f"\"{self.database_widget.file_name().baseName()}\"\n" +
            slvs_process_script(
                tuple(vpoint.expr() for vpoint in self.vpoint_list),
                tuple((b, d) for b, d, a in self.inputs_widget.input_pairs())
            ),
            Python3Lexer(),
            "Python script",
            ["Python3 Script (*.py)"],
            self
        )
        dlg.show()
        dlg.exec()
        dlg.deleteLater()

    @Slot(name='on_action_check_update_triggered')
    def __check_update(self):
        """Check for update."""
        dlg = QProgressDialog("Checking update ...", "Cancel", 0, 3, self)
        dlg.setWindowTitle("Check for update")
        dlg.resize(400, dlg.height())
        dlg.setModal(True)
        dlg.show()
        url = check_update(dlg)
        dlg.deleteLater()
        if url:
            if QMessageBox.question(
                self,
                "Pyslvs has update",
                "Do you want to get it from Github?"
            ) == QMessageBox.Yes:
                self.__open_url(url)
        else:
            QMessageBox.information(
                self,
                "Pyslvs is up to date",
                "You are using the latest version of Pyslvs."
            )

    def check_file_changed(self) -> bool:
        """If the user has not saved the change.

        Return True if user want to "discard" the operation.
        """
        if not self.database_widget.changed:
            return False

        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?\nAny changes won't be saved.",
            (QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel),
            QMessageBox.Save
        )
        if reply == QMessageBox.Save:
            self.save()
            return self.database_widget.changed
        elif reply == QMessageBox.Discard:
            return False
        return True

    def restore_settings(self):
        """Restore Pyslvs settings."""
        for widget, value in self.__settings():
            name = widget.objectName()
            widget_type = type(widget)
            if widget_type == QSpinBox:
                widget.setValue(self.settings.value(name, value, type=int))
            elif widget_type == QDoubleSpinBox:
                widget.setValue(self.settings.value(name, value, type=float))
            elif widget_type == QComboBox:
                widget.setCurrentIndex(self.settings.value(name, value, type=int))
            elif widget_type == QCheckBox:
                widget.setChecked(self.settings.value(name, value, type=bool))
            elif widget_type == QLineEdit:
                widget.setText(self.settings.value(name, value, type=str))
        # Specified solver setting.
        if ARGUMENTS.kernel:
            if ARGUMENTS.kernel == "python_solvespace":
                kernel_name = kernel_list[1]
            elif ARGUMENTS.kernel == "sketch_solve":
                kernel_name = kernel_list[2]
            elif ARGUMENTS.kernel == "pyslvs":
                kernel_name = kernel_list[0]
            else:
                raise ValueError("no such kernel")
            self.planar_solver_option.setCurrentText(kernel_name)
            self.path_preview_option.setCurrentText(kernel_name)

    def save_settings(self):
        """Save Pyslvs settings (auto save when close event)."""
        if self.dontsave_option.isChecked():
            f = QFile(self.settings.fileName())
            if f.exists():
                f.remove()
            return

        self.settings.setValue("ENV", self.env)
        for widget, value in self.__settings():
            name = widget.objectName()
            widget_type = type(widget)
            if widget_type in {QSpinBox, QDoubleSpinBox}:
                self.settings.setValue(name, widget.value())
            elif widget_type == QComboBox:
                self.settings.setValue(name, widget.currentIndex())
            elif widget_type == QCheckBox:
                self.settings.setValue(name, widget.isChecked())
            elif widget_type == QLineEdit:
                self.settings.setValue(name, widget.text())

    def reset_options(self):
        """Reset options with default value."""
        for widget, value in self.__settings():
            widget_type = type(widget)
            if widget_type in {QSpinBox, QDoubleSpinBox}:
                widget.setValue(value)
            elif widget_type == QComboBox:
                widget.setCurrentIndex(value)
            elif widget_type == QCheckBox:
                widget.setChecked(value)
            elif widget_type == QLineEdit:
                widget.setText(value)

    def load_from_args(self):
        if not ARGUMENTS.filepath:
            return
        suffix = QFileInfo(ARGUMENTS.filepath).suffix()
        if suffix == 'pyslvs':
            self.database_widget.read(ARGUMENTS.filepath)
        elif suffix == 'slvs':
            self.__read_slvs(ARGUMENTS.filepath)
        else:
            logger.critical("Unsupported format has been ignore when startup.")

    @Slot(int)
    def command_reload(self, index: int):
        """The time of withdrawal and redo action."""
        self.workbook_no_save()
        self.entities_point.clearSelection()
        self.inputs_widget.variable_reload()
        self.solve()
