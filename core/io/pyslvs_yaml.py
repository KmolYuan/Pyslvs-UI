# -*- coding: utf-8 -*-

"""YAML format processing function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

import yaml
from core.QtModules import QObject
from core import main_window as mn


class YamlEditor(QObject):

    """YAML reader and writer."""

    def __init__(self, parent: 'mn.MainWindow'):
        super(YamlEditor, self).__init__(parent)
        self.file_name = ""

    def reset(self):
        """Reset some settings."""
        self.file_name = ""

    def save(self):
        """Save YAML file."""

    def save_as(self, file_name: str):
        """Save to a new YAML file."""

    def load(self, file_name: str):
        """Load YAML file."""
        self.file_name = file_name
