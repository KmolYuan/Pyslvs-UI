# -*- coding: utf-8 -*-

"""Chart dialog of Pyslvs.

This part is using PyQtChart module.
"""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from logging import WARNING, getLogger
from qtpy.QtWidgets import QWidget, QVBoxLayout, QDialog
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)

mpl_logger = getLogger('matplotlib')
mpl_logger.setLevel(WARNING)


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
        self._ax: Axes = figure.subplots(row, col)

    def ax(self) -> Axes:
        """Return figure."""
        return self._ax


class DataChartDialog(QDialog):
    """Dialog container."""

    def __init__(self, parent: QWidget, title: str, row: int = 1, col: int = 1):
        super(DataChartDialog, self).__init__(parent)
        self.setWindowTitle(title)
        layout = QVBoxLayout(self)
        self._chart = DataChart(self, row, col)
        layout.addWidget(self._chart)

    def ax(self) -> Axes:
        """Wrapper method."""
        return self._chart.ax()
