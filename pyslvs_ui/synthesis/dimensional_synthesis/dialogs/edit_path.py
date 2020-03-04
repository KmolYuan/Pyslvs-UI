# -*- coding: utf-8 -*-

"""The option dialog use to adjust target path."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING
from math import cos, sin, atan2, radians, hypot
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

    @Slot(name='on_move_button_clicked')
    def __move(self) -> None:
        """Translate function."""
        mx = self.move_x.value()
        my = self.move_y.value()
        self.set_path((x + mx, y + my) for x, y in self.path)
        self.accept()

    @Slot(name='on_rotate_button_clicked')
    def __rotate(self) -> None:
        """Rotate by origin."""
        angle = radians(self.rotate_angle.value())
        path = []
        for x, y in self.path:
            h = hypot(x, y)
            a = atan2(y, x) + angle
            path.append((h * cos(a), h * sin(a)))
        self.set_path(path)
        self.accept()

    @Slot(name='on_scale_button_clicked')
    def __scale(self) -> None:
        """Scale function."""
        ox = self.scale_rx.value()
        oy = self.scale_ry.value()
        rx = self.scale_rx.value()
        ry = self.scale_ry.value()
        sh = self.scale_h.value()
        sv = self.scale_v.value()
        self.set_path((ox + (x - rx) * sh, oy + (y - ry) * sv) for x, y in self.path)
        self.accept()

    @Slot(name='on_reduce_button_clicked')
    def __reduce(self) -> None:
        """Reduce function."""
        n = self.reduce_n.value()
        self.set_path(self.path[::n])
        self.accept()
