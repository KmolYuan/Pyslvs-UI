# -*- coding: utf-8 -*-

"""The chart dialog of dimensional synthesis result."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2021"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import Sequence, Mapping, Any
from numpy import array
from qtpy.QtCore import Qt, QSize
from qtpy.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget
from pyslvs_ui.graphics import DataChart


class ChartDialog(QDialog):
    """There are three charts in the dialog.

    + Fitness / Generation Chart.
    + Generation / Time Chart.
    + Fitness / Time Chart.
    """

    def __init__(
        self,
        title: str,
        algorithm_data: Sequence[Mapping[str, Any]],
        parent: QWidget
    ):
        """Add three tabs of chart."""
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle("Fitness-Generation-Time Charts")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        self.title = title
        self.algorithm_data = algorithm_data
        # Widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        self.tab_widget = QTabWidget(self)
        self.__set_chart("F-G Plot", 0, 1, 'Generation', 'Fitness')
        self.__set_chart("G-T Plot", 2, 0, 'Time', 'Generation')
        self.__set_chart("F-T Plot", 2, 1, 'Time', 'Fitness')
        main_layout.addWidget(self.tab_widget)

    def __set_chart(self, name: str, x_i: int, y_i: int,
                    x_l: str, y_l: str) -> None:
        """Setting charts by data index.

        pos_x / pos_y: [0], [1], [2]
        time_fitness: List[List[Tuple[gen, fitness, time]]]
        """
        chart = DataChart(self)
        ax = chart.ax()
        for i, data in enumerate(self.algorithm_data):
            a = array(data['time_fitness'], dtype=float)
            ax[0].plot(a[:, x_i], a[:, y_i], 'bs-', label=f"Task {i + 1}")
            ax[0].set_xlabel(x_l)
            ax[0].set_ylabel(y_l)
            ax[0].legend()
        self.tab_widget.addTab(chart, name)
