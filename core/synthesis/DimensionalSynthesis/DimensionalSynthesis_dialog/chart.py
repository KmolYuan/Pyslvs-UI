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
    
    def __init__(self, Title, mechanism_data=[], parent=None):
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle("Chart")
        self.setWindowFlags(self.windowFlags() | Qt.WindowMaximizeButtonHint)
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        self.Title = Title
        self.mechanism_data = mechanism_data
        #Widgets
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(6, 6, 6, 6)
        self.tabWidget = QTabWidget(self)
        self.setChart("Fitness / Generation Chart", 0, 1)
        self.setChart("Generation / Time Chart", 2, 0)
        self.setChart("Fitness / Time Chart", 2, 1)
        main_layout.addWidget(self.tabWidget)
    
    def setChart(self, tabName: str, posX: int, posY: int):
        '''Setting charts by data index.
        
        posX / posY: [0] / [1] / [2]
        TimeAndFitness: List[List[Tuple[gen, fitness, time]]]
        '''
        if self.mechanism_data:
            if type(self.mechanism_data[0]['TimeAndFitness'][0])==float:
                TimeAndFitness = [
                    [(data['lastGen']*i/len(data['TimeAndFitness']), Tnf, 0)
                    for i, Tnf in enumerate(data['TimeAndFitness'])]
                    for data in self.mechanism_data]
            else:
                #Just copy from mechanism_data
                TimeAndFitness = [[Tnf for Tnf in data['TimeAndFitness']] for data in self.mechanism_data]
        axisX = QCategoryAxis()
        axisY = QValueAxis()
        axisX.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axisX.setMin(0)
        axisY.setTickCount(11)
        #X maxima
        if self.mechanism_data:
            maximaX = int(max([max([Tnf[posX] for Tnf in data]) for data in TimeAndFitness])*100)
            axisX.setMax(maximaX)
            i10 = int(maximaX/10)
            if i10:
                for i in range(0, maximaX+1, i10):
                    axisX.append(str(i/100), i)
            else:
                for i in range(0, 1000, 100):
                    axisX.append(str(i/100), i)
        #Y maxima
        if self.mechanism_data:
            maximaY = max([max([Tnf[posY] for Tnf in data]) for data in TimeAndFitness])+10
        else:
            maximaY = 100
        maximaY -= maximaY%10
        axisY.setRange(0., maximaY)
        chart = DataChart(self.Title, axisX, axisY)
        #Append datasets
        for data in self.mechanism_data:
            line = QLineSeries()
            scatter = QScatterSeries()
            gen = data['lastGen']
            Tnf = TimeAndFitness[self.mechanism_data.index(data)]
            points = Tnf[:-1] if Tnf[-1]==Tnf[-2] else Tnf
            line.setName("{}({} gen): {}".format(data['Algorithm'], gen, data['Expression']))
            scatter.setMarkerSize(7)
            scatter.setColor(QColor(110, 190, 30))
            for i, e in enumerate(points):
                y = e[posY]
                x = e[posX]*100
                line.append(QPointF(x, y))
                scatter.append(QPointF(x, y))
            for series in [line, scatter]:
                chart.addSeries(series)
                series.attachAxis(axisX)
                series.attachAxis(axisY)
            chart.legend().markers(scatter)[0].setVisible(False)
        #Add chart into tab widget
        widget = QWidget()
        self.tabWidget.addTab(widget, QIcon(), tabName)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        chartView = QChartView(chart)
        chartView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(chartView)
