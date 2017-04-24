# -*- coding: utf-8 -*-
from ..QtModules import *
from .Ui_run_Drive_shaft import Ui_Form as Drive_Form
from time import sleep

class playShaft(QThread):
    done = pyqtSignal()
    progress_Signal = pyqtSignal(int)
    def __init__(self, minima, maxima, parent=None):
        super(playShaft, self).__init__(parent)
        self.stoped = False
        self.mutex = QMutex()
        self.minima = minima
        self.maxima = maxima
    
    def run(self):
        with QMutexLocker(self.mutex): self.stoped = False
        for t in range(10):
            for i in range(self.minima, self.maxima, 300):
                if self.stoped: return
                else:
                    sleep(.05)
                    self.progress_Signal.emit(i)
        self.done.emit()
    
    def stop(self):
        with QMutexLocker(self.mutex): self.stoped = True

class Drive_shaft_show(QWidget, Drive_Form):
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
    def playStart(self):
        self.playShaft = playShaft(self.startAngle, self.endAngle)
        self.playShaft.done.connect(self.finish)
        self.playShaft.progress_Signal.connect(self.playGoing)
        self.playButton.clicked.disconnect(self.playStart)
        self.playButton.clicked.connect(self.playStop)
        self.Degree_text.setEnabled(False)
        self.Degree.setEnabled(False)
        self.playButton.setText('Stop')
        self.playShaft.start()
    
    @pyqtSlot(int)
    def playGoing(self, val): self.Degree.setValue(val)
    
    @pyqtSlot()
    def finish(self):
        self.playButton.clicked.disconnect(self.playStop)
        self.playButton.clicked.connect(self.playStart)
        self.playButton.setText('Play')
        self.Degree_text.setEnabled(True)
        self.Degree.setEnabled(True)
        self.Degree.setValue(self.demoAngle)
    
    @pyqtSlot()
    def playStop(self):
        self.playShaft.stop()
        self.playButton.clicked.disconnect(self.playStop)
        self.playButton.clicked.connect(self.playStart)
        self.playButton.setText('Play')
        self.Degree_text.setEnabled(True)
        self.Degree.setEnabled(True)
