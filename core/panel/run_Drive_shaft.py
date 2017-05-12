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
        for i in range(self.startAngle if self.startAngle>self.minima else self.minima, self.maxima, 300):
            if self.stoped: return
            else:
                sleep(.05)
                self.progress_Signal.emit(i)
        for t in range(9):
            for i in range(self.minima, self.maxima, 300):
                if self.stoped: return
                else:
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
            else:
                sleep(.05)
                self.progress_Signal.emit(i)
        self.done.emit(self.endAngle)
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True

class Drive_shaft_show(QWidget, Drive_Form):
    degreeChange = pyqtSignal(float)
    def __init__(self, table, currentShaft, parent=None):
        super(Drive_shaft_show, self).__init__(parent)
        self.setupUi(self)
        self.table = table
        for i in range(len(table)): self.Shaft.insertItem(i, QIcon(QPixmap(":/icons/circle.png")), 'Shaft{}'.format(i))
        self.Shaft.setCurrentIndex(currentShaft)
        self.startAngle = int(table[currentShaft].start*100)
        self.endAngle = int(table[currentShaft].end*100)
        self.demoAngle = int(table[currentShaft].demo*100)
        self.playButton.clicked.connect(self.playStart)
        self.Degree.setMinimum(self.startAngle)
        self.Degree.setMaximum(self.endAngle)
        self.Degree.setValue(self.demoAngle)
    
    @pyqtSlot(int)
    def on_Shaft_currentIndexChanged(self, index):
        self.startAngle = int(self.table[index].start*100)
        self.endAngle = int(self.table[index].end*100)
        self.demoAngle = int(self.table[index].demo*100)
        self.Degree.setValue(self.demoAngle)
    
    @pyqtSlot(int)
    def on_Degree_valueChanged(self, val): self.Degree_text.setValue(float(val/100))
    @pyqtSlot(float)
    def on_Degree_text_valueChanged(self, val): self.Degree.setValue(int(val*100))
    
    @pyqtSlot()
    def on_a0_clicked(self): self.playAngle(360.)
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
    def setAngle(self, angle):
        self.Degree_text.setValue(angle)
        self.degreeChange.emit(float(angle))
    def playAngle(self, angle):
        self.playShaft = playAngle(self.Degree_text.value(), angle)
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
