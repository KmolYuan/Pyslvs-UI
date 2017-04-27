# -*- coding: utf-8 -*-
from ..QtModules import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class BasicChart(FigureCanvas):
    def __init__(self, data, parent=None, width=5, height=4, dpi=100):
        self.data = data
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.initial_figure()
        FigureCanvas.updateGeometry(self)
    
    def initial_figure(self):
        x = [i for i in range(len(self.data))]
        y = self.data
        self.axes.plot(x, y, 'r')

class BasicChartDialog(QDialog):
    def __init__(self, Title, data=[0], parent=None):
        super(BasicChartDialog, self).__init__(parent)
        self.CentralWidget = QWidget(self)
        layout = QVBoxLayout(self.CentralWidget)
        chart = BasicChart(data=data, parent=self.CentralWidget)
        layout.addWidget(chart)
        self.setWindowTitle(Title)
        self.setModal(True)
        self.setMinimumSize(chart.size())
        self.setMaximumSize(chart.size())
