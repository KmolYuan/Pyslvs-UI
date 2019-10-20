# -*- coding: utf-8 -*-

"""The option dialog use to adjust target path."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QDialog
from .path_adjust_ui import Ui_Dialog
if TYPE_CHECKING:
    from pyslvs_ui.synthesis import DimensionalSynthesis


class PathAdjustDialog(QDialog, Ui_Dialog):

    """Option dialog.

    Only edit the target path after closed.
    """

    def __init__(self, parent: DimensionalSynthesis) -> None:
        """Just load in path data."""
        super(PathAdjustDialog, self).__init__(parent)
        self.setupUi(self)
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)
        # Get the current path from parent widget
        self.path = parent.current_path()
        self.clear_path = parent.clear_path
        self.add_point = parent.add_point
        for x, y in self.path:
            self.path_list.addItem(f"({x}, {y})")

    @Slot(name='on_scaling_button_clicked')
    def __scale(self) -> None:
        ox = self.scaling_rx.value()
        oy = self.scaling_ry.value()
        rx = self.scaling_rx.value()
        ry = self.scaling_ry.value()
        sh = self.scaling_h.value()
        sv = self.scaling_v.value()
        self.clear_path(ask=False)
        for x, y in self.path:
            self.add_point(ox + (x - rx) * sh, oy + (y - ry) * sv)
        self.accept()

    @Slot(name='on_moving_button_clicked')
    def __move(self) -> None:
        """Translate functions."""
        mx = self.moving_x_coordinate.value()
        my = self.moving_y_coordinate.value()
        self.clear_path(ask=False)
        for x, y in self.path:
            self.add_point(x + mx, y + my)
        self.accept()
