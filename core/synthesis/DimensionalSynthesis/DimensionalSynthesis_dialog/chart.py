# -*- coding: utf-8 -*-

"""The chart dialog of dimensional synthesis result."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QDialog,
    Qt,
    QSize,
    QVBoxLayout,
    QTabWidget,
    QCategoryAxis,
    QValueAxis,
    QLineSeries,
    QScatterSeries,
    QColor,
    QPointF,
    QWidget,
    QIcon,
    QChartView,
    QSizePolicy,
)
from core.graphics import DataChart


class ChartDialog(QDialog):
    
    """There are three charts are in the dialog.
    
    + Fitness / Generation Chart.
    + Generation / Time Chart.
    + Fitness / Time Chart.
    """
    
    def __init__(self, title, mechanism_data, parent: QWidget):
        """Add three tabs of chart."""
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle("Chart")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        
        self.__title = title
        self.__mechanism_data = mechanism_data
        
        # Widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        self.tabWidget = QTabWidget(self)
        self.__setChart("Fitness / Generation Chart", 0, 1)
        self.__setChart("Generation / Time Chart", 2, 0)
        self.__setChart("Fitness / Time Chart", 2, 1)
        main_layout.addWidget(self.tabWidget)
    
    def __setChart(self, tabName: str, posX: int, posY: int):
        """Setting charts by data index.
        
        posX / posY: [0], [1], [2]
        time_fitness: List[List[Tuple[gen, fitness, time]]]
        """
        if self.__mechanism_data:
            if type(self.__mechanism_data[0]['time_fitness'][0]) == float:
                plot = [[
                    (data['last_gen']*i/len(data['time_fitness']), tnf, 0)
                    for i, tnf in enumerate(data['time_fitness'])
                ] for data in self.__mechanism_data]
            else:
                # Just copy from __mechanism_data
                plot = [[tnf for tnf in data['time_fitness']] for data in self.__mechanism_data]
        axisX = QCategoryAxis()
        axisY = QValueAxis()
        axisX.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axisX.setMin(0)
        axisY.setTickCount(11)
        # X maxima
        if self.__mechanism_data:
            maximaX = int(max([max([tnf[posX] for tnf in data]) for data in plot])*100)
            axisX.setMax(maximaX)
            i10 = int(maximaX / 10)
            if i10:
                for i in range(0, maximaX + 1, i10):
                    axisX.append(str(i/100), i)
            else:
                for i in range(0, 1000, 100):
                    axisX.append(str(i/100), i)
        # Y maxima
        if self.__mechanism_data:
            maximaY = max(max([tnf[posY] for tnf in data]) for data in plot) + 10
        else:
            maximaY = 100
        maximaY -= maximaY % 10
        axisY.setRange(0., maximaY)
        chart = DataChart(self.__title, axisX, axisY)
        # Append datasets
        for data in self.__mechanism_data:
            line = QLineSeries()
            scatter = QScatterSeries()
            gen = data['last_gen']
            tnf = plot[self.__mechanism_data.index(data)]
            points = tnf[:-1] if (tnf[-1] == tnf[-2]) else tnf
            line.setName(f"{data['Algorithm']}({gen} gen): {data['Expression']}")
            scatter.setMarkerSize(7)
            scatter.setColor(QColor(110, 190, 30))
            for i, e in enumerate(points):
                y = e[posY]
                x = e[posX]*100
                line.append(QPointF(x, y))
                scatter.append(QPointF(x, y))
            for series in (line, scatter):
                chart.addSeries(series)
                series.attachAxis(axisX)
                series.attachAxis(axisY)
            chart.legend().markers(scatter)[0].setVisible(False)
        # Add chart into tab widget
        widget = QWidget()
        self.tabWidget.addTab(widget, QIcon(), tabName)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        chartView = QChartView(chart)
        chartView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(chartView)
