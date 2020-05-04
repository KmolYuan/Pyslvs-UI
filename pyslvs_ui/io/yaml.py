# -*- coding: utf-8 -*-

"""YAML format processing function."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from re import sub
from yaml import safe_dump, safe_load
from .format_editor import FormatEditor


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
        yaml_script = safe_dump(data, default_flow_style=flow_style)
        if self.prefer.file_type_option == 1:
            yaml_script = sub(r"\s\s+", " ", yaml_script)
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(yaml_script)

    def load(self, file_name: str) -> None:
        """Load YAML file."""
        with open(file_name, 'r', encoding='utf-8') as f:
            yaml_script = f.read()
        self.load_data(file_name, safe_load(yaml_script))
