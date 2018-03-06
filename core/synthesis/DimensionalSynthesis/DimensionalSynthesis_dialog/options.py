# -*- coding: utf-8 -*-

"""The option dialog use to adjust the setting of algorithm."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from core.QtModules import (
    QDialog,
    Qt,
    QTableWidgetItem,
    QDoubleSpinBox,
    QSpinBox,
    pyqtSlot,
    QDialogButtonBox,
)
from core.info import html
from enum import Enum
from typing import (
    List,
    Tuple,
    Dict,
    Any
)
from .Ui_options import Ui_Dialog

GeneticPrams = {
    'nPop': 500,
    'pCross': 0.95,
    'pMute': 0.05,
    'pWin': 0.95,
    'bDelta': 5.
}
FireflyPrams = {
    'n': 80,
    'alpha': 0.01,
    'betaMin': 0.2,
    'gamma': 1.,
    'beta0': 1.
}
DifferentialPrams = {
    'strategy': 1,
    'NP': 400,
    'F': 0.6,
    'CR': 0.9
}
defaultSettings = {
    'maxGen': 1000, 'report': 10,
    'IMin': 5., 'LMin': 5.,
    'FMin': 5., 'AMin': 0.,
    'IMax': 100., 'LMax': 100.,
    'FMax': 100., 'AMax': 360.,
    'algorithmPrams': DifferentialPrams
}

class AlgorithmType(Enum):
    
    """Enum type of algorithms."""
    
    def __str__(self):
        return str(self.value)
    
    RGA = "Real-coded Genetic Algorithm"
    Firefly = "Firefly Algorithm"
    DE = "Differential Evolution"

class Options_show(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Only edit the settings after closed.
    """
    
    def __init__(self,
        algorithm: AlgorithmType,
        settings: Dict[str, Any],
        parent=None
    ):
        super(Options_show, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.algorithm = algorithm
        self.settings_tab.setTabText(1, self.algorithm.value)
        self.init_PLTable()
        self.init_APTable()
        for table in [self.APTable, self.PLTable]:
            table.setColumnWidth(0, 200)
            table.setColumnWidth(1, 90)
        self.setArgs(settings)
        self.isOk()
    
    def init_PLTable(self):
        """Initialize the linkage table widgets."""
        
        def writeTable(
            Length: List[Tuple[str, str, str]],
            Degrees: List[Tuple[str, str, str]]
        ):
            """Use to write table data."""
            i = 0
            for Types, maxV, minV in zip(
                [Length, Degrees],
                [1000., 360.],
                [0.1, 0.]
            ):
                for name, vname, tooltip in Types:
                    self.PLTable.insertRow(i)
                    name_cell = QTableWidgetItem(name)
                    name_cell.setToolTip(tooltip)
                    self.PLTable.setItem(i, 0, name_cell)
                    spinbox = QDoubleSpinBox()
                    spinbox.setMaximum(maxV)
                    spinbox.setMinimum(minV)
                    spinbox.setToolTip(vname)
                    self.PLTable.setCellWidget(i, 1, spinbox)
                    i += 1
        
        title = "{} maximum".format
        des = "This value holds with the {} random number of {}.".format
        data = lambda t, p, m: (title(t), p, html(des(m, t.lower())))
        
        writeTable(
            Length=[
                data("Input linkage", 'IMax', 'maximum'),
                data("Input linkage", 'IMin', 'minimum'),
                data("Connected linkage", 'LMax', 'maximum'),
                data("Connected linkage", 'LMin', 'minimum'),
                data("Follower linkage", 'FMax', 'maximum'),
                data("Follower linkage", 'FMin', 'minimum')
            ],
            Degrees=[
                data("Input angle", 'AMax', 'maximum'),
                data("Input angle", 'AMin', 'minimum')
            ])
        for i in range(self.PLTable.rowCount()):
            self.PLTable.cellWidget(i, 1).valueChanged.connect(self.isOk)
    
    def init_APTable(self):
        """Initialize the algorithm table widgets."""
        
        def writeTable(
            Integers: List[Tuple[str, str, str]],
            Floats: List[Tuple[str, str, str]]
        ):
            """Use to write table data."""
            i = 0
            for Types, box, maxV in zip(
                [Integers, Floats],
                [QSpinBox, QDoubleSpinBox],
                [9, 10.]
            ):
                for name, vname, tooltip in Types:
                    self.APTable.insertRow(i)
                    name_cell = QTableWidgetItem(name)
                    name_cell.setToolTip(tooltip)
                    self.APTable.setItem(i, 0, name_cell)
                    spinbox = box()
                    spinbox.setMaximum(maxV)
                    spinbox.setToolTip(vname)
                    self.APTable.setCellWidget(i, 1, spinbox)
                    i += 1
        
        if self.algorithm == AlgorithmType.RGA:
            writeTable(
                Floats=[
                    ("Crossover Rate", 'pCross',
                        html("The chance of crossover.")),
                    ("Mutation Rate", 'pMute',
                        html("The chance of mutation.")),
                    ("Winning Rate", 'pWin',
                        html("The chance of winning.")),
                    ("Delta value", 'bDelta',
                        html("The power value when matching chromosome."))
                ]
            )
        elif self.algorithm == AlgorithmType.Firefly:
            writeTable(
                Floats=[
                    ("Alpha value", 'alpha',
                        html("Alpha value is the step size of the firefly.")),
                    ("Minimum Beta value", 'betaMin',
                        html("The minimal attraction, must not less than this.")),
                    ("Gamma value", 'gamma',
                        html("Beta will multiplied by exponential power value " +
                            "with this weight factor.")),
                    ("Beta0 value", 'beta0',
                        html("The attraction of two firefly in 0 distance."))
                ]
            )
        elif self.algorithm == AlgorithmType.DE:
            writeTable(
                Integers=[
                    ("Evolutionary strategy (0-9)", 'strategy',
                        html("There are 10 way to evolution."))
                ],
                Floats=[
                    ("Weight factor", 'F',
                        html("Weight factor is usually between 0.5 and 1" +
                            "(in rare cases > 1).")),
                    ("Recombination factor", 'CR',
                        html("The chance of crossover possible."))
                ]
            )
    
    def setArgs(self, PLnAP: Dict[str, Any]):
        """Set arguments by settings dict."""
        if 'maxGen' in PLnAP:
            self.maxGen.setValue(PLnAP['maxGen'])
        elif 'minFit' in PLnAP:
            self.minFit_option.setChecked(True)
            self.minFit.setValue(PLnAP['minFit'])
        elif 'maxTime' in PLnAP:
            self.maxTime_option.setChecked(True)
            #In second (int).
            maxTime = PLnAP['maxTime']
            self.maxTime_h.setValue(maxTime // 3600)
            self.maxTime_m.setValue((maxTime % 3600) // 60)
            self.maxTime_s.setValue(maxTime % 3600 % 60)
        self.report.setValue(PLnAP['report'])
        for i, tag in enumerate([
            'IMax',
            'IMin',
            'LMax',
            'LMin',
            'FMax',
            'FMin',
            'AMax',
            'AMin'
        ]):
            self.PLTable.cellWidget(i, 1).setValue(PLnAP[tag])
        if self.algorithm == AlgorithmType.RGA:
            self.popSize.setValue(PLnAP['algorithmPrams']['nPop'])
            for i, tag in enumerate(['pCross', 'pMute', 'pWin', 'bDelta']):
                self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
        elif self.algorithm == AlgorithmType.Firefly:
            self.popSize.setValue(PLnAP['algorithmPrams']['n'])
            for i, tag in enumerate(['alpha', 'betaMin', 'gamma', 'beta0']):
                self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
        elif self.algorithm == AlgorithmType.DE:
            self.popSize.setValue(PLnAP['algorithmPrams']['NP'])
            for i, tag in enumerate(['strategy', 'F', 'CR']):
                self.APTable.cellWidget(i, 1).setValue(PLnAP['algorithmPrams'][tag])
    
    @pyqtSlot(int)
    @pyqtSlot(float)
    def isOk(self, r=None):
        """Set buttons enable if values ok."""
        n = True
        pre = 0
        for i in range(self.PLTable.rowCount()):
            if i%2 == 0:
                pre = self.PLTable.cellWidget(i, 1).value()
            elif i%2 == 1:
                n &= pre>=self.PLTable.cellWidget(i, 1).value()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(n)
    
    @pyqtSlot()
    def on_setDefault_clicked(self):
        """Reset the settings to default."""
        #Differential Evolution (Default)
        d = defaultSettings.copy()
        if self.algorithm == AlgorithmType.RGA:
            d['algorithmPrams'] = GeneticPrams.copy()
        elif self.algorithm == AlgorithmType.Firefly:
            d['algorithmPrams'] = FireflyPrams.copy()
        self.setArgs(d)
