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
from .edit_path_ui import Ui_Dialog
if TYPE_CHECKING:
    from pyslvs_ui.synthesis import DimensionalSynthesis


class EditPathDialog(QDialog, Ui_Dialog):

    """Option dialog.

    Only edit the target path after closed.
    """

    def __init__(self, parent: DimensionalSynthesis) -> None:
        """Just load in path data."""
        super(EditPathDialog, self).__init__(parent)
        self.setupUi(self)
        flags = self.windowFlags()
        self.setWindowFlags(flags & ~Qt.WindowContextHelpButtonHint)
        # Get the current path from parent widget
        self.path = parent.current_path().copy()
        self.set_path = parent.set_path
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
        self.set_path((ox + (x - rx) * sh, oy + (y - ry) * sv) for x, y in self.path)
        self.accept()

    @Slot(name='on_moving_button_clicked')
    def __move(self) -> None:
        """Translate functions."""
        mx = self.moving_x_coordinate.value()
        my = self.moving_y_coordinate.value()
        self.set_path((x + mx, y + my) for x, y in self.path)
        self.accept()
