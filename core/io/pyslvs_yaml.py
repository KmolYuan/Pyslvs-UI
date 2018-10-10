# -*- coding: utf-8 -*-

"""YAML format processing function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Dict, Any
import yaml
from core.QtModules import QObject
from core import main_window as mn


class YamlEditor(QObject):

    """YAML reader and writer."""

    def __init__(self, parent: 'mn.MainWindow'):
        super(YamlEditor, self).__init__(parent)

        # Check file changed function.
        self.__check_file_changed = parent.checkFileChanged
        # Check workbook saved function.
        self.__workbook_saved = parent.workbookSaved

        # Call to get point expressions.
        self.__point_expr_func = parent.EntitiesPoint.expression
        # Call to get link data.
        self.__link_expr_func = parent.EntitiesLink.colors
        # Call to get storage data.
        self.__storage_data_func = parent.getStorage
        # Call to get collections data.
        self.__collect_data_func = parent.CollectionTabPage.collect_data
        # Call to get triangle data.
        self.__triangle_data_func = parent.CollectionTabPage.triangle_data
        # Call to get inputs variables data.
        self.__inputs_data_func = parent.InputsWidget.inputPairs
        # Call to get algorithm data.
        self.__algorithm_data_func = parent.DimensionalSynthesis.mechanism_data
        # Call to get path data.
        self.__path_data_func = parent.InputsWidget.pathData

        # Call to load collections data.
        self.__load_collect_func = parent.CollectionTabPage.StructureWidget.addCollections
        # Call to load triangle data.
        self.__load_triangle_func = parent.CollectionTabPage.TriangularIterationWidget.addCollections
        # Call to load inputs variables data.
        self.__load_inputs_func = parent.InputsWidget.addInputsVariables
        # Call after loaded algorithm results.
        self.__load_algorithm_func = parent.DimensionalSynthesis.loadResults
        # Call after loaded paths.
        self.__load_path_func = parent.InputsWidget.loadPaths
        # Add empty links function.
        self.__add_links_func = parent.addEmptyLinks
        # Parse function.
        self.__parse_func = parent.parseExpression
        # Clear function for main window.
        self.__clear_func = parent.clear
        # Add storage function.
        self.__add_storage_func = parent.addMultipleStorage

        self.file_name = ""

    def reset(self):
        """Reset some settings."""
        self.file_name = ""

    def save(self):
        """Save YAML file."""
        data = {}
        # TODO: Data structure.
        yaml_script = yaml.dump(data, default_flow_style=True)
        with open(self.file_name, 'w') as f:
            f.write(yaml_script)

    def save_as(self, file_name: str):
        """Save to a new YAML file."""
        self.file_name = file_name
        self.save()

    def load(self, file_name: str):
        """Load YAML file."""
        self.file_name = file_name
        with open(self.file_name) as f:
            yaml_script = f.read()
        data: Dict[str, Any] = yaml.load(yaml_script)
        # TODO: Load function.
