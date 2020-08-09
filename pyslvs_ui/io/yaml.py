# -*- coding: utf-8 -*-

"""YAML format processing function."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from re import sub
from numpy import float64
from yaml import safe_load, safe_dump
from yaml.representer import SafeRepresenter
from qtpy.QtWidgets import QMessageBox
from .format_editor import FormatEditor

# Add a patch for numpy numbers
SafeRepresenter.add_representer(float64, SafeRepresenter.represent_float)


class YamlEditor(FormatEditor):
    """YAML reader and writer."""

    def __init__(self, *args):
        super(YamlEditor, self).__init__(*args)

    def save(self, file_name: str) -> None:
        """Save YAML file."""
        data = self.save_data()
        if self.prefer.file_type_option == 0:
            flow_style = False
        elif self.prefer.file_type_option == 1:
            flow_style = True
        else:
            raise ValueError(f"unsupported option: {self.prefer.file_type_option}")
        try:
            yaml_script = safe_dump(data, default_flow_style=flow_style)
        except Exception as e:
            QMessageBox.warning(self._parent, "Save error", f"{e}")
            return
        if self.prefer.file_type_option == 1:
            yaml_script = sub(r"\s\s+", " ", yaml_script)
        with open(file_name, 'w+', encoding='utf-8') as f:
            f.write(yaml_script)

    def load(self, file_name: str) -> None:
        """Load YAML file."""
        with open(file_name, 'r', encoding='utf-8') as f:
            yaml_script = f.read()
        try:
            data = safe_load(yaml_script)
        except Exception as e:
            QMessageBox.warning(self._parent, "Loader error", f"{e}")
            return
        self.load_data(file_name, data)
