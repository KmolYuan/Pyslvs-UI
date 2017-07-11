# -*- coding: utf-8 -*-
from ...QtModules import *
from .Ui_Path_Solving import Ui_Form as PathSolving_Form
from ...graphics.ChartGraphics import ChartDialog
from .Path_Solving_options import Path_Solving_options_show
from .Path_Solving_progress_zmq import Path_Solving_progress_zmq_show
from .Path_Solving_series import Path_Solving_series_show

class Path_Solving_show(QWidget, PathSolving_Form):
    addPathPoint = pyqtSignal(float, float)
    deletePathPoint = pyqtSignal(int)
    moveupPathPoint = pyqtSignal(int)
    movedownPathPoint = pyqtSignal(int)
    mergeResult = pyqtSignal(int)
    GeneticPrams = {'nPop':250, 'pCross':0.95, 'pMute':0.05, 'pWin':0.95, 'bDelta':5.}
    FireflyPrams = {'n':40, 'alpha':0.01, 'betaMin':0.2, 'gamma':1., 'beta0':1.}
    DifferentialPrams = {'strategy':1, 'NP':190, 'F':0.6, 'CR':0.9}
    defaultSettings = {'maxGen':1500, 'report':1, 'AxMin':-50., 'AyMin':-50., 'DxMin':-50., 'DyMin':-50., 'IMin':5., 'LMin':5., 'FMin':5., 'AMin':0.,
        'AxMax':50., 'AyMax':50., 'DxMax':50., 'DyMax':50., 'IMax':50., 'LMax':50., 'FMax':50., 'AMax':360.,
        'algorithmPrams':DifferentialPrams}
    mechanismParams_4Bar = { #No 'targetPath'
        'Driving':'A',
        'Follower':'D',
        'Link':'L0,L1,L2,L3,L4',
        'Target':'E',
        'ExpressionName':'PLAP,PLLP,PLLP',
        'Expression':'A,L0,a0,D,B,B,L1,L2,D,C,B,L3,L4,C,E',
        'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'}],
        'formula':['PLAP','PLLP']}
    mechanismParams_4Bar['VARS'] = len(set(mechanismParams_4Bar['Expression'].split(',')))-2
    mechanismParams_8Bar = { #No 'targetPath'
        'Driving':'A',
        'Follower':'B',
        'Link':'L0,L1,L2,L3,L4,L5,L6,L7,L8,L9,L10',
        'Target':'H',
        'ExpressionName':'PLAP,PLLP,PLLP,PLLP,PLLP,PLLP',
        'Expression':'A,L0,a0,B,C,B,L2,L1,C,D,B,L4,L3,D,E,C,L5,L6,B,F,F,L8,L7,E,G,F,L9,L10,G,H',
        'constraint':[{'driver':'L0', 'follower':'L2', 'connect':'L1'}],
        'formula':['PLAP','PLLP']}
    mechanismParams_8Bar['VARS'] = len(set(mechanismParams_8Bar['Expression'].split(',')))-2
    
    def __init__(self, path, mechanism_data, parent=None):
        super(Path_Solving_show, self).__init__(parent)
        self.setupUi(self)
        self.mechanism_data = mechanism_data
        self.path = path
        for e in path: self.Point_list.addItem("({}, {})".format(e['x'], e['y']))
        for e in mechanism_data: self.addResult(e)
        self.Settings = self.defaultSettings
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
            c = self.Point_list.currentItem().text()[1:-1].split(', ')
            self.Point_list.insertItem(n+2, "({}, {})".format(c[0], c[1]))
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
            "<html><head/><body><p><span style=\"font-size:12pt; color:#00aa00;\">"+str(self.Point_list.count())+"</span></p></body></html>")
        n = self.Point_list.count()>1
        self.GenerateLocal.setEnabled(n)
        self.GenerateZMQ.setEnabled(n)
    
    @pyqtSlot()
    def on_GenerateLocal_clicked(self): self.startAlgorithm()
    @pyqtSlot()
    def on_GenerateZMQ_clicked(self): self.startAlgorithm(True)
    def startAlgorithm(self, hasPort=False):
        type_num, mechanismParams, GenerateData = self.getGenerate()
        dlg = Path_Solving_progress_zmq_show(type_num, mechanismParams, GenerateData, self.Settings['algorithmPrams'],
            PORT=self.portText.text() if hasPort else None, parent=self)
        dlg.show()
        if dlg.exec_():
            self.mechanism_data.append(dlg.mechanism)
            self.addResult(dlg.mechanism)
            sec = dlg.time_spand%60
            mins = int(dlg.time_spand/60)
            self.timeShow.setText("<html><head/><body><p><span style=\"font-size:10pt\">{}[min] {}[s]</span></p></body></html>".format(mins, sec))
            print('Finished.')
    def getGenerate(self):
        type_num = 0 if self.type0.isChecked() else 1 if self.type1.isChecked() else 2
        mechanismParams = self.mechanismParams_4Bar if self.FourBar.isChecked() else self.mechanismParams_8Bar
        link_q = mechanismParams['VARS']-7
        upper = [self.Settings['AxMax'], self.Settings['AyMax'], self.Settings['DxMax'], self.Settings['DyMax'],
            self.Settings['IMax'], self.Settings['LMax'], self.Settings['FMax']]+[self.Settings['LMax']]*link_q
        lower = [self.Settings['AxMin'], self.Settings['AyMin'], self.Settings['DxMin'], self.Settings['DyMin'],
            self.Settings['IMin'], self.Settings['LMin'], self.Settings['FMin']]+[self.Settings['LMin']]*link_q
        mechanismParams['targetPath'] = tuple((e['x'], e['y']) for e in self.path)
        p = len(self.path)
        GenerateData = {
            'nParm':p+mechanismParams['VARS'],
            'upper':upper+[self.Settings['AMax']]*p,
            'lower':lower+[self.Settings['AMin']]*p,
            'maxGen':self.Settings['maxGen'],
            'report':int(self.Settings['maxGen']*self.Settings['report']/100)}
        return type_num, mechanismParams, GenerateData
    
    def addResult(self, e):
        keys = sorted(list(e.keys()))
        item = QListWidgetItem("{} ({} gen)".format(e['Algorithm'], e['GenerateData']['maxGen']))
        item.setToolTip('\n'.join(["[{}] ({} gen)".format(e['Algorithm'], e['GenerateData']['maxGen'])]+["{}: {}".format(k, e[k]) for k in keys
            if not k in ['Algorithm', 'TimeAndFitness', 'mechanismParams', 'GenerateData', 'algorithmPrams']]))
        self.Result_list.addItem(item)
    
    @pyqtSlot()
    def on_deleteButton_clicked(self):
        row = self.Result_list.currentRow()
        del self.mechanism_data[row]
        self.Result_list.takeItem(row)
        self.isGetResult()
    
    def isGetResult(self):
        for button in [self.mergeButton, self.deleteButton]: button.setEnabled(self.Result_list.currentRow()>-1)
    
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
    
    @pyqtSlot(int)
    def on_Result_list_currentRowChanged(self, cr):
        self.isGetResult()
        if cr>-1:
            args = self.mechanism_data[cr]
            if args['Algorithm']=='Genetic': self.type0.setChecked(True)
            elif args['Algorithm']=='Firefly': self.type1.setChecked(True)
            elif args['Algorithm']=="Differtial Evolution": self.type2.setChecked(True)
            GenerateData = args['GenerateData']
            self.Settings = {'maxGen':GenerateData['maxGen'], 'report':GenerateData['maxGen']/GenerateData['report']/100,
                'AxMax':GenerateData['upper'][0], 'AxMin':GenerateData['lower'][0],
                'AyMax':GenerateData['upper'][1], 'AyMin':GenerateData['lower'][1],
                'DxMax':GenerateData['upper'][2], 'DxMin':GenerateData['lower'][2],
                'DyMax':GenerateData['upper'][3], 'DyMin':GenerateData['lower'][3],
                'IMax':GenerateData['upper'][4], 'IMin':GenerateData['lower'][4],
                'LMax':GenerateData['upper'][5], 'LMin':GenerateData['lower'][5],
                'FMax':GenerateData['upper'][6], 'FMin':GenerateData['lower'][6],
                'AMax':GenerateData['upper'][-1], 'AMin':GenerateData['lower'][-1]}
            self.Settings['algorithmPrams'] = args['algorithmPrams']
            self.on_clearAll_clicked()
            for e in args['mechanismParams']['targetPath']: self.on_add_clicked(e[0], e[1])
    
    def algorithmPrams_default(self):
        type_num = 0 if self.type0.isChecked() else 1 if self.type1.isChecked() else 2
        if type_num==0: self.Settings['algorithmPrams'] = self.GeneticPrams
        elif type_num==1: self.Settings['algorithmPrams'] = self.FireflyPrams
        elif type_num==2: self.Settings['algorithmPrams'] = self.DifferentialPrams
    @pyqtSlot(bool)
    def on_type0_toggled(self, checked): self.algorithmPrams_default()
    @pyqtSlot(bool)
    def on_type1_toggled(self, checked): self.algorithmPrams_default()
    @pyqtSlot(bool)
    def on_type2_toggled(self, checked): self.algorithmPrams_default()
    
    @pyqtSlot()
    def on_advanceButton_clicked(self):
        type_num = "Genetic Algorithm" if self.type0.isChecked() else "Firefly Algorithm" if self.type1.isChecked() else "Differential Evolution"
        dlg = Path_Solving_options_show("4 Bar", type_num, self.Settings)
        dlg.show()
        if dlg.exec_():
            tablePL = lambda row: dlg.PLTable.cellWidget(row, 1).value()
            self.Settings = {'maxGen':dlg.maxGen.value(), 'report':dlg.report.value(),
                'AxMax':tablePL(0), 'AxMin':tablePL(1),
                'AyMax':tablePL(2), 'AyMin':tablePL(3),
                'DxMax':tablePL(4), 'DxMin':tablePL(5),
                'DyMax':tablePL(6), 'DyMin':tablePL(7),
                'IMax':tablePL(8), 'IMin':tablePL(9),
                'LMax':tablePL(10), 'LMin':tablePL(11),
                'FMax':tablePL(12), 'FMin':tablePL(13),
                'AMax':tablePL(14), 'AMin':tablePL(15)}
            tableAP = lambda row: dlg.APTable.cellWidget(row, 1).value()
            if type_num=="Genetic Algorithm": self.Settings['algorithmPrams'] = {
                'nPop':tableAP(0), 'pCross':tableAP(1), 'pMute':tableAP(2), 'pWin':tableAP(3), 'bDelta':tableAP(4)}
            elif type_num=="Firefly Algorithm": self.Settings['algorithmPrams'] = {
                'n':tableAP(0), 'alpha':tableAP(1), 'betaMin':tableAP(2), 'gamma':tableAP(3), 'beta0':tableAP(4)}
            elif type_num=="Differential Evolution": self.Settings['algorithmPrams'] = {
                'strategy':tableAP(0), 'NP':tableAP(1), 'F':tableAP(2), 'CR':tableAP(3)}
