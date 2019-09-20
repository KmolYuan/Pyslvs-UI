# -*- coding: utf-8 -*-

from __future__ import annotations

"""Genetic format processing editor."""

from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Tuple,
    List,
    Sequence,
    Dict,
    Any,
)
from qtpy.QtCore import QObject, QFileInfo, QCoreApplication
from qtpy.QtWidgets import QProgressDialog
from pyslvs import __version__
from pyslvs_ui.core.qt_patch import QABCMeta
from pyslvs_ui.core.info import logger
from .overview import OverviewDialog
if TYPE_CHECKING:
    from pyslvs_ui.core.widgets import MainWindowBase

PROJECT_FORMAT = (
    "YAML",
    "Compressed YAML",
    "HDF5",
)


class FormatEditor(QObject, metaclass=QABCMeta):

    """Genetic reader and writer."""

    def __init__(self, parent: MainWindowBase) -> None:
        super(FormatEditor, self).__init__(parent)
        # Undo stack
        self.command_stack = parent.command_stack
        # Action group settings
        self.prefer = parent.prefer
        # Call to get point expressions
        self.vpoints = parent.vpoint_list
        # Call to get link data
        self.vlinks = parent.vlink_list
        # Call to get storage data
        self.get_storage = parent.get_storage
        # Call to get collections data
        self.collect_data = parent.collections.collect_data
        # Call to get triangle data
        self.config_data = parent.collections.config_data
        # Call to get inputs variables data
        self.input_pairs = parent.inputs_widget.input_pairs
        # Call to get algorithm data
        self.algorithm_data = parent.dimensional_synthesis.mechanism_data
        # Call to get path data
        self.path_data = parent.inputs_widget.path_data

        # Add empty links function
        self.add_empty_links = parent.add_empty_links
        # Add points function
        self.parse_expression = parent.parse_expression
        self.add_points = parent.add_points

        # Call to load inputs variables data
        self.load_inputs = parent.inputs_widget.add_inputs_variables
        # Add storage function
        self.load_storage = parent.add_multiple_storage
        # Call to load paths
        self.load_paths = parent.inputs_widget.load_paths
        # Call to load collections data
        self.load_collections = parent.collections.structure_widget.add_collections
        # Call to load config data
        self.load_config = parent.collections.configure_widget.add_collections
        # Call to load algorithm results
        self.load_algorithm = parent.dimensional_synthesis.load_results

        # Clear function for main window
        self.main_clear = parent.clear

    def save_data(self) -> Dict[str, Any]:
        """Save file method."""
        data = {
            'pyslvs_ver': __version__,
            'file_type': self.prefer.file_type_option,
            'mechanism': "M[" + ", ".join(p.expr() for p in self.vpoints) + "]",
            'links': {l.name: l.color_str for l in self.vlinks},
            'input': [(b, d) for b, d, _ in self.input_pairs()],
            'storage': self.get_storage(),
            'collection': self.collect_data(),
            'triangle': self.config_data(),
            'algorithm': self.algorithm_data,
            'path': self.path_data(),
        }
        for k, v in tuple(data.items()):
            if not v:
                data.pop(k)
        return data

    def load_data(self, file_name: str, data: Dict[str, Any]) -> None:
        """Load file method."""
        self.main_clear()
        ver = data.get('pyslvs_ver', "")
        if ver:
            logger.info(f"Load data from Pyslvs {ver}")
        del ver
        dlg = QProgressDialog("Loading project", "Cancel", 0, 8, self.parent())
        dlg.setLabelText("Reading file ...")
        dlg.show()

        # Mechanism data
        dlg.setValue(1)
        dlg.setLabelText("Loading mechanism ...")
        if dlg.wasCanceled():
            dlg.deleteLater()
            return self.main_clear()
        self.__set_group("Add mechanism")
        links_data: Dict[str, str] = data.get('links', {})
        self.add_empty_links(links_data)
        mechanism_data: str = data.get('mechanism', "")
        self.parse_expression(mechanism_data)
        self.__end_group()

        # Input data
        dlg.setValue(2)
        dlg.setLabelText("Loading inputs data ...")
        if dlg.wasCanceled():
            dlg.deleteLater()
            return self.main_clear()
        self.__set_group("Add inputs data")
        input_data: List[Dict[str, int]] = data.get('input', [])
        i_attr = []
        for b, d in input_data:
            QCoreApplication.processEvents()
            i_attr.append((b, d))
        self.load_inputs(i_attr)
        self.__end_group()

        # Storage data
        dlg.setValue(3)
        dlg.setLabelText("Loading storage ...")
        if dlg.wasCanceled():
            dlg.deleteLater()
            return self.main_clear()
        self.__set_group("Add storage")
        storage_data: Dict[str, str] = data.get('storage', {})
        self.load_storage(storage_data)
        self.__end_group()

        # Path data
        dlg.setValue(4)
        dlg.setLabelText("Loading paths ...")
        if dlg.wasCanceled():
            dlg.deleteLater()
            return self.main_clear()
        self.__set_group("Add paths")
        path_data: Dict[str, Sequence[Tuple[float, float]]] = data.get('path', {})
        self.load_paths(path_data)
        self.__end_group()

        # Collection data
        dlg.setValue(5)
        dlg.setLabelText("Loading graph collections ...")
        if dlg.wasCanceled():
            dlg.deleteLater()
            return self.main_clear()
        self.__set_group("Add graph collections")
        collection_data: List[Tuple[Tuple[int, int], ...]] = data.get('collection', [])
        self.load_collections(collection_data)
        self.__end_group()

        # Configuration data
        dlg.setValue(6)
        dlg.setLabelText("Loading synthesis configurations ...")
        if dlg.wasCanceled():
            dlg.deleteLater()
            return self.main_clear()
        self.__set_group("Add synthesis configurations")
        config_data: Dict[str, Dict[str, Any]] = data.get('triangle', {})
        self.load_config(config_data)
        self.__end_group()

        # Algorithm data
        dlg.setValue(7)
        dlg.setLabelText("Loading synthesis results ...")
        if dlg.wasCanceled():
            dlg.deleteLater()
            return self.main_clear()
        self.__set_group("Add synthesis results")
        algorithm_data: List[Dict[str, Any]] = data.get('algorithm', [])
        self.load_algorithm(algorithm_data)
        self.__end_group()

        # Workbook loaded
        dlg.setValue(8)
        dlg.deleteLater()

        # File type option align (ignore previous one)
        self.prefer.file_type_option = data.get('file_type', 0)

        # Show overview dialog
        dlg = OverviewDialog(
            self.parent(),
            QFileInfo(file_name).baseName(),
            storage_data,
            i_attr,
            path_data,
            collection_data,
            config_data,
            algorithm_data
        )
        dlg.show()
        dlg.exec_()
        dlg.deleteLater()

    def __set_group(self, text: str) -> None:
        """Set group."""
        if self.prefer.open_project_actions_option == 1:
            self.command_stack.beginMacro(text)

    def __end_group(self) -> None:
        """End group."""
        if self.prefer.open_project_actions_option == 1:
            self.command_stack.endMacro()

    @abstractmethod
    def save(self, file_name: str) -> None:
        ...

    @abstractmethod
    def load(self, file_name: str) -> None:
        ...
