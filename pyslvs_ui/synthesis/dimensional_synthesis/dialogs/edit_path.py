# -*- coding: utf-8 -*-

"""The option dialog use to adjust target path."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING
from math import cos, sin, atan2, radians, hypot
from numpy import array, linspace
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QDialog
from pyslvs import efd_fitting
from pyslvs_ui.info import HAS_SCIPY
from .edit_path_ui import Ui_Dialog

if TYPE_CHECKING:
    from pyslvs_ui.synthesis import DimensionalSynthesis
if HAS_SCIPY:
    from scipy.interpolate import splprep, splev


class EditPathDialog(QDialog, Ui_Dialog):
    """Option dialog.

    Only edit the target path after closed.
    """

    def __init__(self, parent: DimensionalSynthesis):
        """Just load in path data."""
        super(EditPathDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags()
                            & ~Qt.WindowContextHelpButtonHint)
        # Get the current path from parent widget
        self.path = parent.current_path().copy()
        self.set_path = parent.set_path
        # GUI settings
        self.bspline_option.setEnabled(HAS_SCIPY)
        self.efd_option.toggled.connect(self.close_path_option.toggle)
        self.efd_option.toggled.connect(self.close_path_option.setDisabled)
        self.num_points.setValue(len(self.path))

    @Slot(name='on_fitting_button_clicked')
    def __fitting(self) -> None:
        """Curve fitting function."""
        num = self.num_points.value()
        if self.bspline_option.isChecked():
            is_close = self.close_path_option.isChecked()
            path = array(self.path + self.path[:1]
                         if is_close else self.path, dtype=float)
            tck = splprep((path[:, 0], path[:, 1]), per=is_close)
            u = linspace(0, 1, num, endpoint=not is_close)
            self.set_path(zip(*splev(u, tck[0])))
        else:
            self.set_path(efd_fitting(self.path, num))
        self.accept()

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
        self.set_path((ox + (x - rx) * sh, oy + (y - ry) * sv)
                      for x, y in self.path)
        self.accept()
