# -*- coding: utf-8 -*-
from .__init__ import *
from ..calculation.pathTrack import WorkerThread

class Path_Track_show(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Path_Track_show, self).__init__(parent)
        self.setupUi(self)
        self.work = WorkerThread()
        self.Path_data = []
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.start)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.stop)
        self.work.done.connect(self.finish)
        self.work.progress_Signal.connect(self.progressbar_change)
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(False)
    
    @pyqtSlot()
    def on_add_button_clicked(self):
        try:
            self.Run_list.addItem(self.Point_list.currentItem().text())
            self.Point_list.takeItem(self.Point_list.currentRow())
        except: pass
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(self.Run_list.count()>=1)
    
    @pyqtSlot()
    def on_remove_botton_clicked(self):
        try:
            self.Point_list.addItem(self.Run_list.currentItem().text())
            self.Run_list.takeItem(self.Run_list.currentRow())
        except: pass
        self.buttonBox.button(QDialogButtonBox.Apply).setEnabled(self.Run_list.count()>=1)
    
    def loadData(self, Point, Link, Chain, Shaft, Slider, Rod, Parameter):
        self.work.Point = Point
        self.work.Link = Link
        self.work.Chain = Chain
        self.work.Shaft = Shaft
        self.work.Slider = Slider
        self.work.Rod = Rod
        self.work.Parameter = Parameter
        for i in range(len(Shaft)):
            shaftCheckBox = QCheckBox(self.scrollAreaWidgetContents)
            shaftCheckBox.setText("Shaft"+str(i))
            self.verticalLayout_6.insertWidget(0, shaftCheckBox)
    
    def start(self):
        self.work.Run_list = self.Run_list
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
            self.Run_list.setEnabled(False)
            self.Point_list.setEnabled(False)
            self.Resolution.setEnabled(False)
            self.add_button.setEnabled(False)
            self.remove_botton.setEnabled(False)
            self.allShafts.setEnabled(False)
            self.chooseShafts.setEnabled(False)
            self.shaftsScrollArea.setEnabled(False)
    def stop(self): self.work.stop()
    
    @pyqtSlot(int)
    def progressbar_change(self, val): self.progressBar.setValue(val)
    
    @pyqtSlot(list)
    def finish(self, Path):
        self.Path_data = Path
        self.accept()
    
    @pyqtSlot(bool)
    def on_chooseShafts_toggled(self, checked):
        self.shaftsScrollArea.setEnabled(checked)
