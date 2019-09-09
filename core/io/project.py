# -*- coding: utf-8 -*-

"""SQL database output function."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING
from pyslvs import example_list
from core.QtModules import (
    Signal,
    QUndoView,
    QFileInfo,
    QVBoxLayout,
    QWidget,
    QInputDialog,
    QMessageBox,
    QDateTime,
    QPixmap,
    QIcon,
)
from core.info import logger, size_format
from .pyslvs_yaml import YamlEditor
from .Ui_project import Ui_Form
if TYPE_CHECKING:
    from core.widgets import MainWindowBase


class ProjectWidget(QWidget, Ui_Form):

    """The table that stored workbook data and changes."""

    load_id = Signal(int)

    def __init__(self, parent: MainWindowBase) -> None:
        super(ProjectWidget, self).__init__(parent)
        self.setupUi(self)
        # Undo view
        undo_view = QUndoView(parent.command_stack)
        undo_view.setEmptyLabel("~ Start Pyslvs")
        w = QWidget(self)
        layout = QVBoxLayout(w)
        layout.addWidget(undo_view)
        history_icon = QIcon(QPixmap(":/icons/history.png"))
        self.history_tabs.addTab(w, history_icon, "Mechanism")
        # Check workbook saved function
        self.workbook_saved = parent.workbook_saved
        # Parse function
        self.parse_expression = parent.parse_expression
        # Call to load inputs variables data
        self.load_inputs = parent.inputs_widget.add_inputs_variables
        # Clear function for main window
        self.main_clear = parent.clear
        # Environment path
        self.env_path = parent.env_path

        self.overview_button.clicked.connect(parent.show_overview)
        self.ex_expression_button.clicked.connect(parent.show_expr)
        self.ex_dxf_button.clicked.connect(parent.export_dxf)
        self.ex_slvs_button.clicked.connect(parent.export_slvs)
        self.ex_pmks_button.clicked.connect(parent.save_pmks)
        self.ex_py_button.clicked.connect(parent.py_script)
        self.ex_image_button.clicked.connect(parent.export_image)
        self.ex_capture_button.clicked.connect(parent.save_picture_clipboard)

        self.im_pmks_button.clicked.connect(parent.import_pmks_url)
        self.im_example_button.clicked.connect(lambda: self.load_example(is_import=True))

        # YAML editor
        self.yaml_editor = YamlEditor(parent)
        # Undo Stack
        self.command_clear = parent.command_stack.clear
        # Reset
        self.__file_name = QFileInfo("")
        self.__changed = False
        self.reset()

    def reset(self) -> None:
        """Clear all the things that dependent on database."""
        self.set_file_name(self.env_path() + "/Untitled")
        self.__changed = False
        self.command_clear()

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
            t = "File"
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
        """Return True if the file is exist."""
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
        self.yaml_editor.save(file_name)
        self.set_file_name(file_name)

    def read(self, file_name: str) -> None:
        """Load database commit."""
        if not QFileInfo(file_name).isFile():
            QMessageBox.warning(self, "File not exist", "The path is invalid.")
            return
        self.yaml_editor.load(file_name)
        self.set_file_name(file_name)

    def load_example(self, is_import: bool = False) -> bool:
        """Load example to new workbook."""
        # load example by expression
        example_name, ok = QInputDialog.getItem(
            self,
            "Examples",
            "Select an example to load:",
            sorted(example_list),
            0,
            False
        )
        if not ok:
            return False
        expr, inputs = example_list[example_name]
        if not is_import:
            self.reset()
            self.main_clear()
        self.parse_expression(expr)
        if not is_import:
            # Import without input data
            self.load_inputs(inputs)
        self.set_file_name(example_name, is_example=True)
        self.workbook_saved()
        logger.info(f"Example \"{example_name}\" has been loaded.")
        return True
