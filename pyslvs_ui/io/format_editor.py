# -*- coding: utf-8 -*-

from __future__ import annotations

"""Genetic format processing editor."""

from abc import abstractmethod
from enum import unique, auto, IntEnum
from typing import (
    TYPE_CHECKING, Tuple, List, Sequence, Dict, Mapping, Union, Any,
)
from qtpy.QtCore import QObject, QFileInfo
from qtpy.QtWidgets import QProgressDialog, QMessageBox
from pyslvs_ui import __version__
from pyslvs_ui.qt_patch import QABCMeta
from pyslvs_ui.info import logger
from .overview import OverviewDialog

if TYPE_CHECKING:
    from pyslvs_ui.io import ProjectWidget
    from pyslvs_ui.widgets import MainWindowBase

_Coord = Tuple[float, float]
_Paths = Sequence[Sequence[_Coord]]
_SliderPaths = Mapping[int, Sequence[_Coord]]
_Pairs = Sequence[Tuple[int, int]]
_Data = Mapping[str, Any]


@unique
class ProjectFormat(IntEnum):
    """Project format."""
    YAML = 0
    C_YAML = auto()
    PICKLE = auto()

    @property
    def format_name(self):
        if self == ProjectFormat.YAML:
            return "YAML"
        elif self == ProjectFormat.C_YAML:
            return "Compressed YAML"
        elif self == ProjectFormat.PICKLE:
            return "Pickle"
        else:
            raise ValueError("invalid format")


class FormatEditor(QObject, metaclass=QABCMeta):
    """A generic loader and dumper."""
    dlg: Union[QProgressDialog, OverviewDialog, None]

    @abstractmethod
    def __init__(self, project_widget: ProjectWidget, parent: MainWindowBase):
        super(FormatEditor, self).__init__(parent)
        self._parent = parent
        # Undo stack
        self.command_stack = parent.cmd_stack
        # Action group settings
        self.prefer = parent.prefer
        # Point expressions
        self.get_expression = parent.get_expression
        # Link data
        self.vlinks = parent.vlink_list
        # Storage data
        self.get_storage = parent.get_storage
        # Collections data
        self.collect_data = parent.collections.collect_data
        # Triangle data
        self.config_data = parent.collections.config_data
        # Inputs variables data
        self.input_pairs = parent.inputs_widget.input_pairs
        # Algorithm data
        self.algorithm_data = parent.optimizer.mechanism_data
        # Path data
        self.paths = parent.inputs_widget.paths
        self.slider_paths = parent.inputs_widget.slider_paths
        # Background options
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
        self.load_collections = \
            parent.collections.structure_widget.add_collections
        # Call to load config data
        self.load_config = parent.collections.configure_widget.add_collections
        # Call to load algorithm results
        self.load_algorithm = parent.optimizer.load_results
        # Call to load background options
        self.set_background_config = project_widget.set_background_config
        # Clear function for main window
        self.main_clear = parent.clear
        # Dialog for loader
        self.dlg = None

    def save_data(self) -> _Data:
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
            'path': self.paths(),
            'slider_path': self.slider_paths(),
            'background': self.background_config(),
        }
        for k, v in tuple(data.items()):
            if not v:
                data.pop(k)
        return data

    def load_data(self, file_name: str, data: _Data) -> None:
        """Load file method."""
        self.main_clear()
        ver = data.get('pyslvs_ver', "")
        if ver:
            logger.info(f"Load data from version {ver}")
        del ver
        self.dlg = QProgressDialog("Loading project", "Cancel", 0, 7,
                                   self._parent)
        self.dlg.show()
        try:
            mechanism_data = self.__load_mech(data)
            storage_data = self.__load_storage(data)
            input_data = self.__load_input(data)
            paths = self.__load_path(data)
            collection_data = self.__load_collection(data)
            config_data = self.__load_config(data)
            algorithm_data = self.__load_algorithm(data)
            self.__load_background(data)
        except Exception as e:
            QMessageBox.warning(self._parent, "Load error", f"Exception:\n{e}")
            self.dlg.deleteLater()
            self.dlg = None
            return
        # File type option align (ignore previous one)
        self.prefer.file_type_option = data.get('file_type', ProjectFormat.YAML)
        # Show overview dialog
        self.dlg.deleteLater()
        self.dlg = OverviewDialog(
            self._parent,
            QFileInfo(file_name).baseName(),
            mechanism_data,
            storage_data,
            input_data,
            paths,
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

    def __load_mech(self, data: _Data) -> str:
        """Load mechanism data."""
        self.__process("mechanism")
        links_data: Mapping[str, str] = data.get('links', {})
        mechanism_data: str = data.get('mechanism', "M[]")
        if len(links_data) > 1 or mechanism_data != "M[]":
            self.__set_group("mechanism")
            self.add_empty_links(links_data)
            self.parse_expression(mechanism_data)
            self.__end_group()
        return mechanism_data

    def __load_input(self, data: _Data) -> List[Tuple[int, int]]:
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

    def __load_storage(self, data: _Data) -> Mapping[str, str]:
        """Load storage data."""
        self.__process("storage")
        storage_data: Mapping[str, str] = data.get('storage', {})
        if storage_data:
            self.__set_group("storage")
            self.load_storage(storage_data)
            self.__end_group()
        return storage_data

    def __load_path(self, data: _Data) -> Mapping[str, _Paths]:
        """Load path data."""
        self.__process("paths")
        paths: Mapping[str, _Paths] = data.get('path', {})
        slider_paths: Mapping[str, _SliderPaths] = data.get('slider_path', {})
        if paths:
            self.__set_group("paths")
            self.load_paths({
                n: [[(c[0], c[1]) for c in p] for p in ps]
                for n, ps in paths.items()
            }, slider_paths)
            self.__end_group()
        return paths

    def __load_collection(self, data: _Data) -> List[_Pairs]:
        """Load collection data."""
        self.__process("graph collections")
        collection_data: List[_Pairs] = data.get('collection', [])
        if collection_data:
            self.__set_group("graph collections")
            self.load_collections(collection_data)
            self.__end_group()
        return collection_data

    def __load_config(self, data: _Data) -> Mapping[str, _Data]:
        """Load synthesis configurations."""
        self.__process("synthesis configurations")
        config_data: Mapping[str, _Data] = data.get('triangle', {})
        if config_data:
            self.__set_group("synthesis configurations")
            self.load_config(config_data)
            self.__end_group()
        return config_data

    def __load_algorithm(self, data: _Data) -> Sequence[_Data]:
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

    def __load_background(self, data: _Data) -> None:
        """Set background."""
        self.__process("background")
        background: Mapping[str, Union[str, float]] = data.get('background', {})
        self.set_background_config(background)

    def __set_group(self, text: str) -> None:
        """Set group."""
        if self.prefer.open_project_actions_option == 1:
            self.command_stack.beginMacro(f"Add {text}")

    def __end_group(self) -> None:
        """End group."""
        if self.prefer.open_project_actions_option == 1:
            self.command_stack.endMacro()

    @staticmethod
    def test(file_name: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save(self, file_name: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def load(self, file_name: str) -> None:
        raise NotImplementedError
