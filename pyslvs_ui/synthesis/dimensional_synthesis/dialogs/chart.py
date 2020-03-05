# -*- coding: utf-8 -*-

"""The chart dialog of dimensional synthesis result."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2020"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from typing import List, Sequence, Dict, Any
from qtpy.QtCore import Qt, QSize, QPointF
from qtpy.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTabWidget,
    QWidget,
    QSizePolicy,
)
from qtpy.QtGui import QColor, QIcon
from qtpy.QtCharts import QtCharts
from pyslvs_ui.graphics import DataChart

_Plot = List[List[List[float]]]


class ChartDialog(QDialog):
    """There are three charts are in the dialog.

    + Fitness / Generation Chart.
    + Generation / Time Chart.
    + Fitness / Time Chart.
    """

    def __init__(
        self,
        title: str,
        algorithm_data: Sequence[Dict[str, Any]],
        monochrome: bool,
        parent: QWidget
    ) -> None:
        """Add three tabs of chart."""
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle("Chart")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        self.title = title
        self.algorithm_data = algorithm_data
        self.monochrome = monochrome
        # Widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        self.tabWidget = QTabWidget(self)
        self.__set_chart("Fitness / Generation Chart", 0, 1)
        self.__set_chart("Generation / Time Chart", 2, 0)
        self.__set_chart("Fitness / Time Chart", 2, 1)
        main_layout.addWidget(self.tabWidget)

    def __set_chart(self, tab_name: str, pos_x: int, pos_y: int) -> None:
        """Setting charts by data index.

        pos_x / pos_y: [0], [1], [2]
        time_fitness: List[List[Tuple[gen, fitness, time]]]
        """
        axis_x = QtCharts.QCategoryAxis()
        axis_y = QtCharts.QValueAxis()
        axis_x.setLabelsPosition(QtCharts.QCategoryAxis.AxisLabelsPositionOnValue)
        axis_x.setMin(0)
        axis_y.setTickCount(11)
        if self.algorithm_data:
            # Just copy references from algorithm data
            plot: _Plot = [data['time_fitness'] for data in self.algorithm_data]
            # X max
            max_x = int(max(max(tnf[pos_x] for tnf in data) for data in plot)) * 100
            axis_x.setMax(max_x)
            i10 = int(max_x / 10)
            if i10:
                for i in range(0, max_x + 1, i10):
                    axis_x.append(str(i / 100), i)
            else:
                for i in range(0, 1000, 100):
                    axis_x.append(str(i / 100), i)
            # Y max
            max_y = max(max([tnf[pos_y] for tnf in data]) for data in plot) + 10
        else:
            plot = []
            # Y max
            max_y = 100
        max_y -= max_y % 10
        axis_y.setRange(0., max_y)
        chart = DataChart(self.title, axis_x, axis_y, self.monochrome)
        # Append data set
        for i, data in enumerate(self.algorithm_data):
            line = QtCharts.QLineSeries()
            scatter = QtCharts.QScatterSeries()
            line.setName(f"{i}: {data['algorithm']}")
            scatter.setMarkerSize(7)
            scatter.setColor(QColor(110, 190, 30))
            if plot:
                for e in plot[self.algorithm_data.index(data)]:
                    y = e[pos_y]
                    x = e[pos_x] * 100
                    line.append(QPointF(x, y))
                    scatter.append(QPointF(x, y))
            for series in (line, scatter):
                chart.addSeries(series)
                series.attachAxis(axis_x)
                series.attachAxis(axis_y)
            chart.legend().markers(scatter)[0].setVisible(False)
        # Add chart into tab widget
        widget = QWidget()
        self.tabWidget.addTab(widget, QIcon(), tab_name)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        chart_view = QtCharts.QChartView(chart)
        chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(chart_view)
