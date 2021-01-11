# -*- coding: utf-8 -*-

"""Pickle format processing function."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from pickle import load, dump, UnpicklingError, HIGHEST_PROTOCOL
from qtpy.QtWidgets import QMessageBox
from .format_editor import FormatEditor


class PickleEditor(FormatEditor):
    """Pickle reader and writer."""

    def __init__(self, *args):
        super(PickleEditor, self).__init__(*args)

    @staticmethod
    def test(file_name: str) -> bool:
        """Test the file is valid."""
        try:
            with open(file_name, 'rb') as f:
                load(f)
        except (OSError, UnicodeError, UnpicklingError):
            return False
        else:
            return True

    def save(self, file_name: str) -> None:
        """Save to pickle file."""
        data = self.save_data()
        with open(file_name, 'wb') as f:
            dump(data, f, HIGHEST_PROTOCOL)

    def load(self, file_name: str) -> None:
        """Load a pickle file."""
        try:
            with open(file_name, 'rb') as f:
                data = load(f)
        except (OSError, UnicodeError, UnpicklingError) as e:
            QMessageBox.warning(self._parent, "Loader Error", f"{e}")
        self.load_data(file_name, data)
