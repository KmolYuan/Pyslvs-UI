# -*- coding: utf-8 -*-

"""This module contains the preferences dialog."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Iterator
from dataclasses import fields, Field
from pyslvs_ui.core.widgets import MainWindowBase
from pyslvs_ui.core.QtModules import (
    Slot,
    qt_image_format,
    QDialog,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QComboBox,
    QDialogButtonBox,
)
from pyslvs_ui.core.info import kernel_list
from .preference_ui import Ui_Dialog


class PreferencesDialog(QDialog, Ui_Dialog):

    """Preference dialog."""

    def __init__(self, parent: MainWindowBase):
        super(PreferencesDialog, self).__init__(parent)
        self.setupUi(self)
        self.input_from = parent.input_from
        self.planar_solver_option.addItems(kernel_list)
        self.path_preview_option.addItems(kernel_list + ("Same as solver kernel",))
        self.prefer = parent.prefer
        self.prefer_origin = self.prefer.copy()

        self.accepted.connect(self.__save_settings)
        self.button_box.button(QDialogButtonBox.Apply).clicked.connect(self.__save_settings)
        self.button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.__reset)
        self.__load_settings()

    @Slot()
    def __reset(self) -> None:
        """Reset user options."""
        self.prefer.reset()
        self.__load_settings()

    @Slot()
    def __load_settings(self) -> None:
        """Load settings on UI."""
        for field in fields(self.prefer):  # type: Field
            widget = getattr(self, field.name)
            value = getattr(self.prefer, field.name)
            if type(widget) is QSpinBox or type(widget) is QDoubleSpinBox:
                widget.setValue(value)
            elif type(widget) is QLineEdit:
                widget.setText(value)
            elif type(widget) is QCheckBox:
                widget.setChecked(value)
            elif type(widget) is QComboBox:
                widget.setCurrentIndex(value)

    @Slot()
    def __save_settings(self):
        """Save settings after clicked apply."""
        for field in fields(self.prefer):  # type: Field
            widget = getattr(self, field.name)
            if type(widget) is QSpinBox or type(widget) is QDoubleSpinBox:
                setattr(self.prefer, field.name, widget.value())
            elif type(widget) is QLineEdit:
                setattr(self.prefer, field.name, widget.text())
            elif type(widget) is QCheckBox:
                setattr(self.prefer, field.name, widget.isChecked())
            elif type(widget) is QComboBox:
                setattr(self.prefer, field.name, widget.currentIndex())

    def diff(self) -> Iterator[str]:
        """Return the diff of two data."""
        if self.prefer == self.prefer_origin:
            return
        yield from self.prefer_origin.diff(self.prefer)

    @Slot(name='on_background_choose_dir_clicked')
    def __background_choose_dir(self) -> None:
        """Choose background directory."""
        file_name = self.input_from("background image", qt_image_format)
        if file_name:
            self.background_option.setText(file_name)
