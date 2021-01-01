# -*- coding: utf-8 -*-

"""The functions of the entities dialogs."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from qtpy.QtWidgets import QComboBox
from qtpy.QtGui import QColor
from pyslvs_ui.graphics import color_icon


def set_custom_color(color_box: QComboBox, color_text: str):
    color_index = color_box.findText(color_text)
    if color_index > -1:
        color_box.setCurrentIndex(color_index)
    else:
        color_box.addItem(color_icon(color_text), color_text)
        color_box.setCurrentIndex(color_box.count() - 1)


def add_custom_color(color_box: QComboBox, color: QColor):
    rgb_str = f"({color.red()}, {color.green()}, {color.blue()})"
    color_box.addItem(color_icon(rgb_str), rgb_str)
    color_box.setCurrentIndex(color_box.count() - 1)
