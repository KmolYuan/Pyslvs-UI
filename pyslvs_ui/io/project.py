# -*- coding: utf-8 -*-

"""SQL database output function."""

from __future__ import annotations

__all__ = ['ProjectFormat', 'ProjectWidget']
__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING, Mapping, Union
from os.path import join
from qtpy.QtCore import Slot, QFileInfo, QDateTime
from qtpy.QtWidgets import (
    QUndoView,
    QVBoxLayout,
    QWidget,
    QInputDialog,
    QMessageBox,
)
from qtpy.QtGui import QPixmap, QIcon
from pyslvs import example_list, all_examples
from pyslvs_ui.info import logger, size_format
from pyslvs_ui.qt_patch import qt_image_format
from .project_yaml import YamlEditor
from .project_pickle import PickleEditor
from .project_ui import Ui_Form
from .format_editor import ProjectFormat

if TYPE_CHECKING:
    from pyslvs_ui.widgets import MainWindowBase


class ProjectWidget(QWidget, Ui_Form):
    """The table that stored project data and changes."""

    def __init__(self, parent: MainWindowBase):
        super(ProjectWidget, self).__init__(parent)
        self.setupUi(self)
        # Undo view
        self.command_stack = parent.cmd_stack
        undo_view = QUndoView(self.command_stack)
        undo_view.setEmptyLabel("~Start Pyslvs")
        w = QWidget(self)
        layout = QVBoxLayout(w)
        layout.addWidget(undo_view)
        history_icon = QIcon(QPixmap("icons:history.png"))
        self.history_tabs.addTab(w, history_icon, "Mechanism")
        # Settings
        self.prefer = parent.prefer
        # Check project saved function
        self.project_saved = parent.project_saved
        # Open file dialog
        self.input_from = parent.input_from
        # Parse function
        self.parse_expression = parent.parse_expression
        # Call to load inputs variables data
        self.load_inputs = parent.inputs_widget.add_inputs_variables
        # Clear function for main window
        self.main_clear = parent.clear
        # Environment path
        self.env_path = parent.env_path

        self.overview_btn.clicked.connect(parent.show_overview)
        self.ex_expression_btn.clicked.connect(parent.show_expr)
        self.ex_dxf_btn.clicked.connect(parent.export_dxf)
        self.ex_slvs_btn.clicked.connect(parent.export_slvs)
        self.ex_pmks_btn.clicked.connect(parent.save_pmks)
        self.ex_py_btn.clicked.connect(parent.py_script)
        self.ex_image_btn.clicked.connect(parent.export_image)
        self.ex_capture_btn.clicked.connect(parent.save_picture_clipboard)

        self.im_pmks_btn.clicked.connect(parent.import_pmks_url)
        self.im_example_btn.clicked.connect(lambda: self.load_example(is_import=True))

        self.background_option.textChanged.connect(parent.main_canvas.set_background)
        self.background_opacity_option.valueChanged.connect(parent.main_canvas.set_background_opacity)
        self.background_x_option.valueChanged.connect(parent.main_canvas.set_background_offset_x)
        self.background_y_option.valueChanged.connect(parent.main_canvas.set_background_offset_y)
        self.background_scale_option.valueChanged.connect(parent.main_canvas.set_background_scale)

        # Editors
        self.yaml_editor = YamlEditor(self, parent)
        self.pickle_editor = PickleEditor(self, parent)
        # Reset
        self.__file_name = QFileInfo()
        self.__changed = False
        self.reset()

    def reset(self) -> None:
        """Clear all the things that dependent on database."""
        self.set_file_name(join(self.env_path(), "Untitled"))
        self.__changed = False
        self.command_stack.clear()
        self.command_stack.setUndoLimit(self.prefer.undo_limit_option)
        self.set_background_config({})

    def set_file_name(self, file_name: str, *, is_example: bool = False) -> None:
        """Set file name."""
        self.__file_name = QFileInfo(file_name)
        self.file_name_label.setText(self.__file_name.fileName())
        self.path_label.setText(self.__file_name.absolutePath())
        self.owner_label.setText(self.__file_name.owner())
        time: QDateTime = self.__file_name.lastModified()
        self.last_modified_label.setText(time.toString())
        self.file_size_label.setText(size_format(self.__file_name.size()))
        if is_example:
            t = "Example (In memory)"
        elif self.file_exist():
            t = f"File ({self.prefer.file_type_option.format_name})"
        else:
            t = "In memory"
        self.type_label.setText(t)

    def file_name(self) -> QFileInfo:
        """Expose file name."""
        return self.__file_name

    def file_path(self) -> str:
        """Expose absolute file path."""
        return self.__file_name.absoluteFilePath()

    def base_file_name(self) -> str:
        """Expose base file name."""
        return self.__file_name.baseName()

    def file_suffix(self) -> str:
        """Expose file name suffix."""
        return self.__file_name.suffix()

    def file_exist(self) -> bool:
        """Return true if the file is exist."""
        return self.__file_name.isFile()

    def set_changed(self, changed: bool) -> None:
        """Set file state."""
        self.__changed = changed

    def changed(self) -> bool:
        """Expose file state."""
        return self.__changed

    def save(self, file_name: str = "") -> None:
        """Save database, append commit to new branch function."""
        if not file_name:
            file_name = self.file_path()
        if self.prefer.file_type_option == ProjectFormat.PICKLE:
            self.pickle_editor.save(file_name)
        else:
            self.yaml_editor.save(file_name)
        self.set_file_name(file_name)

    def read(self, file_name: str) -> None:
        """Load database commit."""
        if not QFileInfo(file_name).isFile():
            QMessageBox.warning(self, "File not exist", "The path is invalid.")
            return
        if YamlEditor.test(file_name):
            self.yaml_editor.load(file_name)
        else:
            self.pickle_editor.load(file_name)
        if self.prefer.open_project_actions_option == 0:
            self.command_stack.clear()
            self.command_stack.setUndoLimit(self.prefer.undo_limit_option)
        self.set_file_name(file_name)

    def load_example(self, is_import: bool = False) -> bool:
        """Load example to new project."""
        # load example by expression
        example_name, ok = QInputDialog.getItem(
            self,
            "Examples",
            "Select an example to load:",
            all_examples(),
            0,
            False
        )
        if not ok:
            return False
        if not is_import:
            self.reset()
            self.main_clear()
            if self.prefer.open_project_actions_option == 1:
                self.command_stack.beginMacro("Add mechanism")
        expr, inputs = example_list(example_name)
        self.parse_expression(expr)
        if not is_import:
            if self.prefer.open_project_actions_option == 1:
                self.command_stack.endMacro()
                self.command_stack.beginMacro("Add inputs data")
            # Import without inputs data
            self.load_inputs(inputs)
            if self.prefer.open_project_actions_option == 0:
                self.command_stack.clear()
                self.command_stack.setUndoLimit(self.prefer.undo_limit_option)
            elif self.prefer.open_project_actions_option == 1:
                self.command_stack.endMacro()
        self.set_file_name(example_name, is_example=True)
        self.project_saved()
        logger.info(f"Example \"{example_name}\" has been loaded.")
        return True

    @Slot(name='on_background_choose_dir_clicked')
    def __background_choose_dir(self) -> None:
        """Choose background directory."""
        file_name = self.input_from("background image", qt_image_format)
        if file_name:
            self.background_option.setText(file_name)

    def background_config(self) -> Mapping[str, Union[str, float]]:
        """Return background config."""
        env = self.__file_name.absoluteDir()
        return {
            'background': env.relativeFilePath(self.background_option.text()),
            'background_x': self.background_x_option.value(),
            'background_y': self.background_y_option.value(),
            'background_scale': self.background_scale_option.value(),
            'background_opacity': self.background_opacity_option.value(),
        }

    def set_background_config(self, config: Mapping[str, Union[str, float]]) -> None:
        """Set background config by dict object."""
        env = self.__file_name.absoluteDir()
        file = QFileInfo(env, config.get('background', ""))
        path = file.absoluteFilePath()
        self.background_option.setText(path if file.isFile() else "")
        self.background_x_option.setValue(config.get('background_x', 0.))
        self.background_y_option.setValue(config.get('background_y', 0.))
        self.background_scale_option.setValue(config.get('background_scale', 1.))
        self.background_opacity_option.setValue(config.get('background_opacity', 1.))

    def get_background_path(self) -> str:
        """Get background path."""
        path = self.background_option.text()
        return path if QFileInfo(path).isFile() else ""
