# -*- coding: utf-8 -*-

"""Chart dialog of Pyslvs.

This part is using PyQtChart module.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Sequence
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QVBoxLayout, QDialog
from numpy import ndarray
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)


class DataChart(QWidget):
    """Chart widget."""

    def __init__(self, parent: QWidget, row: int = 1, col: int = 1):
        """Input title and two axises, QChart class has no parent."""
        super(DataChart, self).__init__(parent)
        layout = QVBoxLayout(self)
        figure = Figure()
        canvas = FigureCanvasQTAgg(figure)
        layout.addWidget(NavigationToolbar2QT(canvas, self))
        layout.addWidget(canvas)
        ax = figure.subplots(row, col)
        if not isinstance(ax, ndarray):
            ax = (ax,)
        self._ax: Sequence[Axes] = ax

        def set_margin(m: float) -> None:
            figure.tight_layout(pad=m)

        self.set_margin = set_margin

    def ax(self) -> Sequence[Axes]:
        """Return figure."""
        return self._ax


class DataChartDialog(QDialog):
    """Dialog container."""

    def __init__(self, parent: QWidget, title: str, row: int = 1, col: int = 1):
        super(DataChartDialog, self).__init__(parent)
        self.setWindowFlags(
            self.windowFlags()
            & ~Qt.WindowContextHelpButtonHint
            | Qt.WindowMaximizeButtonHint
        )
        self.setWindowTitle(title)
        self.setModal(True)
        layout = QVBoxLayout(self)
        self._chart = DataChart(self, row, col)
        layout.addWidget(self._chart)

    def ax(self) -> Sequence[Axes]:
        """Wrapper method."""
        return self._chart.ax()

    def set_margin(self, m: float) -> None:
        """Wrapper method."""
        self._chart.set_margin(m)
