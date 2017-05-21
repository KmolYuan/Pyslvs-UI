# -*- coding: utf-8 -*-
from ..QtModules import *
from ..graphics.color import colorIcons
from ..calculation.pathTrack import WorkerThread
from .Ui_run_Path_Track import Ui_Dialog as PathTrack_Dialog

class Path_Track_show(QDialog, PathTrack_Dialog):
    def __init__(self, Point, Link, Chain, Shaft, Slider, Rod, warning, parent=None):
        super(Path_Track_show, self).__init__(parent)
        self.setupUi(self)
        self.rejected.connect(self.closeWork)
        self.work = WorkerThread(Point, Link, Chain, Shaft, Slider, Rod, warning, None)
        self.work.done.connect(self.finish)
        self.work.progress_Signal.connect(self.progressbar_change)
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.start)
        self.allShafts.clicked.connect(self.isReady)
        self.chooseShafts.clicked.connect(self.isReady)
        for i, e in enumerate(Point):
            if not e.fix: self.Run_list.addItem(QListWidgetItem(colorIcons()[e.color], 'Point{}'.format(i)))
        self.shaftList = list()
        for i in range(len(Shaft)):
            shaftCheckBox = QCheckBox(self.scrollAreaWidgetContents)
            shaftCheckBox.setText('Shaft{}'.format(i))
            if i==0: shaftCheckBox.setChecked(True)
            shaftCheckBox.clicked.connect(self.isReady)
            self.shaftList.append(shaftCheckBox)
        for checkBox in reversed(self.shaftList): self.scrollAreaWidgetLayout.insertWidget(0, checkBox)
        self.isReady()
    
    @pyqtSlot()
    def isReady(self):
        self.shaftReadyList = [e.isChecked() for e in self.shaftList]
        n = False
        for e in self.shaftReadyList: n |= e
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(n or self.allShafts.isChecked())
    
    @pyqtSlot(bool)
    def on_chooseShafts_toggled(self, checked): self.shaftsScrollArea.setEnabled(checked)
    
    def start(self):
        self.work.set(
            [i for i in range(len(self.shaftReadyList))] if self.allShafts.isChecked() else
            [i for i in range(len(self.shaftReadyList)) if self.shaftReadyList[i]==True],
            [int(self.Run_list.item(i).text().replace('Point', '')) for i in range(self.Run_list.count())],
            self.Resolution.value())
        self.progressBar.setRange(0, sum([(e.end-e.start)/self.Resolution.value() for e in self.work.Shaft]))
        self.work.start()
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
        self.mainPanel.setEnabled(False)
        self.subPanel.setEnabled(False)
    
    @pyqtSlot(int)
    def progressbar_change(self, val): self.progressBar.setValue(val)
    
    @pyqtSlot(list)
    def finish(self, Path):
        self.ShaftSuggest = list()
        for vpaths in Path:
            route = vpaths.paths[0].path
            resolution = self.Resolution.value()
            fallIndex = sorted([i*resolution for i, dot in enumerate(route) if dot[0]==False])
            if (not fallIndex) or len(fallIndex)==len(route): continue
            self.ShaftSuggest.append(list(reversed([fallIndex[0]%360, fallIndex[-1]%360])))
        self.Path_data = Path
        self.accept()
    
    @pyqtSlot()
    def closeWork(self):
        if self.work.isRunning():
            self.work.stop()
            self.work.exit()
            self.work.wait()
            print("The thread has been canceled.")
