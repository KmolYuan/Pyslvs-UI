# -*- coding: utf-8 -*-

"""YAML format processing function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import cast, Type
from re import sub
from numpy import float64
from yaml import safe_load, safe_dump
from yaml.error import YAMLError
from yaml.representer import SafeRepresenter
from qtpy.QtWidgets import QMessageBox
from .format_editor import FormatEditor, ProjectFormat

# Add a patch for numpy numbers
SafeRepresenter.add_representer(cast(Type[float], float64),
                                SafeRepresenter.represent_float)


class YamlEditor(FormatEditor):
    """YAML reader and writer."""

    def __init__(self, *args):
        super(YamlEditor, self).__init__(*args)

    @staticmethod
    def test(file_name: str) -> bool:
        """Test the file is valid."""
        with open(file_name, 'r', encoding='utf-8') as f:
            try:
                yaml_script = f.read()
                safe_load(yaml_script)
            except (OSError, UnicodeError, YAMLError):
                return False
            else:
                return True

    def save(self, file_name: str) -> None:
        """Save to YAML file."""
        data = self.save_data()
        opt = self.prefer.file_type_option
        if opt == ProjectFormat.YAML:
            flow_style = False
        elif opt == ProjectFormat.C_YAML:
            flow_style = True
        else:
            raise ValueError(f"unsupported option: {opt}")
        try:
            yaml_script = safe_dump(data, default_flow_style=flow_style)
        except Exception as e:
            QMessageBox.warning(self._parent, "Save error", f"{e}")
            return
        if self.prefer.file_type_option == ProjectFormat.C_YAML:
            yaml_script = sub(r"\s\s+", " ", yaml_script)
        with open(file_name, 'w+', encoding='utf-8') as f:
            f.write(yaml_script)

    def load(self, file_name: str) -> None:
        """Load a YAML file."""
        with open(file_name, 'r', encoding='utf-8') as f:
            yaml_script = f.read()
        try:
            data = safe_load(yaml_script)
        except (OSError, UnicodeError, YAMLError) as e:
            QMessageBox.warning(self._parent, "Loader Error", f"{e}")
            return
        self.load_data(file_name, data)
