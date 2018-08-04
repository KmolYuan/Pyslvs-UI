# -*- coding: utf-8 -*-

"""The option dialog use to adjust the setting of algorithm."""

__author__ = "Yuan Chang"
__copyright__ = "Copyright (C) 2016-2018"
__license__ = "AGPL"
__email__ = "pyslvs@gmail.com"

from enum import Enum
from typing import (
    List,
    Tuple,
    Dict,
    Any,
)
from core.QtModules import (
    pyqtSlot,
    Qt,
    QDialog,
    QTableWidgetItem,
    QDoubleSpinBox,
    QSpinBox,
    QWidget,
)
from core.info import html
from .Ui_options import Ui_Dialog


GeneticPrams = {
    'nPop': 500,
    'pCross': 0.95,
    'pMute': 0.05,
    'pWin': 0.95,
    'bDelta': 5.,
}

FireflyPrams = {
    'n': 80,
    'alpha': 0.01,
    'betaMin': 0.2,
    'gamma': 1.,
    'beta0': 1.,
}

DifferentialPrams = {
    'strategy': 1,
    'NP': 400,
    'F': 0.6,
    'CR': 0.9,
}

defaultSettings = {'maxGen': 1000, 'report': 10}


class AlgorithmType(Enum):
    
    """Enum type of algorithms."""
    
    def __str__(self):
        return str(self.value)
    
    RGA = "Real-coded Genetic Algorithm"
    Firefly = "Firefly Algorithm"
    DE = "Differential Evolution"


class AlgorithmOptionDialog(QDialog, Ui_Dialog):
    
    """Option dialog.
    
    Only edit the settings after closed.
    """
    
    def __init__(self,
        algorithm: AlgorithmType,
        settings: Dict[str, Any],
        parent: QWidget
    ):
        """Load the settings to user interface."""
        super(AlgorithmOptionDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setWindowTitle("{} Options".format(algorithm.value))
        
        self.__algorithm = algorithm
        self.__init_alg_table()
        self.alg_table.setColumnWidth(0, 200)
        self.alg_table.setColumnWidth(1, 90)
        self.__setArgs(settings)
    
    def __init_alg_table(self):
        """Initialize the algorithm table widgets."""
        
        def writeTable(
            integers: List[Tuple[str, str, str]] = [],
            floats: List[Tuple[str, str, str]] = []
        ):
            """Use to write table data."""
            i = 0
            for Types, box, maxV in zip(
                (integers, floats),
                (QSpinBox, QDoubleSpinBox),
                (9, 10.)
            ):
                for name, vname, tooltip in Types:
                    self.alg_table.insertRow(i)
                    name_cell = QTableWidgetItem(name)
                    name_cell.setToolTip(tooltip)
                    self.alg_table.setItem(i, 0, name_cell)
                    spinbox = box()
                    spinbox.setMaximum(maxV)
                    spinbox.setToolTip(vname)
                    self.alg_table.setCellWidget(i, 1, spinbox)
                    i += 1
        
        if self.__algorithm == AlgorithmType.RGA:
            writeTable(
                floats=[
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
        elif self.__algorithm == AlgorithmType.Firefly:
            writeTable(
                floats=[
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
        elif self.__algorithm == AlgorithmType.DE:
            writeTable(
                integers=[
                    ("Evolutionary strategy (0-9)", 'strategy',
                        html("There are 10 way to evolution."))
                ],
                floats=[
                    ("Weight factor", 'F',
                        html("Weight factor is usually between 0.5 and 1" +
                            "(in rare cases > 1).")),
                    ("Recombination factor", 'CR',
                        html("The chance of crossover possible."))
                ]
            )
    
    def __setArgs(self, settings: Dict[str, Any]):
        """Set arguments by settings dict."""
        if 'maxGen' in settings:
            self.maxGen.setValue(settings['maxGen'])
        elif 'minFit' in settings:
            self.minFit_option.setChecked(True)
            self.minFit.setValue(settings['minFit'])
        elif 'maxTime' in settings:
            self.maxTime_option.setChecked(True)
            #In second (int).
            maxTime = settings['maxTime']
            self.maxTime_h.setValue(maxTime // 3600)
            self.maxTime_m.setValue((maxTime % 3600) // 60)
            self.maxTime_s.setValue(maxTime % 3600 % 60)
        self.report.setValue(settings['report'])
        if self.__algorithm == AlgorithmType.RGA:
            self.pop_size.setValue(settings['nPop'])
            for i, tag in enumerate(['pCross', 'pMute', 'pWin', 'bDelta']):
                self.alg_table.cellWidget(i, 1).setValue(settings[tag])
        elif self.__algorithm == AlgorithmType.Firefly:
            self.pop_size.setValue(settings['n'])
            for i, tag in enumerate(['alpha', 'betaMin', 'gamma', 'beta0']):
                self.alg_table.cellWidget(i, 1).setValue(settings[tag])
        elif self.__algorithm == AlgorithmType.DE:
            self.pop_size.setValue(settings['NP'])
            for i, tag in enumerate(['strategy', 'F', 'CR']):
                self.alg_table.cellWidget(i, 1).setValue(settings[tag])
    
    @pyqtSlot(name='on_reset_button_clicked')
    def __reset(self):
        """Reset the settings to default."""
        #Differential Evolution (Default)
        d = defaultSettings.copy()
        if self.__algorithm == AlgorithmType.RGA:
            d.update(GeneticPrams)
        elif self.__algorithm == AlgorithmType.Firefly:
            d.update(FireflyPrams)
        elif self.__algorithm == AlgorithmType.DE:
            d.update(DifferentialPrams)
        self.__setArgs(d)
