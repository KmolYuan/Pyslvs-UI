# -*- coding: utf-8 -*-

"""SQL database output function."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING
from datetime import datetime
from pyslvs import example_list
from core.QtModules import (
    Signal,
    QFileInfo,
    QWidget,
    QInputDialog,
)
from core.info import logger
from .Ui_database import Ui_Form
if TYPE_CHECKING:
    from core.widgets import MainWindowBase


class DatabaseWidget(QWidget, Ui_Form):

    """The table that stored workbook data and changes."""

    load_id = Signal(int)

    def __init__(self, parent: MainWindowBase):
        super(DatabaseWidget, self).__init__(parent)
        self.setupUi(self)

        # Check file changed function
        self.check_file_changed = parent.check_file_changed
        # Check workbook saved function
        self.workbook_saved = parent.workbook_saved

        # Call to get point expressions
        self.point_expr_func = lambda: "M[" + ", ".join(p.expr() for p in parent.vpoint_list) + "]"
        # Call to get link data
        self.link_color_func = lambda: {l.name: l.color_str for l in parent.vlink_list}
        # Call to get storage data
        self.storage_data_func = parent.get_storage
        # Call to get collections data
        self.collect_data_func = parent.collection_tab_page.collect_data
        # Call to get triangle data
        self.triangle_data_func = parent.collection_tab_page.triangle_data
        # Call to get inputs variables data
        self.inputs_data_func = parent.inputs_widget.input_pairs
        # Call to get algorithm data
        self.algorithm_data_func = lambda: parent.dimensional_synthesis.mechanism_data
        # Call to get path data
        self.path_data_func = parent.inputs_widget.path_data

        # Add empty links function
        self.add_links_func = parent.add_empty_links
        # Parse function
        self.parse_func = parent.parse_expression

        # Call to load inputs variables data
        self.load_inputs_func = parent.inputs_widget.add_inputs_variables
        # Add storage function
        self.add_storage_func = parent.add_multiple_storage
        # Call to load paths
        self.load_path_func = parent.inputs_widget.load_paths
        # Call to load collections data
        self.load_collect_func = parent.collection_tab_page.structure_widget.add_collections
        # Call to load triangle data
        self.load_triangle_func = parent.collection_tab_page.configure_widget.add_collections
        # Call to load algorithm results
        self.load_algorithm_func = parent.dimensional_synthesis.load_results

        # Clear function for main window
        self.clear_func = parent.clear

        # Undo Stack
        self.command_clear = parent.command_stack.clear
        # Reset
        self.history_commit = None
        self.__file_name = QFileInfo("Untitled")
        self.last_time = datetime.now()
        self.__changed = False
        self.reset()

    def reset(self):
        """Clear all the things that dependent on database."""
        self.__file_name = QFileInfo("Untitled")
        self.last_time = datetime.now()
        self.__changed = False
        self.command_clear()

    def set_file_name(self, file_name: str):
        """Set file name."""
        self.__file_name = QFileInfo(file_name)

    def file_name(self) -> QFileInfo:
        """Expose file name."""
        return self.__file_name

    def base_file_name(self) -> str:
        """Expose base file name."""
        return self.__file_name.baseName()

    def file_suffix(self) -> str:
        """Expose file name suffix."""
        return self.__file_name.completeSuffix()

    def set_changed(self, changed: bool):
        """Set file state."""
        self.__changed = changed

    def changed(self) -> bool:
        """Expose file state."""
        return self.__changed

    def save(self, file_name: str, is_branch: bool = False):
        """Save database, append commit to new branch function."""
        ...

    def read(self, file_name: str):
        """Load database commit."""
        ...

    def load_example(self, is_import: bool = False) -> bool:
        """Load example to new workbook."""
        if self.check_file_changed():
            return False
        # load example by expression.
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
            self.clear_func()
        self.parse_func(expr)
        if not is_import:
            # Import without input data.
            self.load_inputs_func(inputs)
        self.__file_name = QFileInfo(example_name)
        self.workbook_saved()
        logger.info(f"Example \"{example_name}\" has been loaded.")
        return True
