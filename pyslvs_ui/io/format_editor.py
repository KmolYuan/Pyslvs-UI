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
    Union,
    Any,
)
from qtpy.QtCore import QObject, QFileInfo
from qtpy.QtWidgets import QProgressDialog, QMessageBox
from pyslvs import __version__
from pyslvs_ui.qt_patch import QABCMeta
from pyslvs_ui.info import logger
from .overview import OverviewDialog
if TYPE_CHECKING:
    from pyslvs_ui.io import ProjectWidget
    from pyslvs_ui.widgets import MainWindowBase

PROJECT_FORMAT = ("YAML", "Compressed YAML", "HDF5")
_Paths = Sequence[Sequence[Tuple[float, float]]]
_Pairs = Sequence[Tuple[int, int]]


class FormatEditor(QObject, metaclass=QABCMeta):
    """Generic loader and dumper."""

    def __init__(self, project_widget: ProjectWidget,
                 parent: MainWindowBase) -> None:
        super(FormatEditor, self).__init__(parent)
        # Undo stack
        self.command_stack = parent.command_stack
        # Action group settings
        self.prefer = parent.prefer
        # Call to get point expressions
        self.get_expression = parent.get_expression
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
        # Call to get background options
        self.background_config = project_widget.background_config
        self.get_background_path = project_widget.get_background_path

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
        # Call to load background options
        self.set_background_config = project_widget.set_background_config
        # Clear function for main window
        self.main_clear = parent.clear
        # Dialog for loader
        self.dlg: Union[QProgressDialog, OverviewDialog, None] = None

    def save_data(self) -> Dict[str, Any]:
        """Save file method."""
        data = {
            'pyslvs_ver': __version__,
            'file_type': self.prefer.file_type_option,
            'mechanism': self.get_expression(),
            'links': {link.name: link.color_str for link in self.vlinks},
            'input': [(b, d) for b, d, _ in self.input_pairs()],
            'storage': self.get_storage(),
            'collection': self.collect_data(),
            'triangle': self.config_data(),
            'algorithm': self.algorithm_data,
            'path': self.path_data(),
            'background': self.background_config(),
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
            logger.info(f"Load data from version {ver}")
        del ver
        self.dlg = QProgressDialog("Loading project", "Cancel", 0, 7, self.parent())
        self.dlg.show()
        try:
            mechanism_data = self.__load_mech(data)
            storage_data = self.__load_storage(data)
            input_data = self.__load_input(data)
            path_data = self.__load_path(data)
            collection_data = self.__load_collection(data)
            config_data = self.__load_config(data)
            algorithm_data = self.__load_algorithm(data)
            self.__load_background(data)
        except Exception as e:
            QMessageBox.warning(self.parent(), "Load error", f"Exception:\n{e}")
            self.dlg.deleteLater()
            self.dlg = None
            return
        # File type option align (ignore previous one)
        self.prefer.file_type_option = data.get('file_type', 0)
        # Show overview dialog
        self.dlg.deleteLater()
        self.dlg = OverviewDialog(
            self.parent(),
            QFileInfo(file_name).baseName(),
            mechanism_data,
            storage_data,
            input_data,
            path_data,
            collection_data,
            config_data,
            algorithm_data,
            self.get_background_path()
        )
        self.dlg.show()
        self.dlg.exec_()
        self.dlg.deleteLater()
        self.dlg = None

    def __process(self, title: str) -> None:
        """Increase progress."""
        if not isinstance(self.dlg, QProgressDialog):
            raise ValueError('not in process')
        self.dlg.setValue(self.dlg.value() + 1)
        self.dlg.setLabelText(f"Loading {title}.")
        if self.dlg.wasCanceled():
            self.dlg.deleteLater()
            self.main_clear()
            raise ValueError('load failed')

    def __load_mech(self, data: Dict[str, Any]) -> str:
        """Load mechanism data."""
        self.__process("mechanism")
        links_data: Dict[str, str] = data.get('links', {})
        mechanism_data: str = data.get('mechanism', "M[]")
        if len(links_data) > 1 or mechanism_data != "M[]":
            self.__set_group("mechanism")
            self.add_empty_links(links_data)
            self.parse_expression(mechanism_data)
            self.__end_group()
        return mechanism_data

    def __load_input(self, data: Dict[str, Any]) -> List[Tuple[int, int]]:
        """Load input data."""
        self.__process("input data")
        input_data: List[Sequence[int]] = data.get('input', [])
        # Assert input
        i_attr = [(i[0], i[1]) for i in input_data]
        if input_data:
            self.__set_group("inputs data")
            self.load_inputs(i_attr)
            self.__end_group()
        return i_attr

    def __load_storage(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Load storage data."""
        self.__process("storage")
        storage_data: Dict[str, str] = data.get('storage', {})
        if storage_data:
            self.__set_group("storage")
            self.load_storage(storage_data)
            self.__end_group()
        return storage_data

    def __load_path(self, data: Dict[str, Any]) -> Dict[str, _Paths]:
        """Load path data."""
        self.__process("paths")
        path_data: Dict[str, _Paths] = data.get('path', {})
        if path_data:
            self.__set_group("paths")
            self.load_paths({
                n: [[(c[0], c[1]) for c in p] for p in ps]
                for n, ps in path_data.items()
            })
            self.__end_group()
        return path_data

    def __load_collection(self, data: Dict[str, Any]) -> List[_Pairs]:
        """Load collection data."""
        self.__process("graph collections")
        collection_data: List[_Pairs] = data.get('collection', [])
        if collection_data:
            self.__set_group("graph collections")
            self.load_collections(collection_data)
            self.__end_group()
        return collection_data

    def __load_config(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Load synthesis configurations."""
        self.__process("synthesis configurations")
        config_data: Dict[str, Dict[str, Any]] = data.get('triangle', {})
        if config_data:
            self.__set_group("synthesis configurations")
            self.load_config(config_data)
            self.__end_group()
        return config_data

    def __load_algorithm(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Load algorithm data."""
        self.__process("synthesis results")
        algorithm_data: List[Dict[str, Any]] = data.get('algorithm', [])
        if algorithm_data:
            self.__set_group("synthesis results")
            # Assert input, it's a mappable object (consist of list)
            for config in algorithm_data:
                config['input'] = [((b, d), a) for (b, d), a in config['input']]
            self.load_algorithm(algorithm_data)
            self.__end_group()
        return algorithm_data

    def __load_background(self, data: Dict[str, Any]) -> None:
        """Set background."""
        self.__process("background")
        background: Dict[str, Union[str, float]] = data.get('background', {})
        self.set_background_config(background)

    def __set_group(self, text: str) -> None:
        """Set group."""
        if self.prefer.open_project_actions_option == 1:
            self.command_stack.beginMacro(f"Add {text}")

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
