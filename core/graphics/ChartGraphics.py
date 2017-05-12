# -*- coding: utf-8 -*-
from ..QtModules import *
from PyQt5.QtChart import *

class ChartDialog(QDialog):
    def __init__(self, Title, DataSet=list(), parent=None):
        super(ChartDialog, self).__init__(parent)
        self.setWindowTitle('Chart')
        self.setModal(True)
        self.setMinimumSize(QSize(800, 600))
        chart = QChart()
        chart.setTitle(Title)
        chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        chart.legend().setAlignment(Qt.AlignRight)
        axisX = QCategoryAxis()
        axisY = QValueAxis()
        axisX.setLabelsPosition(QCategoryAxis.AxisLabelsPositionOnValue)
        axisY.setTickCount(10)
        if len(DataSet)>0:
            maxGen = max([data[1] for data in DataSet])
            chart.setTitle("{} (max {} generations)".format(Title, maxGen))
            maxLen = max([len(data[2]) for data in DataSet])
            report = int(round(maxGen/maxLen-2, 0))
            for i in range(0, maxGen+1, int(maxGen/10)): axisX.append(str(i), i)
        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)
        for data in DataSet:
            line = QLineSeries()
            scatter = QScatterSeries()
            line.setName("{} ({} gen)".format(data[0], data[1]))
            scatter.setMarkerSize(7)
            scatter.setColor(QColor(110, 190, 30))
            for i, e in enumerate(data[2][:-1]):
                x = round(i*data[1]/(len(data[2])-2), 0)
                line.append(QPointF(x, e))
                scatter.append(QPointF(x, e))
            for series in [line, scatter]:
                chart.addSeries(series)
                series.attachAxis(axisX)
                series.attachAxis(axisY)
            chart.legend().markers(scatter)[0].setVisible(False)
        axisY.setRange(0., max([max(e[2]) for e in DataSet]) if DataSet else 100.)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*([2]*4))
        chartView = QChartView(chart)
        chartView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(chartView)
