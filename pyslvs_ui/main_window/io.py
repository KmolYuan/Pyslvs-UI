# -*- coding: utf-8 -*-

"""This module contains the functions that main window needed."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import (
    Tuple, List, Sequence, Mapping, Callable, Iterator, Union, Type,
)
from abc import ABC
from dataclasses import Field, fields
from lark.exceptions import LarkError
from qtpy.QtCore import Slot, QUrl, QFile, QFileInfo, QMimeData
from qtpy.QtWidgets import (
    QApplication,
    QMessageBox,
    QInputDialog,
    QFileDialog,
    QProgressDialog,
)
from qtpy.QtGui import (
    QDesktopServices,
    QPixmap,
    QIcon,
    QDragEnterEvent,
    QDropEvent,
)
from pyslvs import parse_params, VLink
from pyslvs_ui import __version__
from pyslvs_ui.qt_patch import qt_image_format, qt_image_suffix
from pyslvs_ui.info import (
    ARGUMENTS,
    logger,
    PyslvsAbout,
    check_update,
    size_format,
)
from pyslvs_ui.io import (
    ScriptDialog,
    slvs_process_script,
    SlvsParser,
    SlvsOutputDialog,
    DxfOutputDialog,
    OutputDialog,
    OverviewDialog,
    str_between,
)
from pyslvs_ui.widgets import AddTable, EditPointTable, Preferences
from .actions import ActionMethodInterface

_PREFIX = f"# Generate by Pyslvs {__version__}\n# Project "
Settings = Union[int, float, bool, str]


class IOMethodInterface(ActionMethodInterface, ABC):
    """Abstract class for action methods."""

    def __v_to_slvs(self) -> Callable[[], Iterator[Tuple[int, int]]]:
        """Solvespace edges."""

        def func() -> Iterator[Tuple[int, int]]:
            for vlink in self.vlink_list:
                if vlink.name == VLink.FRAME:
                    continue
                for i, p in enumerate(vlink.points):
                    if i == 0:
                        continue
                    yield vlink.points[0], p
                    if i > 1:
                        yield vlink.points[i - 1], p

        return func

    def __read_slvs(self, file_name: str) -> None:
        """Read slvs format.

        + Choose a group.
        + Read the entities of the group.
        """
        parser = SlvsParser(file_name)
        if not parser.is_valid():
            QMessageBox.warning(self, "Format error",
                                "The format is not support.")
            return
        groups = parser.get_groups()
        if not groups:
            QMessageBox.warning(self, "Format error",
                                "The model file is empty.")
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
        logger.debug(f"Read from group: {group}")
        self.parse_expression(parser.parse(group.split('@')[0]))

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Drag file in to our window."""
        mime_data: QMimeData = event.mimeData()
        if not mime_data.hasUrls():
            return
        urls = mime_data.urls()
        if len(urls) == 1:
            suffix = QFileInfo(urls[0].toLocalFile()).suffix().lower()
            if suffix in {'yml', 'pyslvs', 'slvs'} | set(qt_image_suffix):
                event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        """Drop file in to our window."""
        file = event.mimeData().urls()[0].toLocalFile()
        if QFileInfo(file).suffix().lower() in set(qt_image_suffix):
            self.project_widget.set_background_config({'background': file})
        else:
            self.__load_file(file)
        event.acceptProposedAction()

    def project_no_save(self) -> None:
        """Project not saved signal."""
        self.project_widget.set_changed(True)
        self.set_window_title_full_path()

    def project_saved(self) -> None:
        """Project saved signal."""
        self.project_widget.set_changed(False)
        self.set_window_title_full_path()

    def set_window_title_full_path(self) -> None:
        """Set the option 'window title will show the full path'."""
        file_name = self.project_widget.file_name()
        if self.prefer.title_full_path_option:
            title = file_name.absoluteFilePath()
        else:
            title = file_name.completeBaseName()
        self.setWindowTitle(
            f"Pyslvs - {title}{'*' if self.project_widget.changed() else ''}")

    def __open_url(self, url: str) -> None:
        """Use to open link."""
        QDesktopServices.openUrl(QUrl(url))
        self.showMinimized()

    @Slot(name='on_action_mde_tw_triggered')
    def __show_help(self) -> None:
        """Open website: mde.tw"""
        self.__open_url("http://mde.tw")

    @Slot(name='on_action_pyslvs_com_triggered')
    def __show_pyslvs_com(self) -> None:
        """Open website: pyslvs.com"""
        self.__open_url("http://www.pyslvs.com/content/index.html")

    @Slot(name='on_action_github_repository_triggered')
    def __show_github(self) -> None:
        """Open website: Github repository"""
        self.__open_url("https://github.com/KmolYuan/Pyslvs-UI")

    @Slot(name='on_action_documentation_triggered')
    def __show_doc(self) -> None:
        """Open website: Readthedocs"""
        self.__open_url("https://pyslvs-ui.readthedocs.io")

    @Slot(name='on_action_about_triggered')
    def __about(self) -> None:
        """Open Pyslvs about."""
        dlg = PyslvsAbout(self)
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()

    @Slot(name='on_action_example_triggered')
    def __load_example(self) -> None:
        """Load examples from "DatabaseWidget"."""
        if self.check_file_changed():
            return
        if self.project_widget.load_example():
            self.show_expr()
            self.main_canvas.zoom_to_fit()

    @Slot(name='on_action_new_project_triggered')
    def __new_project(self) -> None:
        """Create (Clean) a new project."""
        if self.check_file_changed():
            return
        self.clear()
        logger.info("Created a new project.")

    def clear(self) -> None:
        """Clear to create commit stage."""
        self.free_move_disable.trigger()
        self.mechanism_storage_name_tag.clear()
        self.mechanism_storage.clear()
        self.collections.clear()
        self.structure_synthesis.clear()
        self.inputs_widget.clear()
        self.optimizer.clear()
        self.entities_point.clear()
        self.entities_link.clear()
        self.vpoint_list.clear()
        self.vlink_list[1:] = []
        self.entities_expr.clear()
        self.solve()
        self.project_widget.reset()
        self.project_saved()

    @Slot()
    def import_pmks_url(self) -> None:
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
                expr.append(
                    f"J[{type_text}, P[{item[1]}, {item[2]}], L[{links_text}]]")
            expr = "M[" + ", ".join(expr) + "]"
        except (ValueError, IndexError):
            QMessageBox.warning(
                self,
                "Loading failed",
                "Your link is in an incorrect format."
            )
        else:
            self.parse_expression(expr)

    def parse_expression(self, expr: str) -> None:
        """Parse expression."""
        try:
            args_list = parse_params(expr)
        except LarkError:
            QMessageBox.warning(self, "Loading failed",
                                "Your expression is in an incorrect format.")
        else:
            for args in args_list:
                links = args.links.split(',')
                link_names = {vlink.name for vlink in self.vlink_list}
                for link_name in links:
                    # If link name not exist
                    if link_name not in link_names:
                        self.add_link(link_name, 'Blue')
                row_count = self.entities_point.rowCount()
                self.cmd_stack.beginMacro(f"Add {{Point{row_count}}}")
                self.cmd_stack.push(AddTable(
                    self.vpoint_list,
                    self.entities_point
                ))
                self.cmd_stack.push(EditPointTable(
                    row_count,
                    self.vpoint_list,
                    self.vlink_list,
                    self.entities_point,
                    self.entities_link,
                    args
                ))
                self.cmd_stack.endMacro()

    def add_empty_links(self, link_color: Mapping[str, str]) -> None:
        """Use to add empty link when loading database."""
        for name, color in link_color.items():
            if name != VLink.FRAME:
                self.add_link(name, color)

    @Slot(name='on_action_load_file_triggered')
    def __load_file(self, file_name: str = "") -> None:
        """Load a supported format in Pyslvs."""
        if self.check_file_changed():
            return

        if not file_name:
            file_name = self.input_from("project", [
                "Pyslvs project (*.pyslvs)",
                "Solvespace 2.x-3.x (*.slvs)",
            ])
            if not file_name:
                return

        suffix = QFileInfo(file_name).suffix().lower()
        if suffix == 'pyslvs':
            self.project_widget.read(file_name)
        elif suffix == 'slvs':
            self.__read_slvs(file_name)
        else:
            QMessageBox.warning(
                self,
                "Invalid file suffix",
                "Only support '*.pyslvs' or '*.slvs'."
            )
            return

        self.project_saved()
        self.main_canvas.zoom_to_fit()

    @Slot(name='on_action_save_triggered')
    def save(self) -> None:
        """Save action. (YAML)"""
        if self.project_widget.file_exist():
            self.project_widget.save()
            self.project_saved()
        else:
            self.__save_as()

    @Slot(name='on_action_save_as_triggered')
    def __save_as(self) -> None:
        """Save as action."""
        file_name = self.output_to("Pyslvs project",
                                   ["Pyslvs project (*.pyslvs)"])
        if not file_name:
            return
        self.project_widget.save(file_name)
        self.project_saved()
        self.save_reply_box("YAML Profile", file_name)

    def __cad_export(self, dialog: Type[OutputDialog], title: str) -> None:
        """Export to cad format."""
        dlg = dialog(self.env, self.project_widget.base_file_name(),
                     self.vpoint_list, self.__v_to_slvs(), self)
        dlg.show()
        if dlg.exec_():
            path = dlg.path_edit.text() or dlg.path_edit.placeholderText()
            self.set_locate(path)
            self.save_reply_box(title, path)
        dlg.deleteLater()

    @Slot()
    def export_slvs(self) -> None:
        """Solvespace 2d save function."""
        self.__cad_export(SlvsOutputDialog, "Solvespace sketch")

    @Slot()
    def export_dxf(self) -> None:
        """DXF 2d save function."""
        self.__cad_export(DxfOutputDialog, "Drawing Exchange Format")

    @Slot()
    def export_image(self) -> None:
        """Picture save function."""
        if self.prefer.grab_no_background_option:
            pixmap = self.main_canvas.grab_no_background()
        else:
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
            self.env + '/' + self.project_widget.base_file_name()
            + str_between(format_choose[0], '(', ')').split('*')[-1],
            ';;'.join(format_choose)
        )
        if file_name:
            suffix = str_between(suffix, '(', ')').split('*')[-1]
            logger.debug(f"Format: {suffix}")
            info = QFileInfo(file_name)
            if info.suffix().lower() != suffix[1:]:
                file_name += suffix
                info = QFileInfo(file_name)
                if info.isFile() and QMessageBox.question(
                    self,
                    "File exist",
                    f"{file_name} already exists.\nDo you want to replace it?"
                ) == QMessageBox.No:
                    return ""
            self.set_locate(info.absolutePath())
        return file_name

    def input_from(
        self,
        format_name: str,
        format_choose: Sequence[str]
    ) -> str:
        """Get external file name."""
        file_name, suffix = QFileDialog.getOpenFileName(
            self,
            f"Open {format_name}",
            self.env,
            ';;'.join(format_choose)
        )
        if file_name:
            self.set_locate(QFileInfo(file_name).absolutePath())
        return file_name

    def input_from_multiple(
        self,
        format_name: str,
        format_choose: Sequence[str]
    ) -> List[str]:
        """Get external file names."""
        file_names, suffix = QFileDialog.getOpenFileNames(
            self,
            f"Open {format_name} files ...",
            self.env,
            ';;'.join(format_choose)
        )
        if file_names:
            self.set_locate(QFileInfo(file_names[0]).absolutePath())
        return file_names

    def save_reply_box(self, title: str, file_name: str) -> None:
        """Show message when successfully saved."""
        size = size_format(QFileInfo(file_name).size())
        QMessageBox.information(
            self,
            f"Initial Saved: {title}",
            f"Successfully saved:\n{file_name}\n"
            f"Size: {size}"
        )
        logger.info(f"Saved: [\"{file_name}\"] ({size})")

    @Slot()
    def save_pmks(self) -> None:
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

    @Slot(name='on_action_screenshot_triggered')
    def save_picture_clipboard(self) -> None:
        """Capture the canvas image to clipboard."""
        if self.prefer.grab_no_background_option:
            pixmap = self.main_canvas.grab_no_background()
        else:
            pixmap = self.main_canvas.grab()
        QApplication.clipboard().setPixmap(pixmap)
        QMessageBox.information(
            self,
            "Captured!",
            "Canvas widget picture is copy to clipboard."
        )

    @Slot()
    def show_expr(self) -> None:
        """Output as expression."""
        dlg = ScriptDialog(
            QIcon(QPixmap("icons:id.png")),
            _PREFIX + f"\"{self.project_widget.base_file_name()}\"\n"
            + self.get_expression(indent=4),
            "Pyslvs expression",
            ["Text file (*.txt)"],
            self,
            compressed_script=self.get_expression().replace(", ", ",")
        )
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()

    @Slot()
    def py_script(self) -> None:
        """Output to Python script for Jupyter notebook."""
        dlg = ScriptDialog(
            QIcon(QPixmap("icons:script.png")),
            _PREFIX + f"\"{self.project_widget.base_file_name()}\"\n"
            + slvs_process_script(
                tuple(vpoint.expr() for vpoint in self.vpoint_list),
                tuple((b, d) for b, d, _ in self.inputs_widget.input_pairs())
            ),
            "Python script",
            ["Python3 Script (*.py)"],
            self,
            exprs=self.get_triangle().as_list()
        )
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()

    @Slot(name='on_action_check_update_triggered')
    def __check_update(self) -> None:
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

    @Slot(name='on_action_report_issue_triggered')
    def __report_issue(self) -> None:
        """Open website: Pyslvs issue page."""
        self.__open_url("https://github.com/KmolYuan/Pyslvs-UI/issues")

    def check_file_changed(self) -> bool:
        """If the user has not saved the change.

        Return True if user want to CANCEL the operation.
        """
        if not self.project_widget.changed():
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
            return self.project_widget.changed()
        elif reply == QMessageBox.Discard:
            return False
        return True

    def restore_settings(self) -> None:
        """Restore Pyslvs settings."""
        prefer = Preferences()
        for field in fields(prefer):  # type: Field
            setting = self.settings.value(field.name, field.default)
            setattr(prefer, field.name, setting)
        # Specified solver setting
        kernel = ARGUMENTS.kernel
        if kernel:
            if kernel == "python_solvespace":
                prefer.planar_solver_option = 1
            elif kernel == "sketch_solve":
                prefer.planar_solver_option = 2
            elif kernel == "pyslvs":
                prefer.planar_solver_option = 0
            else:
                QMessageBox.warning(
                    self,
                    "Kernel not found",
                    f"No such kernel: {kernel}"
                )
        self.apply_preferences(prefer, force=True)

    def save_settings(self) -> None:
        """Save Pyslvs settings (auto save when close event)."""
        if self.prefer.not_save_option:
            f = QFile(self.settings.fileName())
            if f.exists():
                f.remove()
            return
        self.settings.setValue("ENV", self.env)
        for field in fields(self.prefer):  # type: Field
            self.settings.setValue(field.name, getattr(self.prefer, field.name))

    def load_from_args(self) -> None:
        filepath = ARGUMENTS.filepath
        if not filepath:
            return
        suffix = QFileInfo(filepath).suffix().lower()
        if suffix == 'pyslvs':
            self.project_widget.read(filepath)
        elif suffix == 'slvs':
            self.__read_slvs(filepath)
        else:
            QMessageBox.warning(
                self,
                "Invalid file suffix",
                "Only support '*.pyslvs' or '*.slvs'."
            )

    @Slot(int)
    def command_reload(self, index: int) -> None:
        """The time of withdrawal and redo action."""
        self.project_no_save()
        self.entities_point.clearSelection()
        self.inputs_widget.variable_reload()
        self.solve()

    @Slot()
    def show_overview(self) -> None:
        """Show overview dialog."""
        dlg = OverviewDialog(
            self,
            self.project_widget.base_file_name(),
            self.get_expression(),
            self.get_storage(),
            [(b, d) for b, d, _ in self.inputs_widget.input_pairs()],
            self.inputs_widget.paths(),
            self.collections.collect_data(),
            self.collections.config_data(),
            self.optimizer.mechanism_data,
            self.project_widget.get_background_path()
        )
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()
