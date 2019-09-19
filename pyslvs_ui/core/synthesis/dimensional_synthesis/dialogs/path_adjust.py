# -*- coding: utf-8 -*-

"""The option dialog use to adjust target path."""

from __future__ import annotations

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2019"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import TYPE_CHECKING, List, Tuple, Callable
import numpy as np
from qtpy.QtCore import Slot, Qt
from qtpy.QtWidgets import QDialog, QMessageBox
from .path_adjust_ui import Ui_Dialog
if TYPE_CHECKING:
    from pyslvs_ui.core.synthesis import DimensionalSynthesis


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

        # Get the current path from parent widget.
        self.path = parent.current_path()

        self.r_path = []
        for x, y in self.path:
            self.path_list.addItem(f"({x}, {y})")
        self.points_num.setText(str(len(self.path)))
        self.match_num.setValue(len(self.path))

    @Slot(name='on_scaling_button_clicked')
    def __scale(self) -> None:
        ox = self.scaling_rx.value()
        oy = self.scaling_ry.value()
        rx = self.scaling_rx.value()
        ry = self.scaling_ry.value()
        sh = self.scaling_h.value()
        sv = self.scaling_v.value()
        self.r_path = [
            (ox + (x - rx) * sh, oy + (y - ry) * sv) for x, y in self.path
        ]
        self.accept()

    @Slot(name='on_moving_button_clicked')
    def __move(self) -> None:
        """Translate functions."""
        mx = self.moving_x_coordinate.value()
        my = self.moving_y_coordinate.value()
        self.r_path = [(x + mx, y + my) for x, y in self.path]
        self.accept()

    @Slot(name='on_match_button_clicked')
    def __match(self) -> None:
        """Fitting function."""
        length = len(self.path)
        if length == 0:
            return
        index = list(range(length))

        def poly_fit(
            x: List[float],
            y: List[float],
            d: int
        ) -> Tuple[Callable[[float], float], float]:
            """Return a 2D fitting equation."""
            coefficient = np.polyfit(x, y, d)
            # Fit values and mean.
            y_hat = np.poly1d(coefficient)(x)
            y_bar: np.ndarray = np.sum(y) / len(y)

            def func(t: float) -> float:
                """Return y(x) function."""
                return sum(c * t**p for p, c in enumerate(reversed(coefficient)))

            yh_yb = y_hat - y_bar
            y_yb = y - y_bar
            return func, np.sum(yh_yb * yh_yb) / np.sum(y_yb * y_yb)

        x_func, x_accuracy = poly_fit(index, [x for x, y in self.path], 4)
        y_func, y_accuracy = poly_fit(index, [y for x, y in self.path], 4)
        QMessageBox.information(
            self,
            "Curve fitting",
            f"Accuracy:\nx: {x_accuracy:.02f}%\ny: {y_accuracy:.02f}%"
        )
        m = self.match_num.value()
        self.r_path = [(x_func(i / m * length), y_func(i / m * length)) for i in range(m)]
        self.accept()
