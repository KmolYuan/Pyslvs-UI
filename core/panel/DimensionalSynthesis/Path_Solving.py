# -*- coding: utf-8 -*-
from ...QtModules import *
from .Ui_Path_Solving import Ui_Form as PathSolving_Form
from ...graphics.ChartGraphics import ChartDialog
from .Path_Solving_options import Path_Solving_options_show
from .Path_Solving_progress import Path_Solving_progress_show
from .Path_Solving_series import Path_Solving_series_show

class Path_Solving_show(QWidget, PathSolving_Form):
    addPathPoint = pyqtSignal(float, float)
    deletePathPoint = pyqtSignal(int)
    moveupPathPoint = pyqtSignal(int)
    movedownPathPoint = pyqtSignal(int)
    mergeResult = pyqtSignal(int)
    def __init__(self, FileState, data, resultData, width, parent=None):
        super(Path_Solving_show, self).__init__(parent)
        self.setupUi(self)
        self.FileState = FileState
        self.mechanism_data = resultData
        self.path = data
        for e in data: self.Point_list.addItem("({}, {})".format(e['x'], e['y']))
        for e in resultData: self.addResult(e)
        self.Settings = {
            'maxGen':1500, 'report':1, 'AxMin':-50., 'AyMin':-50., 'DxMin':-50., 'DyMin':-50., 'IMin':5., 'LMin':5., 'FMin':5., 'AMin':0.,
            'AxMax':50., 'AyMax':50., 'DxMax':50., 'DyMax':50., 'IMax':50., 'LMax':50., 'FMax':50., 'AMax':360.}
        self.isGenerate()
        self.isGetResult()
    
    @pyqtSlot()
    def on_clearAll_clicked(self):
        self.Point_list.setCurrentRow(0)
        for i in reversed(range(self.Point_list.count()+1)): self.on_remove_clicked()
        self.isGenerate()
    
    @pyqtSlot()
    def on_series_clicked(self):
        dlg = Path_Solving_series_show(self)
        dlg.show()
        if dlg.exec_():
            for e in dlg.path: self.on_add_clicked(e[0], e[1])
    
    @pyqtSlot()
    def on_moveUp_clicked(self):
        n = self.Point_list.currentRow()
        if n>0 and self.Point_list.count()>1:
            self.moveupPathPoint.emit(n)
            x = self.Point_list.currentItem().text()[1:-1].split(', ')[0]
            y = self.Point_list.currentItem().text()[1:-1].split(', ')[1]
            self.Point_list.insertItem(n-1, '('+str(x)+", "+str(y)+')')
            self.Point_list.takeItem(n+1)
            self.Point_list.setCurrentRow(n-1)
    
    @pyqtSlot()
    def on_moveDown_clicked(self):
        n = self.Point_list.currentRow()
        if n<self.Point_list.count()-1 and self.Point_list.count()>1:
            self.movedownPathPoint.emit(n)
            x = self.Point_list.currentItem().text()[1:-1].split(', ')[0]
            y = self.Point_list.currentItem().text()[1:-1].split(', ')[1]
            self.Point_list.insertItem(n+2, '('+str(x)+", "+str(y)+')')
            self.Point_list.takeItem(n)
            self.Point_list.setCurrentRow(n+1)
    
    def addPath(self, x, y):
        self.Point_list.addItem('({}, {})'.format(x, y))
        self.isGenerate()
    
    @pyqtSlot()
    def on_add_clicked(self, x=False, y=False):
        if x is False:
            x = self.X_coordinate.value()
            y = self.Y_coordinate.value()
        self.addPathPoint.emit(x, y)
        self.Point_list.addItem("({}, {})".format(x, y))
        self.isGenerate()
    @pyqtSlot()
    def on_remove_clicked(self):
        if self.Point_list.currentRow()>-1:
            self.deletePathPoint.emit(self.Point_list.currentRow())
            self.Point_list.takeItem(self.Point_list.currentRow())
            self.isGenerate()
    
    def isGenerate(self):
        self.pointNum.setText(
            "<html><head/><body><p><span style=\" font-size:12pt; color:#00aa00;\">"+str(self.Point_list.count())+"</span></p></body></html>")
        n = self.Point_list.count()>1
        self.Generate.setEnabled(n)
    
    @pyqtSlot()
    def on_Generate_clicked(self):
        type_num = 0 if self.type0.isChecked() else 1 if self.type1.isChecked() else 2
        upper = ([self.Settings['AxMax'], self.Settings['AyMax'], self.Settings['DxMax'], self.Settings['DyMax'],
            self.Settings['IMax'], self.Settings['LMax'], self.Settings['FMax']]+[self.Settings['LMax']]*2)
        lower = ([self.Settings['AxMin'], self.Settings['AyMin'], self.Settings['DxMin'], self.Settings['DyMin'],
            self.Settings['IMin'], self.Settings['LMin'], self.Settings['FMin']]+[self.Settings['LMin']]*2)
        p = len(self.path)
        upperVal = upper+[self.Settings['AMax']]*p
        lowerVal = lower+[self.Settings['AMin']]*p
        Parm_num = p+9
        mechanismParams = {
            'Driving':'A',
            'Follower':'D',
            'Link':'L0,L1,L2,L3,L4',
            'Target':'E',
            'ExpressionName':'PLAP,PLLP,PLLP',
            'Expression':'A,L0,a0,D,B,B,L1,L2,D,C,B,L3,L4,C,E',
            'targetPath':tuple((e['x'], e['y']) for e in self.path),
            'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'}],
            'VARS':9,
            'formula':['PLAP','PLLP']}
        GenerateData = {
            'nParm':Parm_num,
            'upper':upperVal,
            'lower':lowerVal,
            'maxGen':self.Settings['maxGen'],
            'report':self.Settings['maxGen']*self.Settings['report']/100}
        dlg = Path_Solving_progress_show(type_num, mechanismParams, GenerateData, self)
        dlg.show()
        if dlg.exec_():
            self.mechanism_data.append(dlg.mechanism)
            self.addResult(dlg.mechanism)
            sec = dlg.time_spand%60
            mins = int(dlg.time_spand/60)
            self.timeShow.setText("<html><head/><body><p><span style=\" font-size:10pt\">{} [min] {} [s]</span></p></body></html>".format(mins, sec))
            print('Finished.')
    
    def addResult(self, e):
        keys = sorted(list(e.keys()))
        item = QListWidgetItem("{} ({} gen)".format(e['Algorithm'], e['GenerateData']['maxGen']))
        item.setToolTip('\n'.join(['[{}]'.format(e['Algorithm'])]+[
            "{}: {}".format(k, e[k]) for k in keys if not k in ['Algorithm', 'TimeAndFitness', 'mechanismParams', 'GenerateData']]))
        self.Result_list.addItem(item)
    
    @pyqtSlot(int)
    def on_Result_list_currentRowChanged(self, cr): self.isGetResult()
    
    @pyqtSlot()
    def on_deleteButton_clicked(self):
        row = self.Result_list.currentRow()
        del self.mechanism_data[row]
        self.Result_list.takeItem(row)
        self.isGetResult()
    
    def isGetResult(self):
        n = (self.Result_list.count()>0 and self.Result_list.currentRow()>-1)
        self.mergeButton.setEnabled(n)
        self.deleteButton.setEnabled(n)
    
    @pyqtSlot(QModelIndex)
    def on_Result_list_doubleClicked(self, index):
        if self.Result_list.currentRow()!=-1: self.on_mergeButton_clicked()
    
    @pyqtSlot()
    def on_mergeButton_clicked(self):
        reply = QMessageBox.question(self, 'Prompt Message', "Merge this result to your canvas?",
            (QMessageBox.Apply | QMessageBox.Cancel), QMessageBox.Apply)
        if reply==QMessageBox.Apply: self.mergeResult.emit(self.Result_list.currentRow())
    
    @pyqtSlot()
    def on_getTimeAndFitness_clicked(self):
        results = [[e['Algorithm'], e['GenerateData']['maxGen'], e['TimeAndFitness']] for e in self.mechanism_data]
        dlg = ChartDialog("Convergence Value", results, self)
        dlg.show()
    
    def CopySettings(self):
        if self.Result_list.currentRow()!=-1:
            args = self.mechanism_data[self.Result_list.currentRow()]
            if args['Algorithm']=='Genetic': self.type0.setChecked(True)
            elif args['Algorithm']=='Firefly': self.type1.setChecked(True)
            elif args['Algorithm']=="Differtial Evolution": self.type2.setChecked(True)
            self.Settings = args
            self.on_clearAll_clicked()
            for e in args['path']: self.on_add_clicked(e[0], e[1])
    
    @pyqtSlot()
    def on_advanceButton_clicked(self):
        dlg = Path_Solving_options_show(
            "Genetic Algorithm" if self.type0.isChecked() else "Firefly Algorithm" if self.type1.isChecked() else "Differential Evolution",
            self.Settings)
        dlg.show()
        if dlg.exec_(): self.Settings = {
            'maxGen':dlg.maxGen.value(), 'report':dlg.report.value(),
            'AxMin':dlg.AxMin.value(), 'AyMin':dlg.AyMin.value(),
            'DxMin':dlg.DxMin.value(), 'DyMin':dlg.DyMin.value(),
            'IMin':dlg.IMin.value(), 'LMin':dlg.LMin.value(),
            'FMin':dlg.FMin.value(), 'AMin':dlg.AMin.value(),
            'AxMax':dlg.AxMax.value(), 'AyMax':dlg.AyMax.value(),
            'DxMax':dlg.DxMax.value(), 'DyMax':dlg.DyMax.value(),
            'IMax':dlg.IMax.value(), 'LMax':dlg.LMax.value(),
            'FMax':dlg.FMax.value(), 'AMax':dlg.AMax.value()}
