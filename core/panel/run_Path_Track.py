# -*- coding: utf-8 -*-
from .modules import *
from ..calculation.pathTrack import WorkerThread
from .Ui_run_Path_Track import Ui_Dialog as PathTrack_Dialog

class Path_Track_show(QDialog, PathTrack_Dialog):
    def __init__(self, Point, Link, Chain, Shaft, Slider, Rod, Parameter, parent=None):
        super(Path_Track_show, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkerThread()
        self.Path_data = list()
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.start)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.stop)
        self.work.done.connect(self.finish)
        self.work.progress_Signal.connect(self.progressbar_change)
        self.allShafts.clicked.connect(self.isReady)
        self.chooseShafts.clicked.connect(self.isReady)
        self.work.Point = Point
        self.work.Link = Link
        self.work.Chain = Chain
        self.work.Shaft = Shaft
        self.work.Slider = Slider
        self.work.Rod = Rod
        self.work.Parameter = Parameter
        for i in range(len(Point)):
            if not Point[i]['fix']: self.Point_list.addItem('Point{}'.format(i))
        self.shaftList = list()
        for i in range(len(Shaft)):
            shaftCheckBox = QCheckBox(self.scrollAreaWidgetContents)
            shaftCheckBox.setText("Shaft"+str(i))
            if i==0: shaftCheckBox.setChecked(True)
            shaftCheckBox.clicked.connect(self.isReady)
            self.shaftList.append(shaftCheckBox)
        for checkBox in self.shaftList: self.scrollAreaWidgetLayout.insertWidget(0, checkBox)
        self.isReady()
    
    @pyqtSlot()
    def on_add_button_clicked(self):
        try:
            self.Run_list.addItem(self.Point_list.currentItem().text())
            self.Point_list.takeItem(self.Point_list.currentRow())
        except: pass
        self.isReady()
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        try:
            self.Point_list.addItem(self.Run_list.currentItem().text())
            self.Run_list.takeItem(self.Run_list.currentRow())
        except: pass
        self.isReady()
    @pyqtSlot()
    def isReady(self):
        self.shaftReadyList = [e.isChecked() for e in self.shaftList]
        n = False
        for e in self.shaftReadyList: n |= e
        n |= self.allShafts.isChecked()
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(n and self.Run_list.count()>=1)
    
    @pyqtSlot(bool)
    def on_chooseShafts_toggled(self, checked): self.shaftsScrollArea.setEnabled(checked)
    
    def start(self):
        if self.allShafts.isChecked(): self.work.ShaftList = [e for e in range(len(self.shaftReadyList))]
        else: self.work.ShaftList = [e for e in range(len(self.shaftReadyList)) if self.shaftReadyList[e]==True]
        self.work.Run_list = [int(self.Run_list.item(e).text().replace("Point", "")) for e in range(self.Run_list.count())]
        self.work.Resolution = float(self.Resolution.text())
        if not self.Run_list.count()==0:
            q = 0
            for i in range(len(self.work.Shaft)):
                start_angle = self.work.Shaft[i]['start']*100
                end_angle = self.work.Shaft[i]['end']*100
                Resolution = float(self.Resolution.text())*100
                angle_set = int((end_angle+1-start_angle)/Resolution)
                q = q+angle_set
            limit = self.Run_list.count()*q
            self.progressBar.setRange(0, limit)
            self.work.start()
            self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
            self.mainPanel.setEnabled(False)
            self.subPanel.setEnabled(False)
    def stop(self): self.work.stop()
    
    @pyqtSlot(int)
    def progressbar_change(self, val): self.progressBar.setValue(val)
    
    @pyqtSlot(list)
    def finish(self, Path):
        self.Path_data = Path
        self.accept()
