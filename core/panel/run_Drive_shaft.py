# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Drive_shaft import Ui_Form as Drive_Form
from time import sleep

class playShaft(QThread):
    done = pyqtSignal()
    progress_Signal = pyqtSignal(int)
    def __init__(self, startAngle, minima, maxima, parent=None):
        super(playShaft, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.startAngle = startAngle
        self.minima = minima
        self.maxima = maxima
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        angleSE = sorted([self.minima, self.maxima])
        for i in range(self.startAngle if self.startAngle>angleSE[0] else angleSE[0], angleSE[1], 300):
            if self.stoped: return
            sleep(.05)
            self.progress_Signal.emit(i)
        while True:
            if angleSE[0]!=0 and angleSE[1]!=36000:
                for i in range(angleSE[0], angleSE[1], 300):
                    if self.stoped: return
                    sleep(.05)
                    self.progress_Signal.emit(angleSE[1]-i)
            for i in range(angleSE[0], angleSE[1], 300):
                if self.stoped: return
                sleep(.05)
                self.progress_Signal.emit(i)
        self.done.emit()
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True

class playAngle(QThread):
    done = pyqtSignal(float)
    progress_Signal = pyqtSignal(int)
    def __init__(self, startAngle, endAngle, parent=None):
        super(playAngle, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.startAngle = startAngle
        self.endAngle = endAngle
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        start = int(self.startAngle*100)
        end = int((self.endAngle if self.endAngle>self.startAngle else self.endAngle+360)*100)
        for i in range(start, end+300, 300):
            if self.stoped: return
            sleep(.05)
            self.progress_Signal.emit(i)
        self.done.emit(self.endAngle)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True

class RotatableView(QGraphicsView):
    def __init__(self, item):
        QGraphicsView.__init__(self)
        scene = QGraphicsScene(self)
        self.setScene(scene)
        item.setMinimumSize(QSize(150, 150))
        item.setMaximum(36000)
        item.setSingleStep(100)
        item.setPageStep(100)
        item.setInvertedAppearance(True)
        item.setWrapping(True)
        item.setNotchTarget(.1)
        item.setNotchesVisible(True)
        graphics_item = scene.addWidget(item)
        graphics_item.setRotation(-90)
        # make the QGraphicsView invisible
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedHeight(item.height())
        self.setFixedWidth(item.width())
        self.setStyleSheet("border: 0px;")

class Drive_shaft_show(QWidget, Drive_Form):
    degreeChange = pyqtSignal(float, int)
    def __init__(self, Shaft, currentShaft, isPathDemoMode, parent=None):
        super(Drive_shaft_show, self).__init__(parent)
        self.setupUi(self)
        self.pathDemoMode.setVisible(isPathDemoMode)
        self.Degree = QDial()
        self.Degree.valueChanged.connect(self.on_Degree_valueChanged)
        self.Degree.sliderReleased.connect(self.on_Degree_sliderReleased)
        self.anglePanel.insertWidget(1, RotatableView(self.Degree))
        self.tableShaft = Shaft
        for i in range(len(self.tableShaft)): self.Shaft.insertItem(i, QIcon(QPixmap(":/icons/circle.png")), 'Shaft{}'.format(i))
        self.Shaft.setCurrentIndex(currentShaft)
        self.startAngle = int(self.tableShaft[currentShaft].start*100)
        self.endAngle = int(self.tableShaft[currentShaft].end*100)
        self.demoAngle = int(self.tableShaft[currentShaft].demo*100)
        self.playButton.clicked.connect(self.playStart)
        self.Degree.setMinimum(self.startAngle)
        self.Degree.setMaximum(self.endAngle)
        self.Degree.setValue(self.demoAngle)
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index):
        self.startAngle = int(self.tableShaft[index].start*100)
        self.endAngle = int(self.tableShaft[index].end*100)
        self.demoAngle = int(self.tableShaft[index].demo*100)
        self.Degree.setValue(self.demoAngle)
    
    @pyqtSlot(int)
    def on_Degree_valueChanged(self, val): self.Degree_text.setValue(float(val/100))
    @pyqtSlot(float)
    def on_Degree_text_valueChanged(self, val): self.Degree.setValue(int(val*100))
    
    @pyqtSlot()
    def on_a0_clicked(self): self.playAngle(0.)
    @pyqtSlot()
    def on_a90_clicked(self): self.playAngle(90.)
    @pyqtSlot()
    def on_a180_clicked(self): self.playAngle(180.)
    @pyqtSlot()
    def on_a270_clicked(self): self.playAngle(270.)
    @pyqtSlot()
    def on_a45_clicked(self): self.playAngle(45.)
    @pyqtSlot()
    def on_a135_clicked(self): self.playAngle(135.)
    @pyqtSlot()
    def on_a225_clicked(self): self.playAngle(225.)
    @pyqtSlot()
    def on_a315_clicked(self): self.playAngle(315.)
    @pyqtSlot()
    def on_Degree_sliderReleased(self): self.setAngle(self.Degree_text.value())
    def setAngle(self, angle): self.Degree_text.setValue(angle)
    def playAngle(self, angle):
        self.playShaft = playAngle(self.Degree_text.value(), angle, None)
        self.playShaft.done.connect(self.goal)
        self.startPlay(self.playShaft)
    
    @pyqtSlot()
    def playStart(self):
        self.playShaft = playShaft(int(self.Degree_text.value()*100), self.startAngle, self.endAngle)
        self.playShaft.done.connect(self.finish)
        self.startPlay(self.playShaft)
    
    @pyqtSlot(int)
    def playGoing(self, val): self.Degree.setValue(val)
    
    def startPlay(self, work):
        work.progress_Signal.connect(self.playGoing)
        self.playButton.clicked.disconnect(self.playStart)
        self.playButton.clicked.connect(self.playStop)
        for widget in [self.a0, self.a90, self.a180, self.a270, self.a45, self.a135, self.a225, self.a315,
            self.Degree_text, self.Degree]: widget.setEnabled(False)
        self.playButton.setText('Stop')
        work.start()
    @pyqtSlot()
    def finish(self): self.stopPlay()
    @pyqtSlot(float)
    def goal(self, angle):
        self.stopPlay()
        self.setAngle(angle)
    @pyqtSlot()
    def playStop(self):
        self.playShaft.stop()
        self.stopPlay()
    def stopPlay(self):
        self.playButton.clicked.disconnect(self.playStop)
        self.playButton.clicked.connect(self.playStart)
        self.playButton.setText('Play')
        for widget in [self.a0, self.a90, self.a180, self.a270, self.a45, self.a135, self.a225, self.a315,
            self.Degree_text, self.Degree]: widget.setEnabled(True)
        self.setAngle(self.Degree_text.value())
    
    def __del__(self): self.degreeChange.emit(self.Degree_text.value(), self.Shaft.currentIndex())
